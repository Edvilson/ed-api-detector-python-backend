import re
import unicodedata
import numpy as np
from typing import List, Dict

from app.config import settings

# OpenAI é opcional: só inicializa se habilitado e chave existir
_client = None
if settings.USE_OPENAI and settings.OPENAI_API_KEY:
    try:
        from openai import OpenAI
        _client = OpenAI(api_key=settings.OPENAI_API_KEY)
    except Exception:
        _client = None  # se não conseguir inicializar, segue com local

# ---------------------------
# Utilidades
# ---------------------------
def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)

_word_re = re.compile(r"\w+", re.UNICODE)

def _normalize(text: str) -> str:
    # minúsculas + remover acentos
    text = text.lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return text

def _tokenize(text: str) -> List[str]:
    text = _normalize(text)
    return _word_re.findall(text)

def _bow_vector(tokens: List[str], vocab: Dict[str, int]) -> np.ndarray:
    vec = np.zeros(len(vocab), dtype=float)
    for t in tokens:
        idx = vocab.get(t)
        if idx is not None:
            vec[idx] += 1.0
    # opcional: normalização L2
    return vec

def classify_similarity(pct: float) -> str:
    if pct >= 90:
        return "Muito semelhante"
    if pct >= 70:
        return "Parcialmente semelhante"
    return "Textos diferentes"

# ---------------------------
# Similaridade via OpenAI (quando disponível)
# ---------------------------
def _similarity_openai(text1: str, text2: str):
    if not _client:
        raise RuntimeError("OpenAI indisponível")

    resp = _client.embeddings.create(
        model="text-embedding-3-small",
        input=[text1, text2]
    )
    vec1 = np.array(resp.data[0].embedding, dtype=float)
    vec2 = np.array(resp.data[1].embedding, dtype=float)
    score = _cosine_similarity(vec1, vec2)
    pct = round(score * 100, 2)
    return {
        "similaridade": pct,
        "classificacao": classify_similarity(pct),
        "resumo": "Comparação feita via embeddings e cosseno (OpenAI)",
        "fonte": "openai"
    }

# ---------------------------
# Similaridade local (fallback)
# ---------------------------
def _similarity_local(text1: str, text2: str):
    # Tokenização simples + bag-of-words + cosseno
    t1 = _tokenize(text1)
    t2 = _tokenize(text2)
    vocab = {}
    for t in set(t1 + t2):
        vocab.setdefault(t, len(vocab))
    v1 = _bow_vector(t1, vocab)
    v2 = _bow_vector(t2, vocab)

    score = _cosine_similarity(v1, v2)
    pct = round(score * 100, 2)
    return {
        "similaridade": pct,
        "classificacao": classify_similarity(pct),
        "resumo": "Comparação local via bag-of-words e cosseno",
        "fonte": "local"
    }

# ---------------------------
# API pública usada pelo serviço
# ---------------------------
def calculate_similarity(text1: str, text2: str):
    # tenta OpenAI se habilitado; senão, cai para local
    if _client:
        try:
            return _similarity_openai(text1, text2)
        except Exception:
            # fallback silencioso para local
            pass
    # fallback
    return _similarity_local(text1, text2)

from openai import OpenAI
from app.config import settings
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def calculate_similarity(text1: str, text2: str):
    resp = client.embeddings.create(
        model="text-embedding-3-small",
        input=[text1, text2]
    )
    vec1 = np.array(resp.data[0].embedding, dtype=float)
    vec2 = np.array(resp.data[1].embedding, dtype=float)
    score = float(cosine_similarity([vec1], [vec2])[0][0])
    percentual = round(score * 100, 2)

    return {
        "similaridade": percentual,
        "classificacao": classify_similarity(percentual),
        "resumo": "Comparação feita via embeddings e cosseno"
    }

def classify_similarity(pct: float) -> str:
    if pct >= 90:
        return "Muito semelhante"
    if pct >= 70:
        return "Parcialmente semelhante"
    return "Textos diferentes"

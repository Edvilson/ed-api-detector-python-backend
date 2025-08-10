# 🕵️‍♂️ ED API Detector Backend

API para detecção de similaridade entre textos, com suporte a:
- **Embeddings OpenAI** (modelo `text-embedding-3-small`)
- **Fallback local** (bag-of-words + similaridade de cosseno)
- Autenticação JWT
- Controle de API Key
- Persistência de histórico no banco de dados (PostgreSQL / Supabase)

---

## 🚀 Requisitos

- Python 3.10+
- Banco de dados PostgreSQL (pode usar Supabase)
- Pipenv ou virtualenv
- Chave da OpenAI **(opcional)**

---

## 📊 Fluxo Fallback

```mermaid
flowchart TD
    A[Início: /api/compare] --> B{USE_OPENAI=true<br/>e OPENAI_API_KEY definida?}
    B -- "Não" --> L[Calcular similaridade LOCAL<br/>(Bag-of-Words + Cosseno)]
    B -- "Sim" --> C[Tentar Embeddings OpenAI<br/>(text-embedding-3-small)]
    C -->|Sucesso| D[Cosine de embeddings]
    C -->|Erro: 401/403/429/5xx<br/>timeout/rede| L
    D --> E[Classificar % → rótulo]
    L --> M[Classificar % → rótulo]
    E --> N[Salvar em comparisons<br/>resultado.fonte = "openai"]
    M --> O[Salvar em comparisons<br/>resultado.fonte = "local"]
    N --> P[Responder JSON]
    O --> P[Responder JSON]


## 📦 Instalação

```bash
git clone https://github.com/Edvilson/ed-api-detector-python-backend.git
cd ed-api-detector-python-backend

python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

pip install -r requirements.txt

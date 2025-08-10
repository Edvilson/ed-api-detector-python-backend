# 📝 API Detector de Plágio com Fallback

API para detecção de similaridade de textos com suporte a fallback para cálculo local quando a API da OpenAI não está disponível.

## 🚀 Funcionalidades

- Comparação de textos usando **OpenAI Embeddings** (quando disponível)
- Fallback para cálculo de similaridade local (Bag-of-Words + Cosseno)
- Autenticação **JWT**
- Controle de **API Key**
- Persistência de histórico no banco de dados (PostgreSQL / Supabase)

## 📋 Requisitos

- Python 3.10+
- Banco de dados PostgreSQL (pode usar Supabase)
- Pipenv ou virtualenv
- Chave da OpenAI *(opcional)*

---

## 📊 Fluxo Fallback

```mermaid
flowchart TD
    A["Início: /api/compare"] --> B{"USE_OPENAI=true e OPENAI_API_KEY definida?"}
    B -- "Não" --> L["Calcular similaridade LOCAL (Bag of Words + Cosseno)"]
    B -- "Sim" --> C["Tentar Embeddings OpenAI (text-embedding-3-small)"]
    C -->|Sucesso| D["Cosine de embeddings"]
    C -->|Erro: 401 / 403 / 429 / 5xx ou timeout| L
    D --> E["Classificar % → rótulo"]
    L --> M["Classificar % → rótulo"]
    E --> N["Salvar em comparisons - fonte: openai"]
    M --> O["Salvar em comparisons - fonte: local"]
    N --> P["Responder JSON"]
    O --> P["Responder JSON"]
```
---

## 📦 Instalação

```bash
git clone https://github.com/seu-repo/ed-api-detector-python-backend.git
cd ed-api-detector-python-backend

python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

pip install -r requirements.txt

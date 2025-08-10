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

## 📦 Instalação

```bash
git clone https://github.com/Edvilson/ed-api-detector-python-backend.git
cd ed-api-detector-python-backend

python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

pip install -r requirements.txt

# Detector de Plágio - Backend (FastAPI)

## Rodando local
1. Crie um `.env` baseado no `.env.example`
2. `pip install -r requirements.txt`
3. `uvicorn app.main:app --reload`

## Segurança
- Todas as rotas exigem `X-API-KEY` (mestra, definida no .env)
- Rotas protegidas exigem JWT no header `Authorization: Bearer <token>`
- `/docs` só aparece se `ENVIRONMENT=development`

## Endpoints
- POST `/api/auth/register`
- POST `/api/auth/login`
- POST `/api/compare` (protegida; consome OpenAI embeddings)
- PUT  `/api/plan?plan_name=free|pro|premium` (protegida)

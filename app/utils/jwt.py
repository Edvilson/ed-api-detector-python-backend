# app/utils/jwt.py
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.config import settings
from app.models.user import User
from app.dependencies import get_db

ALG = getattr(settings, "JWT_ALGORITHM", "HS256")
security = HTTPBearer(auto_error=True)  # adiciona "Authorize" no Swagger

def create_jwt_token(user: User):
    payload = {"sub": str(user.id), "exp": datetime.utcnow() + timedelta(hours=12)}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=ALG)

def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    # Swagger envia automaticamente: Authorization: Bearer <token>
    token = creds.credentials
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[ALG])
        user = db.query(User).filter(User.id == payload.get("sub")).first()
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")

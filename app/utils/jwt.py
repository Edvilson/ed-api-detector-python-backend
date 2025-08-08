import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Header
from sqlalchemy.orm import Session
from app.config import settings
from app.database import SessionLocal
from app.models.user import User

def create_jwt_token(user: User):
    payload = {"sub": str(user.id), "exp": datetime.utcnow() + timedelta(hours=12)}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

def get_current_user(authorization: str = Header(...), db: Session = SessionLocal()):
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Header Authorization inválido")
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        user = db.query(User).filter_by(id=payload.get("sub")).first()
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")

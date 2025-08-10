from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from app.config import settings
from app.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def validate_api_key(x_api_key: str = Header(..., alias="X-API-KEY")):
    if x_api_key != settings.API_KEY_MASTER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API Key inválida"
        )

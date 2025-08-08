from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserLogin
from app.utils.password import hash_password, verify_password
from app.utils.jwt import create_jwt_token

def register_user(data: UserCreate, db: Session):
    if db.query(User).filter_by(email=data.email).first():
        raise HTTPException(status_code=400, detail="Email já registrado")
    user = User(name=data.name, email=data.email, password_hash=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"access_token": create_jwt_token(user), "token_type": "bearer"}

def login_user(data: UserLogin, db: Session):
    user = db.query(User).filter_by(email=data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return {"access_token": create_jwt_token(user), "token_type": "bearer"}

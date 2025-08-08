from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserLogin, TokenResponse
from app.services.auth_service import register_user, login_user
from app.dependencies import get_db, validate_api_key

router = APIRouter(dependencies=[Depends(validate_api_key)])

@router.post("/register", response_model=TokenResponse)
def register(data: UserCreate, db: Session = Depends(get_db)):
    return register_user(data, db)

@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    return login_user(data, db)

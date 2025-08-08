from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.comparison_schema import CompareRequest
from app.services.compare_service import compare_texts
from app.dependencies import get_db, validate_api_key, get_current_user_dep

router = APIRouter(dependencies=[Depends(validate_api_key)])

@router.post("/compare")
def compare(data: CompareRequest, db: Session = Depends(get_db), user=Depends(get_current_user_dep)):
    return compare_texts(data.texto_1, data.texto_2, user, db)

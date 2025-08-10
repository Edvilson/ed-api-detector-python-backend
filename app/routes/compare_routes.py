from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.comparison_schema import CompareRequest, CompareResponse
from app.services.compare_service import compare_texts
from app.dependencies import get_db, validate_api_key
from app.utils.jwt import get_current_user

router = APIRouter(dependencies=[Depends(validate_api_key)])

@router.post("/compare", response_model=CompareResponse)
def compare(
    data: CompareRequest,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),  # pega o Bearer via HTTPBearer
):
    return compare_texts(data.texto_1, data.texto_2, user, db)

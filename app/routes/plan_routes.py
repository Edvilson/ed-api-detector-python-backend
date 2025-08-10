from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db, validate_api_key
from app.models.plan import Plan
from app.utils.jwt import get_current_user

router = APIRouter(dependencies=[Depends(validate_api_key)])

@router.put("/plan")
def change_user_plan(
    plan_name: str,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    plan = db.query(Plan).filter_by(name=plan_name).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plano não encontrado")
    user.plan = plan.name
    db.commit()
    return {"msg": f"Plano alterado para {plan.name}", "limite_diario": plan.daily_limit}

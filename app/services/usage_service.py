from datetime import datetime
from sqlalchemy import func
from fastapi import HTTPException
from app.models.plan import Plan
from app.models.comparison import Comparison

def check_daily_limit(user, db):
    plan = db.query(Plan).filter_by(name=user.plan).first()
    if not plan:
        raise HTTPException(status_code=500, detail="Plano inválido")

    today = datetime.utcnow().date()
    total_today = db.query(func.count(Comparison.id)) \        .filter(Comparison.user_id == user.id) \        .filter(func.date(Comparison.created_at) == today) \        .scalar()

    if total_today >= plan.daily_limit:
        raise HTTPException(status_code=429, detail=f"Limite diário do plano '{plan.name}' atingido ({plan.daily_limit})")

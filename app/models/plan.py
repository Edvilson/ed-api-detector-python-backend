from sqlalchemy import Column, Integer, String
from app.database import Base

class Plan(Base):
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    daily_limit = Column(Integer, nullable=False)

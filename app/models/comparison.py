from sqlalchemy import Column, ForeignKey, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from datetime import datetime
from app.database import Base

class Comparison(Base):
    __tablename__ = "comparisons"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    texto_1 = Column(Text, nullable=False)
    texto_2 = Column(Text, nullable=False)
    resultado = Column(JSONB, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

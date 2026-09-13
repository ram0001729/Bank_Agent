from datetime import datetime
from decimal import Decimal

from sqlalchemy import Column, DateTime, Integer, Numeric, String

from backend.database.connection import Base


class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String(64), unique=True, nullable=False, index=True)
    agent_name = Column(String(100), unique=True, nullable=False, index=True)
    role = Column(String(32), nullable=False, index=True)
    status = Column(String(16), nullable=False, default="ACTIVE", index=True)
    daily_budget_limit = Column(Numeric(12, 2), nullable=False, default=Decimal("10000.00"))
    secret_hash = Column(String(64), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    revoked_at = Column(DateTime, nullable=True)

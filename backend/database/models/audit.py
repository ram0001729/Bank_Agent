from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from backend.database.connection import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String, nullable=False, index=True)
    action = Column(String, nullable=False)
    status = Column(String, default="SUCCESS")  # SUCCESS, BLOCKED, DENIED
    details = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

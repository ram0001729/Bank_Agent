from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from backend.database.connection import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    amount = Column(Float, nullable=False)
    merchant = Column(String, nullable=False)
    category = Column(String, default="general")
    status = Column(String, default="completed")  # completed, pending, blocked
    is_fraud = Column(Boolean, default=False)
    risk_score = Column(Float, default=0.0)
    timestamp = Column(DateTime, default=datetime.utcnow)

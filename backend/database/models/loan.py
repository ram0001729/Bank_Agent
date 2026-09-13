from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from backend.database.connection import Base


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    amount = Column(Float, nullable=False)
    term_months = Column(Integer, default=12)
    interest_rate = Column(Float, default=7.5)
    status = Column(String, default="pending")  # pending, approved, rejected
    risk_assessment = Column(String, default="low")
    created_at = Column(DateTime, default=datetime.utcnow)

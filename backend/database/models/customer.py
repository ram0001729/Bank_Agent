from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from backend.database.connection import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    account_number = Column(String, unique=True, index=True, nullable=False)
    balance = Column(Float, default=0.0)
    status = Column(String, default="active")  # active, flagged, frozen
    risk_level = Column(String, default="low")  # low, medium, high
    created_at = Column(DateTime, default=datetime.utcnow)

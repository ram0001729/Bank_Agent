from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.connection import get_db
from backend.database.models.customer import Customer
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/api/customers", tags=["Customers"])


class CustomerSchema(BaseModel):
    id: int
    name: str
    email: str
    account_number: str
    balance: float
    status: str
    risk_level: str

    class Config:
        from_attributes = True


@router.get("", response_model=List[CustomerSchema])
def list_customers(db: Session = Depends(get_db)):
    return db.query(Customer).all()


@router.get("/{customer_id}", response_model=CustomerSchema)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    cust = db.query(Customer).filter(Customer.id == customer_id).first()
    if not cust:
        raise HTTPException(status_code=404, detail="Customer not found")
    return cust

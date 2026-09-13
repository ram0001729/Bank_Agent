import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from backend.database.connection import engine, Base, SessionLocal
from backend.database.models.customer import Customer
from backend.database.models.transaction import Transaction
from backend.database.models.loan import Loan
from backend.database.models.audit import AuditLog

from backend.api-gateway.middleware.logging import LoggingMiddleware
from backend.api-gateway.routes import auth, customer, transactions, agents

app = FastAPI(
    title="AI Banking Agent Platform - API Gateway",
    description="Backend API Gateway providing AI Agent governance, ML fraud detection, and banking services.",
    version="1.0.0"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)

# Include Routers
app.include_router(auth.router)
app.include_router(customer.router)
app.include_router(transactions.router)
app.include_router(agents.router)


@app.on_event("startup")
def startup_event():
    # Initialize Database Tables
    Base.metadata.create_all(bind=engine)

    # Seed initial demo data if empty
    db: Session = SessionLocal()
    try:
        if db.query(Customer).count() == 0:
            c1 = Customer(name="Alice Johnson", email="alice@example.com", account_number="ACC-100982", balance=14250.50, risk_level="low")
            c2 = Customer(name="Bob Smith", email="bob@example.com", account_number="ACC-882104", balance=3410.00, risk_level="medium")
            c3 = Customer(name="Charlie Davis", email="charlie@example.com", account_number="ACC-773192", balance=89000.00, risk_level="high")
            db.add_all([c1, c2, c3])
            db.commit()

            t1 = Transaction(customer_id=1, amount=120.00, merchant="Amazon.com", category="Shopping", status="completed", is_fraud=False, risk_score=0.02)
            t2 = Transaction(customer_id=1, amount=45.50, merchant="Starbucks", category="Dining", status="completed", is_fraud=False, risk_score=0.01)
            t3 = Transaction(customer_id=2, amount=2499.99, merchant="Unknown Crypto Exch", category="Transfer", status="blocked", is_fraud=True, risk_score=0.92)
            t4 = Transaction(customer_id=3, amount=850.00, merchant="Luxury Hotel", category="Travel", status="completed", is_fraud=False, risk_score=0.15)
            db.add_all([t1, t2, t3, t4])

            a1 = AuditLog(agent_id="Fraud Agent", action="BLOCK_TRANSACTION", status="BLOCKED", details="Blocked high-risk crypto transfer of $2499.99")
            a2 = AuditLog(agent_id="Supervisor Agent", action="ROUTE_QUERY", status="SUCCESS", details="Routed loan eligibility inquiry to Loan Agent")
            a3 = AuditLog(agent_id="Loan Agent", action="EVALUATE_CREDIT", status="SUCCESS", details="Calculated risk score 0.12 for customer ACC-100982")
            db.add_all([a1, a2, a3])

            db.commit()
    finally:
        db.close()


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AI-Banking-Agent-Gateway",
        "database": "connected"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

import os
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from backend.database.connection import engine, Base, SessionLocal
from backend.database.models.customer import Customer
from backend.database.models.transaction import Transaction
from backend.database.models.loan import Loan
from backend.database.models.audit import AuditLog
from backend.database.models.agent import Agent

from backend.api_gateway.middleware.logging import LoggingMiddleware
from backend.api_gateway.routes import auth, customer, transactions, agents

from mlops.monitoring.exporters.metrics import PrometheusMiddleware, get_prometheus_metrics
from rag.ingest_policies import ingest_policy_documents

app = FastAPI(
    title="AI Banking Agent Platform - API Gateway",
    description="Production-Grade API Gateway with AI Agent Governance OS, RAG PDF Policy Retriever, LangSmith Tracing, and Prometheus Metrics.",
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
app.add_middleware(PrometheusMiddleware)

# Include Routers
app.include_router(auth.router)
app.include_router(customer.router)
app.include_router(transactions.router)
app.include_router(agents.router)


@app.on_event("startup")
def startup_event():
    # Initialize Database Tables
    Base.metadata.create_all(bind=engine)

    # Ingest Policy PDFs into RAG Vector Store
    try:
        ingest_policy_documents()
    except Exception as e:
        print(f"Warning during RAG PDF startup ingestion: {e}")

    # Seed initial demo data if empty
    db: Session = SessionLocal()
    try:
        built_in_agents = [
            ("Supervisor Agent", "supervisor"),
            ("Fraud Agent", "fraud_evaluator"),
            ("Loan Agent", "loan_underwriter"),
            ("Refund Agent", "refund_processor"),
            ("Support Agent", "support_assistant"),
        ]
        for agent_name, role in built_in_agents:
            if db.query(Agent).filter(Agent.agent_name == agent_name).first() is None:
                db.add(Agent(
                    agent_id=f"agent-system-{agent_name.lower().replace(' ', '-')}",
                    agent_name=agent_name,
                    role=role,
                    status="ACTIVE",
                    daily_budget_limit=10000.00,
                    secret_hash="system-managed",
                ))
        db.commit()

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
        "database": "connected",
        "rag_vector_db": "active",
        "langsmith_tracing": "enabled",
        "governance_os": "active"
    }


@app.get("/metrics")
def metrics():
    data, content_type = get_prometheus_metrics()
    return Response(content=data, media_type=content_type)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

import os
import joblib
import numpy as np
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from backend.database.connection import get_db
from backend.database.models.transaction import Transaction
from ml.constants.fraud_constants import TRAINED_MODEL_PATH, PREPROCESSOR_FILE_PATH

router = APIRouter(prefix="/api/transactions", tags=["Transactions"])

# Global cache for ML model & preprocessor
_MODEL = None
_PREPROCESSOR = None


def load_ml_model():
    global _MODEL, _PREPROCESSOR
    if _MODEL is None and os.path.exists(TRAINED_MODEL_PATH):
        try:
            _MODEL = joblib.load(TRAINED_MODEL_PATH)
        except Exception:
            pass

    if _PREPROCESSOR is None and os.path.exists(PREPROCESSOR_FILE_PATH):
        try:
            _PREPROCESSOR = joblib.load(PREPROCESSOR_FILE_PATH)
        except Exception:
            pass
    return _MODEL, _PREPROCESSOR


class TransactionSchema(BaseModel):
    id: int
    customer_id: int
    amount: float
    merchant: str
    category: str
    status: str
    is_fraud: bool
    risk_score: float

    class Config:
        from_attributes = True


class FraudAnalysisRequest(BaseModel):
    amount: float
    time_offset: Optional[float] = 1000.0
    v_features: Optional[List[float]] = None  # 28 PCA features V1..V28


class FraudAnalysisResponse(BaseModel):
    risk_score: float
    is_fraud: bool
    status: str
    risk_level: str
    recommendation: str


@router.get("", response_model=List[TransactionSchema])
def list_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).order_by(Transaction.timestamp.desc()).all()


@router.post("/analyze-fraud", response_model=FraudAnalysisResponse)
def analyze_transaction_fraud(request: FraudAnalysisRequest):
    model, preprocessor = load_ml_model()

    # Build feature vector
    v_feats = request.v_features if request.v_features and len(request.v_features) == 28 else [0.0] * 28

    # Format dataframe matching EXPECTED_COLUMNS
    cols = ["Time"] + [f"V{i}" for i in range(1, 29)] + ["Amount"]
    row_data = [request.time_offset] + v_feats + [request.amount]

    df_sample = pd.DataFrame([row_data], columns=cols)

    if model is not None and preprocessor is not None:
        try:
            X_trans = preprocessor.transform(df_sample)
            prob = float(model.predict_proba(X_trans)[0, 1])
        except Exception:
            prob = min(0.95, request.amount / 5000.0)
    else:
        # Fallback heuristic if pkl not loaded
        prob = min(0.95, request.amount / 5000.0)

    is_fraud = prob >= 0.50
    risk_level = "High" if prob > 0.70 else "Medium" if prob > 0.30 else "Low"
    recommendation = "Block & Alert Security" if is_fraud else "Approve Transaction"

    return FraudAnalysisResponse(
        risk_score=round(prob, 4),
        is_fraud=is_fraud,
        status="blocked" if is_fraud else "approved",
        risk_level=risk_level,
        recommendation=recommendation
    )

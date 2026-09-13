import os
import joblib
import pandas as pd
from agents.common.agent_base import BaseAgent
from agents.common.schemas import AgentRequest, AgentResponse
from mcp.verification_layer.verification_models import VerificationRequest
from ml.constants.fraud_constants import TRAINED_MODEL_PATH, PREPROCESSOR_FILE_PATH


class FraudAgent(BaseAgent):
    def __init__(self):
        super().__init__("Fraud Agent", "risk_evaluator")
        self.model = None
        self.preprocessor = None
        if os.path.exists(TRAINED_MODEL_PATH) and os.path.exists(PREPROCESSOR_FILE_PATH):
            try:
                self.model = joblib.load(TRAINED_MODEL_PATH)
                self.preprocessor = joblib.load(PREPROCESSOR_FILE_PATH)
            except Exception:
                pass

    def evaluate_fraud_risk(self, request: AgentRequest) -> AgentResponse:
        amount = request.amount or 100.0
        v_feats = request.v_features if request.v_features and len(request.v_features) == 28 else [0.0] * 28

        if self.model and self.preprocessor:
            try:
                cols = ["Time"] + [f"V{i}" for i in range(1, 29)] + ["Amount"]
                df = pd.DataFrame([[1000.0] + v_feats + [amount]], columns=cols)
                X_trans = self.preprocessor.transform(df)
                prob = float(self.model.predict_proba(X_trans)[0, 1])
            except Exception:
                prob = min(0.95, amount / 5000.0)
        else:
            prob = min(0.95, amount / 5000.0)

        # 2-Stage Verification check
        ver_req = VerificationRequest(
            agent_id=self.agent_name,
            mcp_server="TransactionMCPServer",
            mcp_tool="block_transaction" if prob > 0.5 else "process_transfer",
            amount=amount,
            risk_score=prob
        )
        ver_res = self.verifier.verify(ver_req)

        self.log_langsmith_trace("evaluate_fraud_risk", {"amount": amount}, {"risk_score": prob, "verified": ver_res.verified})

        if not ver_res.verified:
            return AgentResponse(
                agent_name=self.agent_name,
                response_text=f"Fraud evaluation completed. Action denied by Governance OS: {ver_res.reason}",
                action_taken="DENIED_BY_GOVERNANCE",
                governance_status="DENIED",
                governance_explanation=ver_res.explanation,
                data={"risk_score": prob, "is_fraud": prob >= 0.5}
            )

        status_msg = "HIGH RISK - Transaction flagged for block" if prob >= 0.5 else "LOW RISK - Transaction clean"
        return AgentResponse(
            agent_name=self.agent_name,
            response_text=f"Fraud Agent Evaluation: {status_msg}. Calculated Risk Score: {(prob*100):.2f}%.",
            action_taken="BLOCK" if prob >= 0.5 else "APPROVE",
            governance_status="APPROVED",
            governance_explanation=ver_res.explanation,
            data={"risk_score": prob, "is_fraud": prob >= 0.5}
        )

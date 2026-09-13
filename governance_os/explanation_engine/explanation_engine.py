class ExplanationEngine:
    """Decision explanation generator."""
    def generate_explanation(self, action: str, allowed: bool, reason: str, risk_score: float) -> str:
        status_text = "APPROVED" if allowed else "DENIED"
        return f"[Governance Explanation] Action '{action}' was {status_text}. Reason: {reason} (Evaluated Risk Score: {risk_score:.4f})"

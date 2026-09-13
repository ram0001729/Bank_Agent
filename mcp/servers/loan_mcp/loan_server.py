from typing import Dict, Any


class LoanMCPServer:
    def approve_loan_application(self, customer_id: int, amount: float) -> Dict[str, Any]:
        return {
            "status": "APPROVED",
            "loan_id": f"LN-{customer_id}-992",
            "amount": amount,
            "interest_rate": 7.5,
            "term_months": 12
        }

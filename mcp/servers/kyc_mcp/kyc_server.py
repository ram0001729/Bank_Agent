from typing import Dict, Any


class KYCMCPServer:
    def verify_kyc_status(self, customer_id: int) -> Dict[str, Any]:
        return {
            "customer_id": customer_id,
            "kyc_status": "VERIFIED",
            "identity_score": 0.99,
            "sanctions_check": "PASSED"
        }

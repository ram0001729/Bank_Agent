from typing import Dict, Any


class CustomerMCPServer:
    def get_customer_profile(self, customer_id: int) -> Dict[str, Any]:
        return {
            "customer_id": customer_id,
            "name": "Alice Johnson",
            "email": "alice@example.com",
            "account_number": "ACC-100982",
            "balance": 14250.50,
            "status": "active",
            "risk_level": "low"
        }

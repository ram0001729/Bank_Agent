from typing import Dict, Any


class TransactionMCPServer:
    def process_refund(self, transaction_id: int, amount: float) -> Dict[str, Any]:
        return {
            "status": "REFUNDED",
            "transaction_id": transaction_id,
            "refund_amount": amount,
            "provisional_credit": True
        }

    def block_transaction(self, transaction_id: int, reason: str) -> Dict[str, Any]:
        return {
            "status": "BLOCKED",
            "transaction_id": transaction_id,
            "reason": reason
        }

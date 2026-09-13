from typing import Any

from mcp.servers.base_server import (
    BaseMCPServer,
)


class TransactionMCPServer(
    BaseMCPServer
):

    @property
    def server_name(
        self,
    ) -> str:

        return "transaction-mcp"

    def list_tools(
        self,
    ) -> list[str]:

        return [
            "get_transaction",
            "list_transactions",
            "get_transaction_status",
            "initiate_transfer",
            "approve_transfer",
            "cancel_transfer",
        ]

    def execute(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> Any:

        if tool_name == "get_transaction":

            return self.get_transaction(
                arguments
            )

        if tool_name == "list_transactions":

            return self.list_transactions(
                arguments
            )

        if tool_name == "get_transaction_status":

            return self.get_transaction_status(
                arguments
            )

        if tool_name == "initiate_transfer":

            return self.initiate_transfer(
                arguments
            )

        if tool_name == "approve_transfer":

            return self.approve_transfer(
                arguments
            )

        if tool_name == "cancel_transfer":

            return self.cancel_transfer(
                arguments
            )

        raise ValueError(
            f"Unknown transaction tool: "
            f"{tool_name}"
        )

    # ========================================================
    # GET TRANSACTION
    # ========================================================

    def get_transaction(
        self,
        arguments: dict[str, Any],
    ) -> dict:

        transaction_id = arguments.get(
            "transaction_id"
        )

        if not transaction_id:

            raise ValueError(
                "transaction_id is required."
            )

        return {
            "transaction_id": transaction_id,
            "status": "completed",
        }

    # ========================================================
    # LIST TRANSACTIONS
    # ========================================================

    def list_transactions(
        self,
        arguments: dict[str, Any],
    ) -> dict:

        account_id = arguments.get(
            "account_id"
        )

        if not account_id:

            raise ValueError(
                "account_id is required."
            )

        return {
            "account_id": account_id,

            "transactions": [
                {
                    "transaction_id": "TXN-001",
                    "type": "debit",
                    "amount": 1000,
                    "currency": "INR",
                },
                {
                    "transaction_id": "TXN-002",
                    "type": "credit",
                    "amount": 5000,
                    "currency": "INR",
                },
            ],
        }

    # ========================================================
    # STATUS
    # ========================================================

    def get_transaction_status(
        self,
        arguments: dict[str, Any],
    ) -> dict:

        transaction_id = arguments.get(
            "transaction_id"
        )

        if not transaction_id:

            raise ValueError(
                "transaction_id is required."
            )

        return {
            "transaction_id": transaction_id,
            "status": "completed",
        }

    # ========================================================
    # INITIATE TRANSFER
    # ========================================================

    def initiate_transfer(
        self,
        arguments: dict[str, Any],
    ) -> dict:

        source_account = arguments.get(
            "source_account"
        )

        destination_account = arguments.get(
            "destination_account"
        )

        amount = arguments.get(
            "amount"
        )

        if not source_account:

            raise ValueError(
                "source_account is required."
            )

        if not destination_account:

            raise ValueError(
                "destination_account is required."
            )

        if amount is None:

            raise ValueError(
                "amount is required."
            )

        if amount <= 0:

            raise ValueError(
                "amount must be greater than zero."
            )

        return {
            "transaction_id": "TXN-NEW-001",

            "status": "initiated",

            "source_account": (
                source_account
            ),

            "destination_account": (
                destination_account
            ),

            "amount": amount,

            "currency": "INR",
        }

    # ========================================================
    # APPROVE TRANSFER
    # ========================================================

    def approve_transfer(
        self,
        arguments: dict[str, Any],
    ) -> dict:

        transaction_id = arguments.get(
            "transaction_id"
        )

        if not transaction_id:

            raise ValueError(
                "transaction_id is required."
            )

        return {
            "transaction_id": transaction_id,
            "status": "approved",
        }

    # ========================================================
    # CANCEL TRANSFER
    # ========================================================

    def cancel_transfer(
        self,
        arguments: dict[str, Any],
    ) -> dict:

        transaction_id = arguments.get(
            "transaction_id"
        )

        if not transaction_id:

            raise ValueError(
                "transaction_id is required."
            )

        return {
            "transaction_id": transaction_id,
            "status": "cancelled",
        }
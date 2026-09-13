from typing import Any

from mcp.servers.base_server import (
    BaseMCPServer,
)


class LoanMCPServer(
    BaseMCPServer
):

    @property
    def server_name(
        self,
    ) -> str:

        return "loan-mcp"

    def list_tools(
        self,
    ) -> list[str]:

        return [
            "get_loan",
            "create_loan",
            "approve_loan",
            "reject_loan",
        ]

    def execute(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> Any:

        if tool_name == "get_loan":

            return self.get_loan(
                arguments
            )

        if tool_name == "create_loan":

            return self.create_loan(
                arguments
            )

        if tool_name == "approve_loan":

            return self.approve_loan(
                arguments
            )

        if tool_name == "reject_loan":

            return self.reject_loan(
                arguments
            )

        raise ValueError(
            f"Unknown loan tool: "
            f"{tool_name}"
        )

    def get_loan(
        self,
        arguments: dict[str, Any],
    ):

        loan_id = arguments.get(
            "loan_id"
        )

        return {
            "loan_id": loan_id,
            "status": "pending",
        }

    def create_loan(
        self,
        arguments: dict[str, Any],
    ):

        return {
            "status": "created",
            "loan_id": "LOAN-001",
        }

    def approve_loan(
        self,
        arguments: dict[str, Any],
    ):

        return {
            "status": "approved",
            "loan_id": arguments.get(
                "loan_id"
            ),
        }

    def reject_loan(
        self,
        arguments: dict[str, Any],
    ):

        return {
            "status": "rejected",
            "loan_id": arguments.get(
                "loan_id"
            ),
        }
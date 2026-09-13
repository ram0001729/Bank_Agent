from mcp.client.mcp_server_registry import (
    MCPServerRegistry,
)

from mcp.servers.customer.customer_server import (
    CustomerMCPServer,
)

from mcp.servers.kyc.kyc_server import (
    KYCMCPServer,
)

from mcp.servers.loan.loan_server import (
    LoanMCPServer,
)

from mcp.servers.transaction.transaction_server import (
    TransactionMCPServer,
)


def create_mcp_server_registry():

    registry = MCPServerRegistry()

    registry.register(
        "customer-mcp",
        CustomerMCPServer(),
    )

    registry.register(
        "kyc-mcp",
        KYCMCPServer(),
    )

    registry.register(
        "loan-mcp",
        LoanMCPServer(),
    )

    registry.register(
        "transaction-mcp",
        TransactionMCPServer(),
    )

    return registry
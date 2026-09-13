class MCPError(Exception):
    pass


class MCPServerNotFoundError(
    MCPError
):
    pass


class MCPToolNotFoundError(
    MCPError
):
    pass


class MCPVerificationError(
    MCPError
):
    pass


class MCPExecutionError(
    MCPError
):
    pass
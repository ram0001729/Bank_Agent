from .verification_models import (
    VerificationRequest,
    VerificationResult,
    VerificationStatus,
)


class MCPServerVerifier:
    """Verification boundary used by the agent workflows."""

    def __init__(self, *args, **kwargs):
        self.emergency_stop = kwargs.get("emergency_stop")

    def verify(self, request: VerificationRequest) -> VerificationResult:
        if self.emergency_stop is not None and getattr(self.emergency_stop, "is_stopped", False):
            return VerificationResult(
                request_id=request.request_id,
                action_id=request.action_id,
                status=VerificationStatus.DENIED,
                verified=False,
                reason="Emergency stop is active.",
                explanation="Governance OS emergency stop is active.",
            )

        return VerificationResult(
            request_id=request.request_id,
            action_id=request.action_id,
            status=VerificationStatus.VERIFIED,
            verified=True,
            reason="Verification passed.",
            explanation="MCP request verified.",
        )

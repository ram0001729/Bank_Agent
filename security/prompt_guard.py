import re
from typing import Tuple


class PromptInjectionGuard:
    """Input Sanitizer and Prompt Injection Guardrail for LLM Agents."""
    INJECTION_PATTERNS = [
        r"ignore previous instructions",
        r"system prompt",
        r"bypass governance",
        r"override safety",
        r"drop database",
        r"grant admin access",
        r"reveal secret key"
    ]

    @classmethod
    def sanitize_and_validate(cls, user_input: str) -> Tuple[bool, str, str]:
        input_lower = user_input.lower()
        for pattern in cls.INJECTION_PATTERNS:
            if re.search(pattern, input_lower):
                return False, f"SECURITY_BLOCKED: Input contained malicious prompt injection pattern '{pattern}'", ""

        # Sanitize HTML / Script tags
        sanitized = re.sub(r'<[^>]*>', '', user_input)
        return True, "Input validation passed", sanitized

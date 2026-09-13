from collections import defaultdict, deque
from threading import Lock


class LoanConversationMemory:

    def __init__(
        self,
        max_messages: int = 20
    ):

        if max_messages <= 0:
            raise ValueError(
                "max_messages must be greater than zero"
            )

        self._memory = defaultdict(
            lambda: deque(
                maxlen=max_messages
            )
        )

        self._lock = Lock()

    def add(
        self,
        session_id: str,
        role: str,
        content: str
    ) -> None:

        if not session_id:
            raise ValueError(
                "session_id is required"
            )

        if not content:
            raise ValueError(
                "content is required"
            )

        with self._lock:

            self._memory[session_id].append(
                {
                    "role": role,
                    "content": content
                }
            )

    def get(
        self,
        session_id: str
    ) -> list[dict[str, str]]:

        with self._lock:

            return list(
                self._memory.get(
                    session_id,
                    []
                )
            )

    def clear(
        self,
        session_id: str
    ) -> None:

        with self._lock:

            self._memory.pop(
                session_id,
                None
            )
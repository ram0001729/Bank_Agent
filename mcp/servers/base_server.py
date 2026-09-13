from abc import ABC, abstractmethod
from typing import Any


class BaseMCPServer(
    ABC
):

    @property
    @abstractmethod
    def server_name(self) -> str:
        pass

    @abstractmethod
    def execute(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> Any:
        pass

    @abstractmethod
    def list_tools(self) -> list[str]:
        pass
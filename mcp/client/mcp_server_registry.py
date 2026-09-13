import sys
from threading import RLock
from typing import Any

from ml.utils.exception import MyException
from ml.utils.logger import logger


class MCPServerRegistry:

    def __init__(self):

        self._servers: dict[
            str,
            Any
        ] = {}

        self._lock = RLock()

        logger.info(
            "MCP server registry initialized"
        )

    # ========================================================
    # REGISTER
    # ========================================================

    def register(
        self,
        server_name: str,
        server: Any,
    ) -> None:

        try:

            with self._lock:

                if server_name in self._servers:

                    raise ValueError(
                        f"MCP server already registered: "
                        f"{server_name}"
                    )

                self._servers[
                    server_name
                ] = server

                logger.info(
                    f"MCP server registered: "
                    f"{server_name}"
                )

        except ValueError:

            raise

        except Exception as e:

            logger.exception(
                "Failed to register MCP server"
            )

            raise MyException(
                e,
                sys
            ) from e

    # ========================================================
    # GET
    # ========================================================

    def get(
        self,
        server_name: str,
    ):

        with self._lock:

            server = self._servers.get(
                server_name
            )

            if server is None:

                raise ValueError(
                    f"MCP server not found: "
                    f"{server_name}"
                )

            return server

    # ========================================================
    # EXISTS
    # ========================================================

    def exists(
        self,
        server_name: str,
    ) -> bool:

        with self._lock:

            return (
                server_name
                in self._servers
            )

    # ========================================================
    # LIST
    # ========================================================

    def list_servers(
        self,
    ) -> list[str]:

        with self._lock:

            return list(
                self._servers.keys()
            )
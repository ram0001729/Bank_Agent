import sys
from threading import RLock
from uuid import UUID

from governance.registry.agent_identity import (
    AgentIdentity,
)

from ml.utils.exception import MyException
from ml.utils.logger import logger


class AgentAlreadyRegisteredError(
    Exception
):
    pass


class AgentNotFoundError(
    Exception
):
    pass


class AgentRegistry:

    def __init__(self):

        self._agents: dict[
            UUID,
            AgentIdentity
        ] = {}

        self._lock = RLock()

        logger.info(
            "Agent registry initialized"
        )

    def register(
        self,
        identity: AgentIdentity
    ) -> AgentIdentity:

        try:

            with self._lock:

                if identity.agent_id in self._agents:

                    raise AgentAlreadyRegisteredError(
                        f"Agent already registered: "
                        f"{identity.agent_id}"
                    )

                self._agents[
                    identity.agent_id
                ] = identity

                logger.info(
                    f"Agent registered: "
                    f"name={identity.name}, "
                    f"id={identity.agent_id}, "
                    f"version={identity.version}"
                )

                return identity

        except AgentAlreadyRegisteredError:
            raise

        except Exception as e:

            logger.exception(
                "Failed to register agent"
            )

            raise MyException(
                e,
                sys
            ) from e

    def unregister(
        self,
        agent_id: UUID
    ) -> None:

        try:

            with self._lock:

                if agent_id not in self._agents:

                    raise AgentNotFoundError(
                        f"Agent not found: "
                        f"{agent_id}"
                    )

                identity = self._agents.pop(
                    agent_id
                )

                logger.info(
                    f"Agent unregistered: "
                    f"name={identity.name}, "
                    f"id={identity.agent_id}"
                )

        except AgentNotFoundError:
            raise

        except Exception as e:

            logger.exception(
                "Failed to unregister agent"
            )

            raise MyException(
                e,
                sys
            ) from e

    def get(
        self,
        agent_id: UUID
    ) -> AgentIdentity:

        try:

            with self._lock:

                identity = self._agents.get(
                    agent_id
                )

                if identity is None:

                    raise AgentNotFoundError(
                        f"Agent not found: "
                        f"{agent_id}"
                    )

                return identity

        except AgentNotFoundError:
            raise

        except Exception as e:

            logger.exception(
                "Failed to retrieve agent"
            )

            raise MyException(
                e,
                sys
            ) from e

    def get_by_name(
        self,
        name: str
    ) -> AgentIdentity:

        try:

            with self._lock:

                for identity in self._agents.values():

                    if identity.name == name:

                        return identity

                raise AgentNotFoundError(
                    f"Agent not found: {name}"
                )

        except AgentNotFoundError:
            raise

        except Exception as e:

            logger.exception(
                "Failed to find agent by name"
            )

            raise MyException(
                e,
                sys
            ) from e

    def list_agents(
        self
    ) -> list[AgentIdentity]:

        with self._lock:

            return list(
                self._agents.values()
            )

    def exists(
        self,
        agent_id: UUID
    ) -> bool:

        with self._lock:

            return agent_id in self._agents

    def count(self) -> int:

        with self._lock:

            return len(
                self._agents
            )
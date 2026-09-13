from typing import Set


class RevocationStore:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RevocationStore, cls).__new__(cls)
            cls._instance.revoked_agents: Set[str] = set()
        return cls._instance

    def revoke_agent(self, agent_name: str):
        self.revoked_agents.add(agent_name)

    def unrevoke_agent(self, agent_name: str):
        self.revoked_agents.discard(agent_name)

    def is_revoked(self, agent_name: str) -> bool:
        return agent_name in self.revoked_agents

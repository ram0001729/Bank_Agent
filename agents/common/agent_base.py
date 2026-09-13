import os
from typing import Dict, Any
from mcp.client.mcp_execution_gateway import MCPExecutionGateway
from mcp.verification_layer.mcp_verifier import MCPServerVerifier
from ml.utils.logger import logging

# Configure LangSmith Environment Variables for Automated Tracing
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2", "true")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "AI-Banking-Agent-Platform")
os.environ["LANGCHAIN_ENDPOINT"] = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")


class BaseAgent:
    def __init__(self, agent_name: str, role: str):
        self.agent_name = agent_name
        self.role = role
        self.verifier = MCPServerVerifier()
        logging.info(f"Initialized {self.agent_name} ({self.role}) with LangSmith tracing enabled.")

    def log_langsmith_trace(self, action: str, inputs: Dict[str, Any], outputs: Dict[str, Any]):
        logging.info(f"[LangSmith Trace] Project: {os.environ.get('LANGCHAIN_PROJECT')} | Agent: {self.agent_name} | Action: {action}")

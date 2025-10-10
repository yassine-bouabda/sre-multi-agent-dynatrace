"""
Problem Finder Agent - Health check and debug
Role: Scans for and triages active incidents. Focus on Problem Discovery
"""
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.mcp import load_mcp_servers
from config import PROBLEM_FINDER_AGENT_MODEL, MCP_CONFIG_FILE
from utils import load_prompt

servers = load_mcp_servers(MCP_CONFIG_FILE)

class ProblemFinderResponse(BaseModel):
    """Structured output for problem findings"""
    summary: str
    current_problems: list[str] = Field(default_factory=list)
    affected_services: list[str] = Field(default_factory=list)
    severity: str = "UNKNOWN"


class Failed(BaseModel):
    """Unable to find problems or analyze"""
    reason: str


# Agent with structured output
problem_finder_agent = Agent[None, ProblemFinderResponse | Failed](
    PROBLEM_FINDER_AGENT_MODEL,
    output_type=ProblemFinderResponse | Failed,
    system_prompt=load_prompt('problem_finder_prompt.txt'),
    toolsets=servers,
)


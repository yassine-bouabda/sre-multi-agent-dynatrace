"""
Root Cause Analyst - Deep dive and cross sources correlations
Role: The deep-dive investigator
Expertise: Correlation and deep dive
"""
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.mcp import load_mcp_servers
from config import ROOT_CAUSE_AGENT_MODEL, MCP_CONFIG_FILE
from utils import load_prompt

servers = load_mcp_servers(MCP_CONFIG_FILE)

class RootCauseResponse(BaseModel):
    """Structured output for root cause analysis"""
    summary: str
    exception_message: str = ""
    stack_trace: str = ""
    correlated_logs: list[str] = Field(default_factory=list)
    root_cause: str = ""


class Failed(BaseModel):
    """Unable to determine root cause"""
    reason: str


# Agent with structured output
root_cause_agent = Agent[None, RootCauseResponse | Failed](
    ROOT_CAUSE_AGENT_MODEL,
    output_type=RootCauseResponse | Failed,
    system_prompt=load_prompt('root_cause_agent_prompt.txt'),
    toolsets=servers,
)


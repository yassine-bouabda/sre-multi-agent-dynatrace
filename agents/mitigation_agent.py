"""
Mitigation Agent - Synthesize and provide actionable plan
Role: Synthesize the Conclusion and provide an actionnable plan
"""
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from config import MITIGATION_AGENT_MODEL
from utils import load_prompt


class MitigationResponse(BaseModel):
    """Structured output for mitigation plan"""
    summary: str
    findings_synthesis: str
    immediate_actions: list[str] = Field(default_factory=list)
    automation_triggers: list[str] = Field(default_factory=list)
    long_term_fixes: list[str] = Field(default_factory=list)
    prevention_measures: list[str] = Field(default_factory=list)


class Failed(BaseModel):
    """Unable to create mitigation plan"""
    reason: str


class AgentFindings(BaseModel):
    """Context data from other agents"""
    problem_summary: str = ""
    vulnerability_summary: str = ""
    root_cause_summary: str = ""


# Agent with dependencies (receives findings from other agents)
mitigation_agent = Agent[AgentFindings, MitigationResponse | Failed](
    MITIGATION_AGENT_MODEL,
    output_type=MitigationResponse | Failed,
    system_prompt=load_prompt('mitigation_agent_prompt.txt'),
)


"""
Orchestrator Agent - Understand, Plan and Delegate
Role: Deconstructs a user's goal into an actionable investigation plan
The orchestrator is itself an LLM agent that decides which specialist agents to call
"""
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from config import ORCHESTRATOR_AGENT_MODEL, REQUEST_LIMIT
from utils import load_prompt
from agents.problem_finder_agent import problem_finder_agent, ProblemFinderResponse
from agents.vulnerability_agent import vulnerability_agent, VulnerabilityResponse
from agents.root_cause_agent import root_cause_agent, RootCauseResponse
from agents.mitigation_agent import mitigation_agent, MitigationResponse, AgentFindings


class OrchestratorResponse(BaseModel):
    """Final orchestrated response"""
    summary: str
    findings: dict = Field(default_factory=dict)
    recommendations: list[str] = Field(default_factory=list)
    requires_human_feedback: bool = False
    feedback_question: str = ""


class Failed(BaseModel):
    """Unable to orchestrate"""
    reason: str


class OrchestratorContext(BaseModel):
    """Context maintained by orchestrator"""
    problem_findings: str = ""
    vulnerability_findings: str = ""
    root_cause_findings: str = ""
    user_feedback: str = ""


# The Orchestrator is itself a Pydantic AI Agent!
orchestrator_agent = Agent[OrchestratorContext, OrchestratorResponse | Failed](
    ORCHESTRATOR_AGENT_MODEL,
    output_type=OrchestratorResponse | Failed,
    system_prompt=load_prompt('orchestrator_prompt.txt'),
)


@orchestrator_agent.tool
async def run_problem_finder(ctx: RunContext[OrchestratorContext], user_query: str) -> dict:
    """
    Scan for active incidents and health issues.
    Use this to identify DAVIS_PROBLEM events and affected services.
    
    Args:
        user_query: The user's question or request
    """
    print("🧭 Problem Finder: scanning for active incidents...")
    result = await problem_finder_agent.run(user_query)
    
    if isinstance(result.output, ProblemFinderResponse):
        ctx.deps.problem_findings = result.output.summary
        return {
            "success": True,
            "summary": result.output.summary,
            "problems": result.output.current_problems,
            "services": result.output.affected_services,
            "severity": result.output.severity
        }
    else:
        return {
            "success": False,
            "reason": result.output.reason
        }


@orchestrator_agent.tool
async def run_vulnerability_scanner(ctx: RunContext[OrchestratorContext], user_query: str) -> dict:
    """
    Hunt for security vulnerabilities and compliance issues.
    Queries security.events table for CVEs and risk scores.
    Can run in parallel with problem_finder.
    
    Args:
        user_query: The user's question or request
    """
    print("🛡️ Vulnerability Scanner: hunting for security issues...")
    result = await vulnerability_agent.run(user_query)
    
    if isinstance(result.output, VulnerabilityResponse):
        ctx.deps.vulnerability_findings = result.output.summary
        return {
            "success": True,
            "summary": result.output.summary,
            "vulnerabilities": result.output.vulnerabilities,
            "affected_entities": result.output.affected_entities,
            "risk_score": result.output.risk_score,
            "compliance_rules": result.output.compliance_rules
        }
    else:
        return {
            "success": False,
            "reason": result.output.reason
        }


@orchestrator_agent.tool
async def run_root_cause_analyst(ctx: RunContext[OrchestratorContext], user_query: str) -> dict:
    """
    Deep dive investigation to find WHY a problem occurred.
    Uses Exception-First workflow: queries spans for exceptions, correlates with logs.
    Should be called AFTER problem_finder identifies issues.
    
    Args:
        user_query: The user's question or request
    """
    print("🔎 Root Cause Analyst: deep-diving for causality...")
    result = await root_cause_agent.run(user_query)
    
    if isinstance(result.output, RootCauseResponse):
        ctx.deps.root_cause_findings = result.output.summary
        return {
            "success": True,
            "summary": result.output.summary,
            "exception": result.output.exception_message,
            "stack_trace": result.output.stack_trace,
            "root_cause": result.output.root_cause,
            "correlated_logs": result.output.correlated_logs
        }
    else:
        return {
            "success": False,
            "reason": result.output.reason
        }


@orchestrator_agent.tool
async def run_mitigation_planner(ctx: RunContext[OrchestratorContext], user_query: str) -> dict:
    """
    Create actionable mitigation plan based on all findings.
    Synthesizes results from other agents and provides immediate actions and long-term fixes.
    Should be called LAST, after other agents have gathered information.
    
    Args:
        user_query: The user's question or request
    """
    # Pass findings from other agents as context
    agent_findings = AgentFindings(
        problem_summary=ctx.deps.problem_findings,
        vulnerability_summary=ctx.deps.vulnerability_findings,
        root_cause_summary=ctx.deps.root_cause_findings
    )
    
    print("🧰 Mitigation Planner: composing actionable steps...")
    result = await mitigation_agent.run(user_query, deps=agent_findings)
    
    if isinstance(result.output, MitigationResponse):
        return {
            "success": True,
            "summary": result.output.summary,
            "synthesis": result.output.findings_synthesis,
            "immediate_actions": result.output.immediate_actions,
            "automation_triggers": result.output.automation_triggers,
            "long_term_fixes": result.output.long_term_fixes,
            "prevention_measures": result.output.prevention_measures
        }
    else:
        return {
            "success": False,
            "reason": result.output.reason
        }


@orchestrator_agent.tool
async def request_user_feedback(
    ctx: RunContext[OrchestratorContext], 
    question: str
) -> dict:
    """
    Request clarification or additional information from the user.
    Use this when you need more context before running expensive queries.
    
    Args:
        question: The question to ask the user
    """
    # This will signal that human feedback is needed
    return {
        "feedback_needed": True,
        "question": question,
        "message": "Waiting for user response..."
    }


async def orchestrate(user_input: str, context: OrchestratorContext = None) -> str:
    """
    Main orchestration function - runs the orchestrator agent.
    The orchestrator agent will decide which specialist agents to call.
    
    Args:
        user_input: User's query or request
        context: Optional context from previous interactions
    
    Returns:
        Formatted response string
    """
    if context is None:
        context = OrchestratorContext()
    
    # Run the orchestrator agent - it will decide what to do!
    result = await orchestrator_agent.run(
        user_input,
        deps=context
    )
    
    # Format the response
    if isinstance(result.output, OrchestratorResponse):
        lines = []
        lines.append("=" * 70)
        lines.append("🎯 ORCHESTRATOR ANALYSIS")
        lines.append("=" * 70)
        lines.append(f"\n📋 {result.output.summary}\n")
        
        if result.output.findings:
            lines.append("📊 FINDINGS:")
            for key, value in result.output.findings.items():
                lines.append(f"   • {key}: {value}")
            lines.append("")
        
        if result.output.recommendations:
            lines.append("💡 RECOMMENDATIONS:")
            for rec in result.output.recommendations:
                lines.append(f"   • {rec}")
            lines.append("")
        
        if result.output.requires_human_feedback:
            lines.append("❓ FEEDBACK NEEDED:")
            lines.append(f"   {result.output.feedback_question}")
            lines.append("")
        
        # Add token usage info
        usage = result.usage()
        lines.append(f"📈 Usage: {usage.total_tokens} tokens")
        lines.append("=" * 70)
        
        return "\n".join(lines)
    else:
        return f"❌ Orchestration failed: {result.output.reason}"
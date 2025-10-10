"""
Configuration for multi-agent system
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Model configurations for each agent
ORCHESTRATOR_AGENT_MODEL = "openai:gpt-4o"
PROBLEM_FINDER_AGENT_MODEL = "openai:gpt-4o-mini"
VULNERABILITY_AGENT_MODEL = "openai:gpt-4o-mini"
ROOT_CAUSE_AGENT_MODEL = "openai:gpt-4o-mini"
MITIGATION_AGENT_MODEL = "openai:gpt-4o-mini"

# Dynatrace Configuration from environment variables
DT_ENVIRONMENT = os.getenv("DT_ENVIRONMENT")
DT_PLATFORM_TOKEN = os.getenv("DT_PLATFORM_TOKEN")
OAUTH_CLIENT_ID = os.getenv("OAUTH_CLIENT_ID")
OAUTH_CLIENT_SECRET = os.getenv("OAUTH_CLIENT_SECRET")

# MCP Configuration
MCP_CONFIG_FILE = "dynatrace_mcp_config.json"

# Usage limits
REQUEST_LIMIT = 20

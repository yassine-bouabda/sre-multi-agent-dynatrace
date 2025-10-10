# Dynatrace Multi-Agent System with Pydantic AI

Intelligent multi-agent system for Dynatrace monitoring, security, and incident response.

## 🏗️ Architecture

The system uses an **LLM Orchestrator** that intelligently decides which specialist agents to call:

- **Orchestrator Agent** (LLM) - Decides which agents to call based on user intent
  - **Problem Finder Agent** - Health check and incident detection
  - **Vulnerability Agent** - Security scanning and compliance
  - **Root Cause Agent** - Deep dive investigation with Exception-First workflow
  - **Mitigation Agent** - Actionable plans with immediate and long-term fixes

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Models
```bash
# Copy example config
cp config.example.py config.py

# Edit config.py to set your preferred models
# Default: OpenAI GPT-4o for orchestrator, GPT-4o-mini for agents
```

### 3. Set API Key
```bash
export OPENAI_API_KEY="sk-your-key-here"
# or
export ANTHROPIC_API_KEY="your-key-here"
```

### 4. Configure MCP (Optional)
```bash
# Create dynatrace_mcp_config.json with your Dynatrace MCP settings
# See agents/dynatrace_mcp_config.json for example
```

### 5. Run
```bash
# Interactive chat
python main.py

# Run demo
python demo.py
```

## 📁 Project Structure

```
dynatrace/
├── config.py                     # Model configurations (created from config.example.py)
├── config.example.py             # Example configuration
├── main.py                       # Chat interface
├── demo.py                       # Demo with example queries
├── orchestrator.py               # Orchestrator Agent (LLM)
├── moderator.py                  # Pass-through
├── memory_updater.py             # Pass-through
├── utils.py                      # Helper functions (load prompts)
├── agents/
│   ├── problem_finder_agent.py  # Health check agent
│   ├── vulnerability_agent.py   # Security scanner agent
│   ├── root_cause_agent.py      # Deep investigation agent
│   └── mitigation_agent.py      # Action plan agent
└── instructions/
    ├── orchestrator_prompt.txt
    ├── problem_finder_prompt.txt
    ├── vulnerability_agent_prompt.txt
    ├── root_cause_agent_prompt.txt
    └── mitigation_agent_prompt.txt
```

## 🎯 Key Features

✅ **Intelligent Orchestration** - LLM decides which agents to call  
✅ **Structured Output** - Pydantic models for all responses  
✅ **MCP Integration** - Direct connection to Dynatrace tools  
✅ **Configurable Models** - Easy to swap AI models via config.py  
✅ **External Prompts** - All system prompts in instructions/ folder  
✅ **Minimal & Clean** - Simple, maintainable codebase  

## 🔧 Configuration

All configuration is centralized in `config.py`:

```python
# Model configurations
ORCHESTRATOR_AGENT_MODEL = "openai:gpt-4o"
PROBLEM_FINDER_AGENT_MODEL = "openai:gpt-4o-mini"
# ... etc

# MCP Configuration
MCP_CONFIG_FILE = "dynatrace_mcp_config.json"

# Usage limits
REQUEST_LIMIT = 20
```

## 💬 Example Usage

```
You: Are there any problems in production?
→ Orchestrator calls: Problem Finder only

You: Check for security vulnerabilities
→ Orchestrator calls: Vulnerability Scanner only

You: Why is the payment service slow? Fix it
→ Orchestrator calls: Problem Finder → Root Cause → Mitigation

You: Full security and health audit
→ Orchestrator calls: All agents in optimal order
```

## 🎨 Design Principles

- **Minimal** - Each component is simple and focused
- **Configurable** - Models and settings in config.py
- **Visible** - System prompts in instructions/ folder
- **Modular** - Each agent is independent
- **Intelligent** - LLM-based orchestration (no hardcoded rules)

## 📚 Documentation

- See `README_ARCHITECTURE.md` for detailed architecture
- See `instructions/README.md` for prompt management

## 🔌 MCP Tools

Agents automatically connect to Dynatrace MCP tools:
- `list_problems` - Query DAVIS_PROBLEM events
- `list_vulnerabilities` - Query security.events
- `execute_dql` - Custom DQL queries
- And more...

Configure MCP in `dynatrace_mcp_config.json`
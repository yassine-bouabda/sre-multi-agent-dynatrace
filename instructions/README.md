# System Prompts

This folder contains all system prompts for the multi-agent system.

## Files

- `orchestrator_prompt.txt` - Orchestrator agent (decides which agents to call)
- `problem_finder_prompt.txt` - Problem Finder agent (health check)
- `vulnerability_agent_prompt.txt` - Vulnerability agent (security scanner)
- `root_cause_agent_prompt.txt` - Root Cause agent (deep investigation)
- `mitigation_agent_prompt.txt` - Mitigation agent (action plans)

## Usage

Prompts are loaded automatically by agents using:
```python
from utils import load_prompt

system_prompt=load_prompt('orchestrator_prompt.txt')
```

## Benefits

✅ Better visibility - All prompts in one place  
✅ Easy to edit - Just modify text files  
✅ Version control - Track prompt changes  
✅ Clean code - No long strings in Python files

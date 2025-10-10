"""
Utility functions for loading system prompts and config
"""
import os
import json
import re
import tempfile
from pathlib import Path
from pydantic_ai.mcp import load_mcp_servers


def load_prompt(filename: str) -> str:
    """Load system prompt from instructions folder"""
    prompt_path = Path(__file__).parent / "instructions" / filename
    return prompt_path.read_text().strip()


def expand_env_vars(text: str) -> str:
    """Expand ${VAR} or $VAR style environment variables in text"""
    def replacer(match):
        var_name = match.group(1) or match.group(2)
        return os.getenv(var_name, match.group(0))
    
    # Match ${VAR} or $VAR
    pattern = r'\$\{([^}]+)\}|\$(\w+)'
    return re.sub(pattern, replacer, text)


def load_mcp_servers_with_env(config_file: str):
    """
    Load MCP servers with environment variable expansion.
    Creates a temporary config file with expanded env vars.
    """
    config_path = Path(__file__).parent / config_file
    
    # Read the config file
    with open(config_path, 'r') as f:
        config_text = f.read()
    
    # Expand environment variables
    expanded_text = expand_env_vars(config_text)
    
    # Create a temporary config file with expanded values
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
        tmp.write(expanded_text)
        tmp_path = tmp.name
    
    try:
        # Load MCP servers from the temporary expanded config
        return load_mcp_servers(tmp_path)
    finally:
        # Clean up the temporary file
        try:
            os.unlink(tmp_path)
        except:
            pass

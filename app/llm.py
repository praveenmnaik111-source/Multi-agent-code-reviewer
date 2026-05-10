"""
LLM initialization and configuration.

Sets up ChatOllama to connect to the local Ollama instance.
All agents share this LLM instance for consistency and efficiency.

Model: qwen2.5-coder:7b (specialized for code generation)
Temperature: 0.2 (low randomness for consistent bug fixes)
"""

import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOllama

# Load environment variables from .env file
load_dotenv()

# Retrieve configuration from environment
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.2"))


def get_llm():
    """
    Initialize and return the LLM instance.
    
    Returns:
        ChatOllama: Configured LLM connected to local Ollama
    
    Note:
        Ensure Ollama is running locally:
        $ ollama serve
        
        Pull the model if not present:
        $ ollama pull qwen2.5-coder:7b
    """
    llm = ChatOllama(
        base_url=OLLAMA_BASE_URL,
        model=OLLAMA_MODEL,
        temperature=LLM_TEMPERATURE,
        num_ctx=4096,  # Context window size for code understanding
    )
    return llm


# Initialize LLM once at module load
llm = get_llm()

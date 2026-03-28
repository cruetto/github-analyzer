"""
NLP Processing Module
=====================
Handles natural language processing tasks:
- LLM initialization and management
- Entity extraction from user queries
- Structured output parsing
"""

import os
from dotenv import load_dotenv, find_dotenv
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

load_dotenv(find_dotenv(), override=True)


class RepoEntity(BaseModel):
    """Pydantic model for repository entity extraction"""
    repo_name: str = Field(description="GitHub repository name extracted from user text")


def get_llm():
    """
    Initialize and return the LLM instance (cached via Streamlit)
    
    Returns:
        ChatGroq: Initialized LLM instance
        
    Raises:
        ValueError: If GROQ_API_KEY is not set
    """
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise ValueError("GROQ_API_KEY not found!")
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=key
    )


def extract_repo(query: str) -> str:
    """
    Extract repository name from natural language query using LLM
    
    Args:
        query: User's natural language query
        
    Returns:
        str: Extracted repository name
    """
    structured_llm = get_llm().with_structured_output(RepoEntity, include_raw=False)
    result = structured_llm.invoke(query)
    
    # Handle both dict and Pydantic object responses
    if isinstance(result, dict):
        return result.get("repo_name", "")
    elif hasattr(result, "repo_name"):
        return result.repo_name  # type: ignore[union-attr]
    return ""
import os
from dotenv import load_dotenv, find_dotenv
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

load_dotenv(find_dotenv(), override=True)


class RepoEntity(BaseModel):
    repo_name: str = Field(description="GitHub repository name extracted from user text")


def get_llm():
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise ValueError("GROQ_API_KEY not found")
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=key
    )


def extract_repo(query: str) -> str:
    structured_llm = get_llm().with_structured_output(RepoEntity, include_raw=False)
    result = structured_llm.invoke(query)
    
    if isinstance(result, dict):
        return result.get("repo_name", "")
    elif hasattr(result, "repo_name"):
        return result.repo_name
    return ""
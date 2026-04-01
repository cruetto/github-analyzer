"""
Pytest Configuration File
==========================
Configuration and fixtures for pytest testing
"""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers",
        "integration: marks tests as integration tests (may be slow)"
    )
    config.addinivalue_line(
        "markers",
        "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )


@pytest.fixture(scope="session")
def github_api_available():
    """Check if GitHub API is available"""
    import requests
    try:
        response = requests.get("https://api.github.com", timeout=5)
        return response.status_code == 200
    except:
        return False


@pytest.fixture(scope="session")
def llm_available():
    """Check if LLM (Groq API) is available"""
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv(), override=True)
    
    key = os.getenv("GROQ_API_KEY")
    return key is not None and len(key) > 0
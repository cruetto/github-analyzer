import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def pytest_configure(config):
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "slow: marks tests as slow")


@pytest.fixture(scope="session")
def github_api_available():
    import requests
    try:
        response = requests.get("https://api.github.com", timeout=5)
        return response.status_code == 200
    except:
        return False


@pytest.fixture(scope="session")
def llm_available():
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv(), override=True)
    key = os.getenv("GROQ_API_KEY")
    return key is not None and len(key) > 0
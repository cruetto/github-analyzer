import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.nlp import extract_repo
from utils.github_api import fetch_repo, analyze_project_structure, get_readme_content
from utils.analysis import generate_comprehensive_analysis


QUERIES = [
    {"query": "I need a library for working with matrices and data analysis", "expected": ["pandas", "numpy"]},
    {"query": "What framework is good for creating graphs?", "expected": ["matplotlib", "networkx"]},
    {"query": "Show me a popular Python web framework", "expected": ["flask", "fastapi"]},
    {"query": "I want to analyze the JavaScript UI library from Meta", "expected": ["react"]},
    {"query": "What is a good HTTP client library for Python?", "expected": ["requests", "httpx"]},
]


class TestEntityExtraction:

    @pytest.mark.parametrize("data", QUERIES, ids=[q["query"][:30] for q in QUERIES])
    def test_extract_repo(self, data):
        result = extract_repo(data["query"])
        assert result is not None
        assert len(result) > 0
        result_lower = result.lower()
        assert any(exp.lower() in result_lower or result_lower in exp.lower() for exp in data["expected"])


class TestGitHubAPI:

    def test_fetch_valid_repo(self):
        repo = fetch_repo("pandas")
        assert repo is not None
        assert "Name" in repo
        assert repo["Stars"] > 0

    def test_fetch_invalid_repo(self):
        repo = fetch_repo("this-repo-does-not-exist-xyz123")
        assert repo is None


class TestAnalysis:

    def test_full_workflow(self):
        repo = fetch_repo("pandas")
        assert repo is not None

        structure = analyze_project_structure(repo["Full_Name"])
        assert structure is not None

        readme = get_readme_content(repo["Full_Name"])
        assert readme is not None

        analysis = generate_comprehensive_analysis(repo, structure, readme, {})
        assert analysis is not None
        assert len(analysis) > 100
"""
GitHub AI Analyzer - Pytest Test Suite
=======================================
5 essential tests for pytest: pytest tests/

Tests use natural language queries as required by TASK.md
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.nlp import extract_repo, get_llm, RepoEntity
from utils.github_api import (
    fetch_repo, 
    analyze_project_structure,
    get_readme_content
)
from utils.analysis import generate_comprehensive_analysis


# 5 Natural Language Test Queries (as per TASK.md requirements)
TEST_QUERIES = [
    {
        "id": 1,
        "query": "I need a library for working with matrices and data analysis",
        "expected_repo": "pandas",
        "description": "Duomenų analizės biblioteka"
    },
    {
        "id": 2,
        "query": "What framework is good for creating graphs and visualizations?",
        "expected_repo": "matplotlib",
        "description": "Grafikų kūrimo biblioteka"
    },
    {
        "id": 3,
        "query": "Show me a popular Python web framework",
        "expected_repo": "flask",
        "description": "Python web framework"
    },
    {
        "id": 4,
        "query": "I want to analyze the JavaScript UI library from Meta",
        "expected_repo": "react",
        "description": "JavaScript UI biblioteka"
    },
    {
        "id": 5,
        "query": "What is a good HTTP client library for Python?",
        "expected_repo": "requests",
        "description": "Python HTTP klientas"
    }
]


class TestEntityExtraction:
    """Test 1: Entity Extraction with Natural Language Queries"""
    
    @pytest.mark.parametrize("query_data", TEST_QUERIES, ids=[q["query"][:30] for q in TEST_QUERIES])
    def test_extract_repo_from_natural_language(self, query_data):
        """Extract repository name from natural language query"""
        extracted = extract_repo(query_data["query"])
        
        assert extracted is not None, f"Extraction failed for: {query_data['query']}"
        assert len(extracted) > 0, "Empty extraction result"
        
        # Check if expected repo is in extracted result
        expected = query_data["expected_repo"].lower()
        extracted_lower = extracted.lower()
        
        assert expected in extracted_lower or extracted_lower in expected, \
            f"Expected '{expected}' in '{extracted}' for query: {query_data['query']}"


class TestGitHubAPI:
    """Test 2: GitHub API Integration"""
    
    def test_fetch_valid_repository(self):
        """Fetch valid repository data"""
        result = fetch_repo("pandas")
        
        assert result is not None, "Should return repository data"
        assert "Name" in result
        assert "Stars" in result
        assert result["Stars"] > 0
    
    def test_fetch_invalid_repository(self):
        """Handle invalid repository gracefully"""
        result = fetch_repo("this-repo-does-not-exist-xyz123")
        assert result is None, "Should return None for invalid repo"


class TestAnalysisWorkflow:
    """Test 3: Complete Analysis Workflow (Integration)"""
    
    def test_full_analysis_workflow(self):
        """Test complete analysis from query to result"""
        # Step 1: Extract entity
        query = TEST_QUERIES[0]["query"]
        repo_name = extract_repo(query)
        assert repo_name is not None
        
        # Step 2: Fetch repository
        repo_data = fetch_repo("pandas")
        assert repo_data is not None
        
        # Step 3: Analyze structure
        structure = analyze_project_structure(repo_data["Full_Name"])
        assert structure is not None
        
        # Step 4: Get README
        readme = get_readme_content(repo_data["Full_Name"])
        assert readme is not None
        
        # Step 5: Generate analysis
        analysis = generate_comprehensive_analysis(repo_data, structure, readme, {})
        assert analysis is not None
        assert len(analysis) > 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
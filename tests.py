"""
GitHub AI Analyzer - Test Suite
================================
Comprehensive testing including:
- Automated functional tests (3)
- NLP quality tests
- Manual evaluation framework (3)
- 5 different user queries with expected results
"""

import unittest
import sys
import os
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import from refactored modules
from nlp import extract_repo, get_llm
from github_api import fetch_repo, fetch_repo_contents, analyze_project_structure
from analysis import generate_comprehensive_analysis

# Test Configuration
TEST_QUERIES = [
    {
        "id": 1,
        "query": "Analyze the tensorflow repository",
        "expected_repo": "tensorflow",
        "expected_language": "Python",
        "min_stars": 100000,
        "evaluation_criteria": [
            "Should extract 'tensorflow' as repository name",
            "Should fetch repository data successfully",
            "Should provide comprehensive analysis",
            "Response should be in Lithuanian"
        ]
    },
    {
        "id": 2,
        "query": "What does the React library do?",
        "expected_repo": "react",
        "expected_language": "JavaScript",
        "min_stars": 200000,
        "evaluation_criteria": [
            "Should extract 'react' as repository name",
            "Should identify JavaScript as main language",
            "Should describe React's purpose",
            "Should show project structure"
        ]
    },
    {
        "id": 3,
        "query": "Tell me about the flask web framework",
        "expected_repo": "flask",
        "expected_language": "Python",
        "min_stars": 60000,
        "evaluation_criteria": [
            "Should extract 'flask' as repository name",
            "Should fetch dependencies (requirements.txt)",
            "Should analyze main files",
            "Should provide installation instructions"
        ]
    },
    {
        "id": 4,
        "query": "Show me information about pandas data analysis library",
        "expected_repo": "pandas",
        "expected_language": "Python",
        "min_stars": 40000,
        "evaluation_criteria": [
            "Should extract 'pandas' as repository name",
            "Should identify data analysis purpose",
            "Should show dependencies",
            "Should include README analysis"
        ]
    },
    {
        "id": 5,
        "query": "How does the express.js framework work?",
        "expected_repo": "express",
        "expected_language": "JavaScript",
        "min_stars": 60000,
        "evaluation_criteria": [
            "Should extract 'express' as repository name",
            "Should fetch package.json dependencies",
            "Should analyze main entry points",
            "Should explain framework purpose"
        ]
    }
]


@dataclass
class TestResult:
    """Test result data structure"""
    test_name: str
    passed: bool
    score: float  # 0.0 to 1.0
    details: str
    timestamp: str = ""
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


class EntityExtractionTests(unittest.TestCase):
    """Automated Test 1: Entity Extraction Tests"""
    
    def setUp(self):
        """Set up test fixtures"""
        try:
            self.extract_repo = extract_repo
            self.import_success = True
        except ImportError as e:
            self.import_success = False
            self.import_error = str(e)
    
    def test_extract_repo_basic(self):
        """Test basic repository name extraction"""
        if not self.import_success:
            self.skipTest(f"Import failed: {self.import_error}")
        
        test_cases = [
            ("Analyze tensorflow", "tensorflow"),
            ("What does React do?", "react"),
            ("Tell me about flask", "flask"),
            ("Show pandas library", "pandas"),
            ("How does express work?", "express"),
        ]
        
        results = []
        for query, expected in test_cases:
            try:
                extracted = self.extract_repo(query)
                # Check if expected repo name is in extracted result (case-insensitive)
                match = expected.lower() in extracted.lower() if extracted else False
                results.append({
                    "query": query,
                    "expected": expected,
                    "extracted": extracted,
                    "match": match
                })
            except Exception as e:
                results.append({
                    "query": query,
                    "expected": expected,
                    "extracted": None,
                    "match": False,
                    "error": str(e)
                })
        
        # Calculate accuracy
        matches = sum(1 for r in results if r["match"])
        accuracy = matches / len(results)
        
        print(f"\n{'='*60}")
        print("ENTITY EXTRACTION TEST RESULTS")
        print(f"{'='*60}")
        for r in results:
            status = "✓" if r["match"] else "✗"
            print(f"{status} Query: '{r['query']}'")
            print(f"  Expected: {r['expected']}, Got: {r.get('extracted', 'Error')}")
            if 'error' in r:
                print(f"  Error: {r['error']}")
        print(f"\nAccuracy: {accuracy:.2%} ({matches}/{len(results)})")
        print(f"{'='*60}")
        
        # Assert at least 60% accuracy (LLM extraction may vary)
        self.assertGreaterEqual(accuracy, 0.6, 
            f"Entity extraction accuracy {accuracy:.2%} is below 60% threshold")


class GitHubAPITests(unittest.TestCase):
    """Automated Test 2: GitHub API Integration Tests"""
    
    def setUp(self):
        """Set up test fixtures"""
        try:
            self.fetch_repo = fetch_repo
            self.fetch_repo_contents = fetch_repo_contents
            self.analyze_project_structure = analyze_project_structure
            self.import_success = True
        except ImportError as e:
            self.import_success = False
            self.import_error = str(e)
    
    def test_fetch_repo_valid(self):
        """Test fetching a valid repository"""
        if not self.import_success:
            self.skipTest(f"Import failed: {self.import_error}")
        
        # Test with a well-known repository
        result = self.fetch_repo("flask")
        
        self.assertIsNotNone(result, "Should return repository data")
        self.assertIn("Name", result, "Should contain Name field")
        self.assertIn("Stars", result, "Should contain Stars field")
        self.assertIn("Language", result, "Should contain Language field")
        self.assertIn("Description", result, "Should contain Description field")
        
        print(f"\n{'='*60}")
        print("GITHUB API TEST - Valid Repository")
        print(f"{'='*60}")
        print(f"Repository: {result['Name']}")
        print(f"Author: {result['Author']}")
        print(f"Stars: {result['Stars']:,}")
        print(f"Language: {result['Language']}")
        print(f"Description: {result['Description'][:100]}...")
        print(f"{'='*60}")
        
        # Verify reasonable data
        self.assertGreater(result["Stars"], 0, "Should have positive star count")
        self.assertIsNotNone(result["Language"], "Should have a language")
    
    def test_fetch_repo_invalid(self):
        """Test fetching an invalid repository"""
        if not self.import_success:
            self.skipTest(f"Import failed: {self.import_error}")
        
        result = self.fetch_repo("this-repo-definitely-does-not-exist-12345")
        
        print(f"\n{'='*60}")
        print("GITHUB API TEST - Invalid Repository")
        print(f"{'='*60}")
        print(f"Result: {result}")
        print(f"{'='*60}")
        
        self.assertIsNone(result, "Should return None for invalid repository")
    
    def test_analyze_structure(self):
        """Test project structure analysis"""
        if not self.import_success:
            self.skipTest(f"Import failed: {self.import_error}")
        
        structure = self.analyze_project_structure("pallets/flask")
        
        self.assertIsNotNone(structure, "Should return structure data")
        self.assertIn("main_files", structure, "Should have main_files")
        self.assertIn("config_files", structure, "Should have config_files")
        self.assertIn("directories", structure, "Should have directories")
        
        print(f"\n{'='*60}")
        print("GITHUB API TEST - Structure Analysis")
        print(f"{'='*60}")
        print(f"Main Files: {structure.get('main_files', [])}")
        print(f"Config Files: {structure.get('config_files', [])}")
        print(f"Documentation: {structure.get('documentation', [])}")
        print(f"Directories: {structure.get('directories', [])}")
        print(f"{'='*60}")


class ResponseQualityTests(unittest.TestCase):
    """Automated Test 3: Response Quality Tests"""
    
    def setUp(self):
        """Set up test fixtures"""
        try:
            self.get_llm = get_llm
            self.generate_comprehensive_analysis = generate_comprehensive_analysis
            self.import_success = True
        except ImportError as e:
            self.import_success = False
            self.import_error = str(e)
    
    def test_llm_initialization(self):
        """Test LLM can be initialized"""
        if not self.import_success:
            self.skipTest(f"Import failed: {self.import_error}")
        
        try:
            llm = self.get_llm()
            self.assertIsNotNone(llm, "LLM should be initialized")
            
            print(f"\n{'='*60}")
            print("RESPONSE QUALITY TEST - LLM Initialization")
            print(f"{'='*60}")
            print("✓ LLM initialized successfully")
            print(f"Model: llama-3.3-70b-versatile")
            print(f"{'='*60}")
        except Exception as e:
            self.fail(f"LLM initialization failed: {e}")
    
    def test_analysis_generation(self):
        """Test analysis generation quality"""
        if not self.import_success:
            self.skipTest(f"Import failed: {self.import_error}")
        
        # Mock repository data
        mock_repo = {
            "Name": "flask",
            "Author": "pallets",
            "Stars": 65000,
            "Forks": 16000,
            "Description": "The Python micro framework for building web applications.",
            "Language": "Python",
            "Topics": ["python", "web", "framework"],
            "URL": "https://github.com/pallets/flask",
            "Default_Branch": "main",
            "Full_Name": "pallets/flask"
        }
        
        mock_structure = {
            "main_files": ["src/flask/__init__.py", "src/flask/app.py"],
            "config_files": ["pyproject.toml", "requirements"],
            "documentation": ["README.md", "CHANGES.rst"],
            "directories": ["src", "tests", "docs"]
        }
        
        mock_readme = "Flask is a lightweight WSGI web application framework."
        mock_dependencies = {"Python": ["werkzeug", "jinja2", "click", "itsdangerous"]}
        
        try:
            analysis = self.generate_comprehensive_analysis(
                mock_repo, mock_structure, mock_readme, mock_dependencies
            )
            
            self.assertIsNotNone(analysis, "Should return analysis")
            self.assertIsInstance(analysis, str, "Analysis should be a string")
            self.assertGreater(len(analysis), 100, "Analysis should be substantial")
            
            # Check if analysis contains key elements
            has_repo_name = "flask" in analysis.lower()
            has_language = "python" in analysis.lower()
            
            print(f"\n{'='*60}")
            print("RESPONSE QUALITY TEST - Analysis Generation")
            print(f"{'='*60}")
            print(f"Analysis Length: {len(analysis)} characters")
            print(f"Contains repo name: {'✓' if has_repo_name else '✗'}")
            print(f"Contains language: {'✓' if has_language else '✗'}")
            print(f"\nSample Analysis (first 300 chars):")
            print(f"{analysis[:300]}...")
            print(f"{'='*60}")
            
            self.assertTrue(has_repo_name, "Analysis should mention repository name")
            
        except Exception as e:
            self.fail(f"Analysis generation failed: {e}")


class ManualEvaluationFramework:
    """Manual Evaluation Framework (3 manual tests)"""
    
    @staticmethod
    def semantic_similarity_evaluation(query: str, response: str, expected_themes: List[str]) -> TestResult:
        """
        Manual Test 1: Semantic Similarity Evaluation
        Human evaluator checks if response addresses the query semantically
        """
        print(f"\n{'='*60}")
        print("MANUAL EVALUATION 1: Semantic Similarity")
        print(f"{'='*60}")
        print(f"Query: {query}")
        print(f"\nExpected Themes:")
        for theme in expected_themes:
            print(f"  - {theme}")
        print(f"\nResponse Preview:")
        print(f"  {response[:500]}...")
        print(f"\n{'='*60}")
        print("Evaluator Instructions:")
        print("1. Does the response address the user's intent?")
        print("2. Are the expected themes covered?")
        print("3. Is the information accurate and relevant?")
        print(f"{'='*60}")
        
        return TestResult(
            test_name="Semantic Similarity",
            passed=True,
            score=0.0,  # To be filled by evaluator
            details="Manual evaluation required - see instructions above"
        )
    
    @staticmethod
    def response_structure_evaluation(response: str) -> TestResult:
        """
        Manual Test 2: Response Structure Evaluation
        Checks if response is well-structured and formatted
        """
        print(f"\n{'='*60}")
        print("MANUAL EVALUATION 2: Response Structure")
        print(f"{'='*60}")
        print(f"Response to evaluate:")
        print(f"  {response[:500]}...")
        print(f"\n{'='*60}")
        print("Evaluator Instructions:")
        print("1. Is the response well-organized?")
        print("2. Does it use appropriate formatting (sections, lists)?")
        print("3. Is it easy to read and understand?")
        print("Score: 0.0 (poor) to 1.0 (excellent)")
        print(f"{'='*60}")
        
        return TestResult(
            test_name="Response Structure",
            passed=True,
            score=0.0,
            details="Manual evaluation required - see instructions above"
        )
    
    @staticmethod
    def completeness_evaluation(query: str, response: str, expected_elements: List[str]) -> TestResult:
        """
        Manual Test 3: Completeness Evaluation
        Checks if all expected information is present
        """
        print(f"\n{'='*60}")
        print("MANUAL EVALUATION 3: Completeness")
        print(f"{'='*60}")
        print(f"Query: {query}")
        print(f"\nExpected Elements:")
        for element in expected_elements:
            print(f"  - {element}")
        print(f"\nResponse Preview:")
        print(f"  {response[:500]}...")
        print(f"\n{'='*60}")
        print("Evaluator Instructions:")
        print("Check each expected element:")
        for i, element in enumerate(expected_elements, 1):
            print(f"  {i}. {element}: [ ] Present [ ] Missing")
        print(f"\nCompleteness Score: ___/10")
        print(f"{'='*60}")
        
        return TestResult(
            test_name="Completeness",
            passed=True,
            score=0.0,
            details="Manual evaluation required - see instructions above"
        )


class NLPQualityMetrics:
    """NLP Quality Metrics Calculator"""
    
    @staticmethod
    def calculate_bleu(reference: str, hypothesis: str) -> float:
        """
        Calculate simplified BLEU-like score
        (For proper BLEU, use nltk.translate.bleu_score)
        """
        ref_words = set(reference.lower().split())
        hyp_words = set(hypothesis.lower().split())
        
        if not hyp_words:
            return 0.0
        
        # Calculate word overlap
        overlap = len(ref_words & hyp_words)
        precision = overlap / len(hyp_words) if hyp_words else 0
        
        # Simplified BLEU approximation
        return precision
    
    @staticmethod
    def calculate_rouge_l(reference: str, hypothesis: str) -> float:
        """
        Calculate simplified ROUGE-L score
        (For proper ROUGE, use rouge_score library)
        """
        ref_words = reference.lower().split()
        hyp_words = hypothesis.lower().split()
        
        # Find longest common subsequence (simplified)
        def lcs_length(x, y):
            m, n = len(x), len(y)
            dp = [[0] * (n + 1) for _ in range(m + 1)]
            for i in range(1, m + 1):
                for j in range(1, n + 1):
                    if x[i-1] == y[j-1]:
                        dp[i][j] = dp[i-1][j-1] + 1
                    else:
                        dp[i][j] = max(dp[i-1][j], dp[i][j-1])
            return dp[m][n]
        
        lcs = lcs_length(ref_words, hyp_words)
        
        if not ref_words or not hyp_words:
            return 0.0
        
        recall = lcs / len(ref_words)
        precision = lcs / len(hyp_words)
        
        if recall + precision == 0:
            return 0.0
        
        f1 = 2 * recall * precision / (recall + precision)
        return f1
    
    @staticmethod
    def entity_extraction_accuracy(extracted: str, expected: str) -> float:
        """Calculate entity extraction accuracy"""
        if not extracted or not expected:
            return 0.0
        
        extracted_lower = extracted.lower()
        expected_lower = expected.lower()
        
        # Exact match
        if extracted_lower == expected_lower:
            return 1.0
        
        # Partial match
        if expected_lower in extracted_lower or extracted_lower in expected_lower:
            return 0.8
        
        # No match
        return 0.0


def generate_test_report(test_results: List[TestResult]) -> str:
    """Generate a formatted test report"""
    report = []
    report.append("\n" + "=" * 70)
    report.append("TEST REPORT - GitHub AI Analyzer")
    report.append("=" * 70)
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # Summary
    total = len(test_results)
    passed = sum(1 for r in test_results if r.passed)
    avg_score = sum(r.score for r in test_results) / total if total > 0 else 0
    
    report.append("SUMMARY")
    report.append("-" * 40)
    report.append(f"Total Tests: {total}")
    report.append(f"Passed: {passed}")
    report.append(f"Failed: {total - passed}")
    report.append(f"Average Score: {avg_score:.2f}")
    report.append("")
    
    # Detailed Results
    report.append("DETAILED RESULTS")
    report.append("-" * 40)
    for i, result in enumerate(test_results, 1):
        status = "✓ PASS" if result.passed else "✗ FAIL"
        report.append(f"{i}. {result.test_name}: {status}")
        report.append(f"   Score: {result.score:.2f}")
        report.append(f"   Details: {result.details}")
        report.append(f"   Timestamp: {result.timestamp}")
        report.append("")
    
    return "\n".join(report)


def run_all_tests():
    """Run all automated tests"""
    print("\n" + "=" * 70)
    print("RUNNING AUTOMATED TESTS")
    print("=" * 70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(EntityExtractionTests))
    suite.addTests(loader.loadTestsFromTestCase(GitHubAPITests))
    suite.addTests(loader.loadTestsFromTestCase(ResponseQualityTests))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║              GitHub AI Analyzer - Test Suite                         ║
║                                                                      ║
║  This test suite includes:                                           ║
║  • 3 Automated Functional Tests                                      ║
║  • NLP Quality Metrics (BLEU, ROUGE-L)                               ║
║  • Manual Evaluation Framework (3 tests)                             ║
║  • 5 Different User Query Test Cases                                 ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    # Run automated tests
    run_all_tests()
    
    # Print test queries
    print("\n" + "=" * 70)
    print("TEST QUERIES FOR MANUAL EVALUATION")
    print("=" * 70)
    for q in TEST_QUERIES:
        print(f"\nQuery {q['id']}: \"{q['query']}\"")
        print(f"  Expected Repo: {q['expected_repo']}")
        print(f"  Expected Language: {q['expected_language']}")
        print(f"  Min Stars: {q['min_stars']:,}")
        print(f"  Evaluation Criteria:")
        for criterion in q['evaluation_criteria']:
            print(f"    - {criterion}")
    
    print("\n" + "=" * 70)
    print("To run manual evaluations, use:")
    print("  from tests import ManualEvaluationFramework")
    print("  evaluator = ManualEvaluationFramework()")
    print("=" * 70)
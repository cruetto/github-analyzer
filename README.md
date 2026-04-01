# GitHub AI Analyzer

AI-powered virtual assistant that analyzes GitHub repositories using natural language queries. It interprets user requests, fetches repository data, analyzes project structure and dependencies, and generates comprehensive summaries in Lithuanian using Llama 3.3.

## Features

- **Natural Language Processing**: Extract repository names from natural language queries using LLM
- **GitHub API Integration**: Fetch repository data, structure, and contents
- **Intelligent Analysis**: Generate comprehensive summaries using Llama 3.3
- **Structured Output**: Display results in organized tables, metrics, and formatted text
- **Lithuanian Language Support**: All analysis generated in Lithuanian

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture documentation.

```
User Query (Natural Language)
         ↓
   NLP Processing (Entity Extraction via LLM)
         ↓
   GitHub API Integration
         ↓
   Data Analysis (Structure, Dependencies, README)
         ↓
   LLM Response Generation (Llama 3.3)
         ↓
   Structured UI Display (Streamlit)
```

## Technologies Used

| Technology | Purpose | Category |
|------------|---------|----------|
| **Streamlit** | Web UI Framework | Frontend |
| **LangChain** | LLM Orchestration | AI/ML |
| **Groq API** | LLM Provider (Llama 3.3) | AI/ML |
| **Pydantic** | Data Validation & Structured Output | Data |
| **Requests** | HTTP Client for GitHub API | Integration |
| **GitHub API** | Repository Data Source | External API |
| **python-dotenv** | Environment Configuration | Configuration |

## Setup

### Prerequisites

- Python 3.9+
- Groq API Key (get from https://console.groq.com/)

### Installation

1. **Clone and enter directory**
   ```bash
   git clone https://github.com/cruetto/github-analyzer.git
   cd github-analyzer
   ```

2. **Create virtual environment and install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

3. **Add API key**
   
   Create `.env` file in project root:
   ```env
   GROQ_API_KEY=your_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

   The application will open in your browser at `http://localhost:8501`

## Usage

1. Enter a natural language query about a GitHub repository:
   - "What does the tensorflow repository do?"
   - "Analyze the React library"
   - "Tell me about flask web framework"

2. The assistant will:
   - Extract the repository name from your query
   - Fetch repository data from GitHub
   - Analyze project structure and dependencies
   - Generate a comprehensive summary in Lithuanian

3. View structured results including:
   - Repository metrics (Stars, Forks, Language)
   - Project structure analysis
   - Main files analysis
   - Dependencies overview
   - README content
   - AI-generated comprehensive analysis

## Testing

The project includes comprehensive testing:

### Run Automated Tests

```bash
python tests/test_suite.py
```

This runs:
- **Entity Extraction Tests**: Verify NLP entity extraction accuracy
- **GitHub API Tests**: Test API integration and data fetching
- **Response Quality Tests**: Validate LLM response generation

### Generate Test Report

```bash
python tests/test_evaluation.py
```

This generates:
- `TEST_REPORT.txt`: Detailed test evaluation report
- `test_results.json`: Machine-readable test results

### Test Queries

The test suite includes 5 different test queries:

1. "Analyze the tensorflow repository"
2. "What does the React library do?"
3. "Tell me about the flask web framework"
4. "Show me information about pandas data analysis library"
5. "How does the express.js framework work?"

### Manual Evaluation

For manual evaluation, use the `ManualEvaluationFramework` class:

```python
from tests import ManualEvaluationFramework

evaluator = ManualEvaluationFramework()

# Semantic Similarity Evaluation
result = evaluator.semantic_similarity_evaluation(
    query="Analyze tensorflow",
    response="...",
    expected_themes=["purpose", "language", "features"]
)

# Response Structure Evaluation
result = evaluator.response_structure_evaluation(response="...")

# Completeness Evaluation
result = evaluator.completeness_evaluation(
    query="...",
    response="...",
    expected_elements=["repository name", "language", "stars"]
)
```

## Project Structure

```
github-analyzer/
├── app.py                    # Main Streamlit application (UI layer)
├── utils/                    # Utility modules
│   ├── __init__.py           # Package initialization
│   ├── nlp.py                # NLP processing (entity extraction, LLM)
│   ├── github_api.py         # GitHub API integration
│   └── analysis.py           # Analysis functions (LLM-powered)
├── tests/                    # Test suite
│   ├── __init__.py           # Package initialization
│   ├── test_suite.py         # Automated tests and manual evaluation
│   └── test_evaluation.py    # Test evaluation report generator
├── ARCHITECTURE.md           # Architecture documentation
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── TASK.md                   # Original task requirements
├── TEST_REPORT.txt           # Generated test report
├── test_results.json         # Machine-readable test results
└── .env                      # API keys (not in repo)
```

### Module Responsibilities

| Module | Responsibility |
|--------|----------------|
| **app.py** | Streamlit UI, user interaction, result display |
| **utils/nlp.py** | LLM initialization, entity extraction, structured output |
| **utils/github_api.py** | GitHub API calls, data fetching, structure analysis |
| **utils/analysis.py** | LLM-powered analysis, summarization, insights |
| **tests/test_suite.py** | Automated tests, manual evaluation framework |
| **tests/test_evaluation.py** | Test report generation, metrics calculation |

## Key Components

### 1. NLP Processing (`extract_repo`)
- Uses LangChain structured output with Pydantic
- Extracts repository names from natural language queries
- LLM: Llama 3.3 via Groq API

### 2. GitHub API Integration
- `fetch_repo()`: Search and fetch repository information
- `fetch_repo_contents()`: Get repository file structure
- `analyze_project_structure()`: Categorize files (main, config, docs, tests)
- `fetch_file_content()`: Retrieve specific file contents

### 3. Analysis Functions
- `analyze_dependencies()`: Extract dependencies from config files
- `analyze_main_files()`: Analyze purpose of main source files
- `get_readme_content()`: Fetch and parse README
- `generate_comprehensive_analysis()`: Generate full analysis using LLM

### 4. UI Components (Streamlit)
- Query input field
- Repository metrics display
- Project structure visualization
- Main files analysis
- Dependencies overview
- README content display
- AI-generated comprehensive analysis

## Evaluation Metrics

The test suite evaluates:

- **Entity Extraction Accuracy**: Percentage of correctly extracted repository names
- **API Success Rate**: Percentage of successful GitHub API calls
- **Analysis Generation Success**: Percentage of successful LLM analyses
- **NLP Quality Metrics**:
  - BLEU Score: N-gram precision
  - ROUGE-L Score: Longest common subsequence
  - Semantic Similarity: Thematic coverage

## NLP Methods Used

1. **Intent Detection**: Determines user wants to analyze a repository
2. **Entity Extraction**: Extracts repository name using structured LLM output
3. **Named Entity Recognition**: Identifies repository names in natural language

## Design Patterns

- **Pipeline Pattern**: Sequential data processing through layers
- **Repository Pattern**: Abstracted GitHub API access
- **Strategy Pattern**: Different analysis for different file types
- **Caching Pattern**: LLM instance caching for performance

## Limitations

- Requires active internet connection for GitHub API and Groq API
- LLM responses may vary slightly between runs
- Repository must be public or API key must have access
- Analysis limited to first 50 lines of main files

## Future Improvements

- Add support for private repositories
- Implement caching for repository data
- Add more detailed code analysis
- Support for multiple languages in output
- Add voice input/output capabilities

## License

This project is for educational purposes.
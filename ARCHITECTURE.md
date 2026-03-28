# Architecture Design - GitHub AI Analyzer

## Overview
The GitHub AI Analyzer is a virtual assistant that interprets natural language queries about GitHub repositories, executes autonomous data fetching and analysis tasks, and presents structured results to users.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           USER INTERFACE (Streamlit)                        │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  Input: Natural Language Query                                        │  │
│  │  "What does the requests library do?"                                 │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────┬─────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        NLP PROCESSING LAYER                                 │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  Intent Detection & Entity Extraction (Structured Output)             │  │
│  │  - Pydantic Model: RepoEntity                                         │  │
│  │  - LLM: Llama 3.3 via Groq API                                        │  │
│  │  - Method: Structured Output Parsing                                  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                    │                                        │
│                                    ▼                                        │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  Extracted Entity: repo_name = "requests"                             │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────┬─────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        TASK EXECUTION LAYER                                 │
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────────┐ │
│  │  GitHub API     │  │  Structure      │  │  Dependencies               │ │
│  │  Integration    │  │  Analyzer       │  │  Analyzer                   │ │
│  │                 │  │                 │  │                             │ │
│  │  - Search repos │  │  - Main files   │  │  - Python (requirements)    │ │
│  │  - Fetch info   │  │  - Config files │  │  - Node.js (package.json)   │ │
│  │  - Get contents │  │  - Documentation│  │  - Other frameworks         │ │
│  └────────┬────────┘  └────────┬────────┘  └──────────────┬──────────────┘ │
│           │                    │                           │                │
│           └────────────────────┼───────────────────────────┘                │
│                                │                                            │
│                                ▼                                            │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  README Content Fetcher                                               │  │
│  │  - Fetches README.md, README.rst, etc.                                │  │
│  │  - Extracts first 2000 characters for analysis                        │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────┬─────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      RESPONSE GENERATION LAYER                              │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  LLM Processing (Llama 3.3 via Groq)                                  │  │
│  │                                                                       │  │
│  │  Prompts:                                                             │  │
│  │  1. Comprehensive Analysis - Full repository overview                 │  │
│  │  2. Main Files Analysis - Purpose and structure of key files          │  │
│  │  3. Description Translation - Translate to Lithuanian                 │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                    │                                        │
│                                    ▼                                        │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  Structured Response                                                  │  │
│  │  - Repository Details (Stars, Forks, Language, Author)                │  │
│  │  - Project Structure (Main files, Config, Docs, Directories)          │  │
│  │  - Dependencies Analysis                                              │  │
│  │  - README Content                                                     │  │
│  │  - Comprehensive AI Analysis (in Lithuanian)                          │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────┬─────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           USER INTERFACE (Streamlit)                        │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  Output: Structured Display                                           │  │
│  │  - Metrics (Stars, Forks, Language, Author)                           │  │
│  │  - Repository Details                                                 │  │
│  │  - Project Structure                                                  │  │
│  │  - Main Files Analysis                                                │  │
│  │  - Dependencies                                                       │  │
│  │  - README Content                                                     │  │
│  │  - Comprehensive AI Analysis                                          │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Input Analysis (NLP Processing)
- **Intent Detection**: Determines user wants to analyze a GitHub repository
- **Entity Extraction**: Extracts repository name using structured LLM output
- **Technology**: LangChain + Pydantic + Groq API (Llama 3.3)

### 2. Task Execution
- **GitHub API Integration**: REST API calls to fetch repository data
- **Structure Analysis**: Parses directory contents, categorizes files
- **Dependency Analysis**: Extracts dependencies from config files
- **README Fetcher**: Retrieves and processes documentation

### 3. Response Generation
- **LLM Processing**: Uses Llama 3.3 for intelligent analysis
- **Multiple Prompts**: Different prompts for different analysis types
- **Structured Output**: Metrics, tables, formatted text

### 4. Additional Features
- **Context Preservation**: Maintains repository data throughout analysis
- **Caching**: Streamlit resource caching for LLM instance
- **Error Handling**: Graceful handling of API failures

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

## Data Flow

1. **User Input** → Natural language query
2. **Entity Extraction** → Repository name (via LLM structured output)
3. **API Call** → GitHub search for repository
4. **Parallel Fetching** → Structure, Dependencies, README
5. **LLM Analysis** → Generate insights and summaries
6. **UI Rendering** → Display structured results

## Design Patterns

- **Pipeline Pattern**: Sequential processing of data through layers
- **Repository Pattern**: Abstracted data fetching from GitHub
- **Strategy Pattern**: Different analysis strategies for different file types
- **Caching Pattern**: LLM instance caching to avoid reinitialization
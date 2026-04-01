# GitHub AI Analyzer

AI-powered virtual assistant that analyzes GitHub repositories using natural language queries. It interprets user requests, fetches repository data, analyzes project structure and dependencies, and generates comprehensive summaries in Lithuanian using Llama 3.3.

## How to Install

1. **Clone and enter directory**
   ```bash
   git clone https://github.com/cruetto/github-analyzer.git
   cd github-analyzer
   ```

2. **Create virtual environment and install dependencies**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   # or
   source venv/bin/activate  # Linux/Mac
   pip install -r requirements.txt
   ```

3. **Add API key**
   
   Create `.env` file in project root:
   ```env
   GROQ_API_KEY=your_key_here
   ```

## How to Run

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`
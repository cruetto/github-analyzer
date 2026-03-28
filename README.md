# GitHub AI Analyzer

AI-powered tool that analyzes GitHub repositories using natural language queries. It fetches repository data, analyzes project structure, dependencies, and generates comprehensive summaries in Lithuanian using Llama 3.3.

## Setup

1. **Clone and enter directory**
   ```bash
   git clone https://github.com/cruetto/github-analyzer.git
   cd github-analyzer
   ```

2. **Create virtual environment and install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   pip install -r requirements.txt
   ```

3. **Add API key**
   
   Create `.env` file:
   ```env
   GROQ_API_KEY=your_key_here
   ```

4. **Run**
   ```bash
   streamlit run app.py
   ```
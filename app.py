import streamlit as st
import requests
from dotenv import load_dotenv, find_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import os
import base64

load_dotenv(find_dotenv(), override=True)

@st.cache_resource
def get_llm():
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise ValueError("GROQ_API_KEY not found!")
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=key
    )

class RepoEntity(BaseModel):
    repo_name: str = Field(description="GitHub repository name extracted from user text")

def extract_repo(query: str) -> str:
    structured_llm = get_llm().with_structured_output(RepoEntity, include_raw=False)
    result = structured_llm.invoke(query)
    # Handle both dict and Pydantic object responses
    if isinstance(result, dict):
        return result.get("repo_name", "")
    elif hasattr(result, "repo_name"):
        return result.repo_name  # type: ignore[union-attr]
    return ""

def fetch_repo(repo_name: str) -> Optional[dict]:
    url = f"https://api.github.com/search/repositories?q={repo_name}&per_page=1"
    res = requests.get(url)
    if res.status_code == 200 and res.json().get("items"):
        item = res.json()["items"][0]
        return {
            "Name": item["name"],
            "Author": item["owner"]["login"],
            "Stars": item["stargazers_count"],
            "Forks": item["forks_count"],
            "Description": item["description"] or "No description",
            "URL": item["html_url"],
            "Language": item.get("language", "Unknown"),
            "Topics": item.get("topics", []),
            "Default_Branch": item.get("default_branch", "main"),
            "Full_Name": item["full_name"]
        }
    return None

def fetch_repo_contents(full_name: str, path: str = "") -> Optional[List[Dict]]:
    """Fetch repository contents from GitHub API"""
    url = f"https://api.github.com/repos/{full_name}/contents/{path}"
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()
    return None

def fetch_file_content(full_name: str, file_path: str) -> Optional[str]:
    """Fetch specific file content from GitHub API"""
    url = f"https://api.github.com/repos/{full_name}/contents/{file_path}"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        if data.get("content"):
            try:
                content = base64.b64decode(data["content"]).decode('utf-8')
                return content
            except:
                return None
    return None

def analyze_project_structure(full_name: str) -> Dict:
    """Analyze the project structure and identify key files"""
    contents = fetch_repo_contents(full_name)
    if not contents:
        return {}
    
    structure = {
        "main_files": [],
        "config_files": [],
        "documentation": [],
        "test_files": [],
        "directories": []
    }
    
    # Key file patterns
    main_patterns = ["main.py", "app.py", "index.js", "index.ts", "main.js", "main.go", 
                     "main.java", "Program.cs", "main.cpp", "main.c", "index.html",
                     "server.js", "app.js", "__init__.py"]
    
    config_patterns = ["package.json", "requirements.txt", "Pipfile", "setup.py", 
                      "Cargo.toml", "go.mod", "pom.xml", "build.gradle", "Makefile",
                      "CMakeLists.txt", "composer.json", "Gemfile", "pyproject.toml"]
    
    doc_patterns = ["README.md", "README.rst", "README.txt", "CONTRIBUTING.md", 
                   "LICENSE", "CHANGELOG.md", "DOCS.md"]
    
    for item in contents:
        name = item["name"].lower()
        item_type = item["type"]
        
        if item_type == "dir":
            structure["directories"].append(item["name"])
        elif item_type == "file":
            # Check for main files
            if any(pattern.lower() in name for pattern in main_patterns):
                structure["main_files"].append(item["name"])
            # Check for config files
            elif any(pattern.lower() in name for pattern in config_patterns):
                structure["config_files"].append(item["name"])
            # Check for documentation
            elif any(pattern.lower() in name for pattern in doc_patterns):
                structure["documentation"].append(item["name"])
            # Check for test files
            elif "test" in name or "spec" in name:
                structure["test_files"].append(item["name"])
    
    return structure

def get_readme_content(full_name: str) -> Optional[str]:
    """Fetch README content"""
    readme_names = ["README.md", "README.rst", "README.txt", "README"]
    for readme in readme_names:
        content = fetch_file_content(full_name, readme)
        if content:
            return content
    return None

def analyze_dependencies(full_name: str, structure: Dict) -> Dict:
    """Analyze project dependencies from config files"""
    dependencies = {}
    
    # Check for Python dependencies
    if "requirements.txt" in structure.get("config_files", []):
        content = fetch_file_content(full_name, "requirements.txt")
        if content:
            deps = [line.strip() for line in content.split('\n') if line.strip() and not line.startswith('#')]
            dependencies["Python (requirements.txt)"] = deps[:10]  # Limit to first 10
    
    # Check for package.json
    if "package.json" in structure.get("config_files", []):
        content = fetch_file_content(full_name, "package.json")
        if content:
            try:
                import json
                pkg = json.loads(content)
                deps = list(pkg.get("dependencies", {}).keys())
                dependencies["Node.js (package.json)"] = deps[:10]  # Limit to first 10
            except:
                pass
    
    return dependencies

def generate_comprehensive_analysis(repo_data: Dict, structure: Dict, readme: Optional[str], dependencies: Dict) -> str:
    """Use LLM to generate comprehensive analysis"""
    
    # Prepare context for LLM
    context = f"""
Repository: {repo_data['Name']} by {repo_data['Author']}
Language: {repo_data['Language']}
Description: {repo_data['Description']}
Topics: {', '.join(repo_data['Topics']) if repo_data['Topics'] else 'None'}

Project Structure:
- Main Files: {', '.join(structure.get('main_files', [])) or 'None found'}
- Config Files: {', '.join(structure.get('config_files', [])) or 'None found'}
- Documentation: {', '.join(structure.get('documentation', [])) or 'None found'}
- Directories: {', '.join(structure.get('directories', [])) or 'None found'}

Dependencies:
{chr(10).join([f"- {k}: {', '.join(v[:5])}" for k, v in dependencies.items()]) if dependencies else 'None analyzed'}

README excerpt (first 500 chars):
{readme[:500] if readme else 'No README found'}
"""
    
    prompt = PromptTemplate.from_template(
        """Analyze this GitHub repository and provide a comprehensive summary in Lithuanian:

{context}

Please provide:
1. What this project does (purpose and functionality)
2. Main files and their roles
3. How to run/install this project (based on config files and README)
4. Key technologies and frameworks used
5. Project structure overview

Be concise but informative."""
    )
    
    chain = prompt | get_llm()
    result = chain.invoke({"context": context})
    return result.content if hasattr(result, "content") else str(result)  # type: ignore[union-attr]

def analyze_main_files(full_name: str, main_files: List[str]) -> str:
    """Analyze main files and their purposes using LLM"""
    if not main_files:
        return "No main files identified."
    
    files_content = {}
    for file in main_files[:3]:  # Limit to first 3 main files
        content = fetch_file_content(full_name, file)
        if content:
            # Get first 50 lines or 2000 chars
            lines = content.split('\n')[:50]
            files_content[file] = '\n'.join(lines)[:2000]
    
    if not files_content:
        return "Could not fetch main file contents."
    
    context = "\n\n".join([f"File: {name}\n{content}" for name, content in files_content.items()])
    
    prompt = PromptTemplate.from_template(
        """Analyze these main files from a GitHub repository and explain in Lithuanian:

{context}

For each file, briefly explain:
1. What is its purpose?
2. What are the key functions/classes?
3. How does it fit into the project?

Be concise and clear."""
    )
    
    chain = prompt | get_llm()
    result = chain.invoke({"context": context})
    return result.content if hasattr(result, "content") else str(result)  # type: ignore[union-attr]

def summarize_repo(desc: str) -> str:
    prompt = PromptTemplate.from_template(
        "Translate this GitHub repo description to Lithuanian and briefly explain its purpose: \n\n{desc}"
    )
    chain = prompt | get_llm()
    result = chain.invoke({"desc": desc})
    return result.content if hasattr(result, "content") else str(result)  # type: ignore[union-attr]

def main():
    st.set_page_config(page_title="GitHub Analyzer", page_icon="🐙", layout="wide")
    st.title("🐙 GitHub AI Analyzer")
    st.markdown("*Comprehensive GitHub repository analysis with AI*")

    query = st.text_input("Enter your request:", placeholder="e.g., What does the requests library do?")

    # Analysis options
    col1, col2, col3 = st.columns(3)
    with col1:
        analyze_structure = st.checkbox("Analyze Structure", value=True)
    with col2:
        analyze_files = st.checkbox("Analyze Main Files", value=True)
    with col3:
        analyze_deps = st.checkbox("Analyze Dependencies", value=True)

    if st.button("🔍 Analyze", type="primary"):
        if not query.strip():
            st.warning("Please enter a query.")
            return

        with st.spinner("Extracting entity..."):
            repo_name = extract_repo(query)
            if not repo_name:
                st.error("Could not extract a repository name from your query.")
                return
            st.info(f"🎯 Extracted target: **{repo_name}**")

        with st.spinner("Fetching data from GitHub API..."):
            repo_data = fetch_repo(repo_name)

        if not repo_data:
            st.error("Repository not found.")
            return

        # Basic Info
        st.subheader("📊 Repository Details")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("⭐ Stars", repo_data["Stars"])
        with col2:
            st.metric("🍴 Forks", repo_data["Forks"])
        with col3:
            st.metric("💻 Language", repo_data["Language"])
        with col4:
            st.metric("👤 Author", repo_data["Author"])
        
        st.markdown(f"**Description:** {repo_data['Description']}")
        st.markdown(f"**URL:** [{repo_data['URL']}]({repo_data['URL']})")
        if repo_data['Topics']:
            st.markdown(f"**Topics:** {', '.join([f'`{t}`' for t in repo_data['Topics']])}")

        # Structure Analysis
        structure = {}
        dependencies = {}
        readme = None
        
        if analyze_structure:
            with st.spinner("Analyzing project structure..."):
                structure = analyze_project_structure(repo_data["Full_Name"])
                readme = get_readme_content(repo_data["Full_Name"])
            
            if structure:
                st.subheader("📁 Project Structure")
                col1, col2 = st.columns(2)
                
                with col1:
                    if structure.get("main_files"):
                        st.markdown("**🎯 Main Files:**")
                        for f in structure["main_files"]:
                            st.markdown(f"- `{f}`")
                    
                    if structure.get("config_files"):
                        st.markdown("**⚙️ Config Files:**")
                        for f in structure["config_files"]:
                            st.markdown(f"- `{f}`")
                
                with col2:
                    if structure.get("documentation"):
                        st.markdown("**📚 Documentation:**")
                        for f in structure["documentation"]:
                            st.markdown(f"- `{f}`")
                    
                    if structure.get("directories"):
                        st.markdown(f"**📂 Directories:** {len(structure['directories'])} found")
                        with st.expander("View directories"):
                            for d in structure["directories"]:
                                st.markdown(f"- `{d}/`")

        # Dependencies Analysis
        if analyze_deps and structure:
            with st.spinner("Analyzing dependencies..."):
                dependencies = analyze_dependencies(repo_data["Full_Name"], structure)
            
            if dependencies:
                st.subheader("📦 Dependencies")
                for dep_type, deps in dependencies.items():
                    with st.expander(f"{dep_type} ({len(deps)} shown)"):
                        for dep in deps:
                            st.markdown(f"- `{dep}`")

        # Main Files Analysis
        if analyze_files and structure.get("main_files"):
            with st.spinner("Analyzing main files with AI..."):
                files_analysis = analyze_main_files(repo_data["Full_Name"], structure["main_files"])
            
            st.subheader("🔍 Main Files Analysis")
            st.markdown(files_analysis)

        # Comprehensive Analysis
        with st.spinner("Generating comprehensive analysis with AI..."):
            comprehensive = generate_comprehensive_analysis(repo_data, structure, readme, dependencies)

        st.subheader("🤖 AI Comprehensive Analysis")
        st.success(comprehensive)

        # README Preview
        if readme:
            with st.expander("📖 README Preview"):
                st.markdown(readme[:2000] + ("..." if len(readme) > 2000 else ""))

        # Raw Data
        with st.expander("🔧 Raw API Response"):
            st.json(repo_data)

if __name__ == "__main__":
    main()

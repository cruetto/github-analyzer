from langchain.prompts import PromptTemplate
from typing import Optional, List, Dict
from .nlp import get_llm
from .github_api import fetch_file_content


def analyze_main_files(full_name: str, main_files: List[str]) -> str:
    if not main_files:
        return "No main files found."
    
    files_content = {}
    for file in main_files[:3]:
        content = fetch_file_content(full_name, file)
        if content:
            lines = content.split('\n')[:50]
            files_content[file] = '\n'.join(lines)[:2000]
    
    if not files_content:
        return "Could not fetch file contents."
    
    context = "\n\n".join([f"File: {name}\n{content}" for name, content in files_content.items()])
    
    prompt = PromptTemplate.from_template(
        """Analyze these main files and explain briefly:

{context}

For each file:
1. What is its purpose?
2. What are the key functions/classes?
3. How does it fit into the project?

Be concise and clear."""
    )
    
    chain = prompt | get_llm()
    result = chain.invoke({"context": context})
    return result.content if hasattr(result, "content") else str(result)


def generate_comprehensive_analysis(repo_data: Dict, structure: Dict, readme: Optional[str], dependencies: Dict) -> str:
    context = f"""
Repository: {repo_data['Name']} by {repo_data['Author']}
Language: {repo_data['Language']}
Description: {repo_data['Description']}
Topics: {', '.join(repo_data['Topics']) if repo_data['Topics'] else 'None'}

Project Structure:
- Main Files: {', '.join(structure.get('main_files', [])) or 'None'}
- Config Files: {', '.join(structure.get('config_files', [])) or 'None'}
- Documentation: {', '.join(structure.get('documentation', [])) or 'None'}
- Directories: {', '.join(structure.get('directories', [])) or 'None'}

Dependencies:
{chr(10).join([f"- {k}: {', '.join(v[:5])}" for k, v in dependencies.items()]) if dependencies else 'None'}

README excerpt:
{readme[:500] if readme else 'No README found'}
"""
    
    prompt = PromptTemplate.from_template(
        """Analyze this GitHub repository and provide a summary:

{context}

Please provide:
1. What this project does
2. Main files and their roles
3. How to run/install this project
4. Key technologies used
5. Project structure overview

Be concise but informative."""
    )
    
    chain = prompt | get_llm()
    result = chain.invoke({"context": context})
    return result.content if hasattr(result, "content") else str(result)


def summarize_repo(desc: str) -> str:
    prompt = PromptTemplate.from_template(
        "Translate this GitHub repo description to English and briefly explain its purpose: \n\n{desc}"
    )
    chain = prompt | get_llm()
    result = chain.invoke({"desc": desc})
    return result.content if hasattr(result, "content") else str(result)
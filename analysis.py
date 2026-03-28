"""
Analysis Module
===============
Handles repository analysis and LLM-powered insights:
- Main files analysis
- Comprehensive repository analysis
- README summarization
- Dependency analysis
"""

from langchain.prompts import PromptTemplate
from typing import Optional, List, Dict
from nlp import get_llm
from github_api import fetch_file_content


def analyze_main_files(full_name: str, main_files: List[str]) -> str:
    """
    Analyze main files and their purposes using LLM
    
    Args:
        full_name: Full repository name (owner/repo)
        main_files: List of main file names
        
    Returns:
        str: LLM-generated analysis of main files
    """
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


def generate_comprehensive_analysis(repo_data: Dict, structure: Dict, readme: Optional[str], dependencies: Dict) -> str:
    """
    Use LLM to generate comprehensive analysis of repository
    
    Args:
        repo_data: Repository metadata dictionary
        structure: Project structure dictionary
        readme: README content (optional)
        dependencies: Dependencies dictionary
        
    Returns:
        str: LLM-generated comprehensive analysis in Lithuanian
    """
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


def summarize_repo(desc: str) -> str:
    """
    Translate and summarize repository description to Lithuanian
    
    Args:
        desc: Repository description in English
        
    Returns:
        str: Translated and summarized description in Lithuanian
    """
    prompt = PromptTemplate.from_template(
        "Translate this GitHub repo description to Lithuanian and briefly explain its purpose: \n\n{desc}"
    )
    chain = prompt | get_llm()
    result = chain.invoke({"desc": desc})
    return result.content if hasattr(result, "content") else str(result)  # type: ignore[union-attr]
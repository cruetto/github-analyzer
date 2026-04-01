"""
GitHub API Integration Module
==============================
Handles all GitHub API interactions:
- Repository search and fetching
- Repository contents retrieval
- File content fetching
- Project structure analysis
"""

import requests
import base64
from typing import Optional, List, Dict


def fetch_repo(repo_name: str) -> Optional[dict]:
    """
    Search and fetch repository information from GitHub
    
    Args:
        repo_name: Repository name to search for
        
    Returns:
        dict: Repository data including name, author, stars, etc.
        None: If repository not found
    """
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
    """
    Fetch repository contents from GitHub API
    
    Args:
        full_name: Full repository name (owner/repo)
        path: Path within repository (empty for root)
        
    Returns:
        list: List of file/directory objects
        None: If fetch fails
    """
    url = f"https://api.github.com/repos/{full_name}/contents/{path}"
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()
    return None


def fetch_file_content(full_name: str, file_path: str) -> Optional[str]:
    """
    Fetch specific file content from GitHub API
    
    Args:
        full_name: Full repository name (owner/repo)
        file_path: Path to file within repository
        
    Returns:
        str: Decoded file content
        None: If fetch fails
    """
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
    """
    Analyze the project structure and identify key files
    
    Args:
        full_name: Full repository name (owner/repo)
        
    Returns:
        dict: Categorized file structure (main_files, config_files, etc.)
    """
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
    """
    Fetch README content from repository
    
    Args:
        full_name: Full repository name (owner/repo)
        
    Returns:
        str: README content
        None: If no README found
    """
    readme_names = ["README.md", "README.rst", "README.txt", "README"]
    for readme in readme_names:
        content = fetch_file_content(full_name, readme)
        if content:
            return content
    return None


def analyze_dependencies(full_name: str, structure: Dict) -> Dict:
    """
    Analyze project dependencies from config files
    
    Args:
        full_name: Full repository name (owner/repo)
        structure: Project structure dictionary
        
    Returns:
        dict: Dependencies by framework type
    """
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
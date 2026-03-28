"""
GitHub AI Analyzer - Main Application
=======================================
Streamlit web application for analyzing GitHub repositories
using natural language queries and AI-powered insights.
"""

import streamlit as st
from nlp import get_llm, extract_repo
from github_api import (
    fetch_repo,
    fetch_repo_contents,
    fetch_file_content,
    analyze_project_structure,
    get_readme_content,
    analyze_dependencies
)
from analysis import analyze_main_files, generate_comprehensive_analysis


@st.cache_resource
def get_cached_llm():
    """Get cached LLM instance"""
    return get_llm()


def main():
    """Main application entry point"""
    st.set_page_config(page_title="GitHub Analyzer", page_icon="🐙", layout="wide")
    st.title("🐙 GitHub AI Analyzer")
    st.markdown("*Comprehensive GitHub repository analysis with AI*")

    query = st.text_input("Enter your request:", placeholder="e.g., What does the requests library do?")

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

        # Run all analyses automatically
        structure = analyze_project_structure(repo_data['Full_Name'])
        st.subheader("📁 Project Structure")
        st.write(structure)

        main_files_analysis = analyze_main_files(repo_data['Full_Name'], structure.get('main_files', []))
        st.subheader("📄 Main Files Analysis")
        st.write(main_files_analysis)

        dependencies = analyze_dependencies(repo_data['Full_Name'], structure)
        st.subheader("📦 Dependencies")
        st.write(dependencies)

        readme = get_readme_content(repo_data['Full_Name'])
        if readme:
            st.subheader("📖 README Content")
            st.write(readme[:2000])  # Show first 2000 chars

        comprehensive_analysis = generate_comprehensive_analysis(repo_data, structure, readme, dependencies)
        st.subheader("🧠 Comprehensive Analysis")
        st.write(comprehensive_analysis)


        
if __name__ == "__main__":
    main()
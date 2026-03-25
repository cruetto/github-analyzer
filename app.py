import streamlit as st
import requests
from dotenv import load_dotenv, find_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import Optional
import os

load_dotenv(find_dotenv(), override=True)

@st.cache_resource
def get_llm():
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise ValueError("GROQ_API_KEY not found!")
    return ChatGroq(
        model_name="llama-3.3-70b-versatile",
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
    return result.repo_name

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
            "URL": item["html_url"]
        }
    return None

def summarize_repo(desc: str) -> str:
    prompt = PromptTemplate.from_template(
        "Translate this GitHub repo description to Lithuanian and briefly explain its purpose: \n\n{desc}"
    )
    chain = prompt | get_llm()
    return chain.invoke({"desc": desc}).content

def main():
    st.set_page_config(page_title="GitHub Analyzer", page_icon="🐙")
    st.title("🐙 GitHub AI Analyzer")

    query = st.text_input("Enter your request:", placeholder="e.g., What does the requests library do?")

    if st.button("Analyze"):
        if not query.strip():
            st.warning("Please enter a query.")
            return

        with st.spinner("Extracting entity..."):
            repo_name = extract_repo(query)
            if not repo_name:
                st.error("Could not extract a repository name from your query.")
                return
            st.info(f"Extracted target: {repo_name}")

        with st.spinner("Fetching data from GitHub API..."):
            repo_data = fetch_repo(repo_name)

        if not repo_data:
            st.error("Repository not found.")
            return

        with st.spinner("Processing with LLM..."):
            summary = summarize_repo(repo_data["Description"])

        st.subheader("Repository Details")
        st.table({
            "Metric": ["Name", "Author", "Stars", "Forks", "URL"],
            "Value": [repo_data["Name"], repo_data["Author"], str(repo_data["Stars"]), str(repo_data["Forks"]), repo_data["URL"]]
        })

        st.subheader("Summary")
        st.success(summary)

        with st.expander("Raw API Response (JSON)"):
            st.json(repo_data)

if __name__ == "__main__":
    main()
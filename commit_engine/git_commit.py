import os
import requests
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv(find_dotenv())

# Get API keys from environment
api_key = os.getenv("OPENAI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
client = OpenAI(api_key=api_key)

# GitHub repository details
OWNER = "yashvanshika"
REPO = "test"
BRANCH = "main"

# Get the latest commit SHA
def get_latest_commit_sha():
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/commits/{BRANCH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    r = requests.get(url, headers=headers)
    if r.status_code == 404 and BRANCH == "main":
        return get_latest_commit_sha_fallback("master")
    r.raise_for_status()
    return r.json()["sha"]

def get_latest_commit_sha_fallback(branch):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/commits/{branch}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()["sha"]

# Get the diff of a commit
def get_commit_diff(sha):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/commits/{sha}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    files = r.json().get("files", [])
    diff = ""
    for file in files:
        if "patch" in file:
            diff += f"File: {file['filename']}\n{file['patch']}\n\n"
    return diff

# Summarize diff using GPT-4.1 mini
def summarize_with_gpt41min(diff_text):
    prompt = f"""
You are a senior software engineer reviewing recent changes in a GitHub repository. Analyze the diff and produce a concise summary split into two clear sections:

Successful Changes – Briefly list the modifications that were implemented correctly and function as intended.

Unsuccessful Changes – Briefly list the changes that were attempted but are either broken, incomplete, or do not function as intended.

Ensure the summary is direct, avoids unnecessary elaboration, and focuses strictly on observable functionality and outcomes.

{diff_text}
"""
    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You summarize git diffs."},
            {"role": "user",   "content": prompt}
        ],
        temperature=0.3,
    )
    return resp.choices[0].message.content

# Main runner
if __name__ == "__main__":
    sha = get_latest_commit_sha()
    ###print(sha)
    
    diff = get_commit_diff(sha)
    ###print(diff)
    summary = summarize_with_gpt41min(diff)
    print("\n🔍 Commit Summary:\n")
    print(summary)

import os
import requests
from dotenv import load_dotenv
from langchain_core.documents import Document

load_dotenv()

github_token = os.getenv("GITHUB_TOKEN")

def fetch_github(owner, repo, endpoint):
    url = f"https://api.github.com/repos/{owner}/{repo}/{endpoint}"
    
    # Debug: Check if token exists
    if not github_token:
        print("Error: GITHUB_TOKEN not found in environment variables")
        return []
    
    print(f"Using token: {github_token[:8]}..." if len(github_token) > 8 else github_token)
    
    headers = {
        "Authorization": f"token {github_token}",  # Changed from "Bearer" to "token"
        "Accept": "application/vnd.github.v3+json",  # Added proper Accept header
        "User-Agent": "Python-Script"  # GitHub requires User-Agent header
    }
    
    print(f"Making request to: {url}")
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print("Success!")
        print(f"Data type: {type(data)}")
        print(f"Data length: {len(data) if isinstance(data, list) else 'Not a list'}")
        print("\n--- RESPONSE DATA ---")
        print(data)
        print("--- END DATA ---\n")
        return data
    else:
        print(f"Failed with status code: {response.status_code}")
        print(f"Response: {response.text}")
        return []

def fetch_github_issues(owner, repo):
    data = fetch_github(owner, repo, "issues")
    return load_issues(data)


def load_issues(issues):
    docs = []
    for entry in issues:
        metadata = {
            "author": entry["user"]["login"],
            "comments": entry["comments"],
            "body": entry["body"],
            "labels": entry["labels"],
            "created_at": entry["created_at"],
        }
        data = entry["title"]
        if entry["body"]:
            data += entry["body"]
        doc = Document(page_content=data, metadata=metadata)
        docs.append(doc)

    return docs
# Fixed endpoint - "code" is not a valid GitHub API endpoint
# Use "contents" to get repository contents
result = fetch_github("username", "repo_name", "issues")
print(f"\nFunction returned: {len(result)} items" if isinstance(result, list) else f"Function returned: {result}")
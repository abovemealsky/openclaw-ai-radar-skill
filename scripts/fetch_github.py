#!/usr/bin/env python3
"""
Fetch trending repositories from GitHub.
"""
import json
import os
import requests
from bs4 import BeautifulSoup

OUTPUT_FILE = "data/raw/open_source.json"

GITHUB_TRENDING_URL = "https://github.com/trending?since=weekly"


def fetch_github_trending():
    """Fetch trending repositories from GitHub."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(GITHUB_TRENDING_URL, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "lxml")
        
        # Find all repository articles
        repos = soup.select("article.box-shadow-normal")
        
        items = []
        for repo in repos[:10]:
            # Get repository name
            repo_link = repo.select_one("h2 a")
            if not repo_link:
                continue
            
            repo_name = repo_link.get("href", "").strip("/")
            url = "https://github.com" + repo_link.get("href", "")
            
            # Get description
            desc_elem = repo.select_one("p")
            description = desc_elem.get_text(strip=True) if desc_elem else ""
            
            # Get language
            lang_elem = repo.select_one("span[itemprop='programmingLanguage']")
            language = lang_elem.get_text(strip=True) if lang_elem else "Unknown"
            
            items.append({
                "repo_name": repo_name,
                "url": url,
                "description": description,
                "language": language
            })
        
        return items
    except Exception as e:
        print(f"Error fetching GitHub trending: {e}")
        return []


def main():
    """Main function to fetch trending repos."""
    os.makedirs("data/raw", exist_ok=True)
    
    print("Fetching GitHub trending repositories...")
    items = fetch_github_trending()
    
    with open(OUTPUT_FILE, "w") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    
    print(f"Fetched {len(items)} trending repos -> {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

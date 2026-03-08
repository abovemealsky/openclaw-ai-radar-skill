#!/usr/bin/env python3
"""
Fetch trending repositories from GitHub.
"""
import json
import os
import requests
from bs4 import BeautifulSoup

# Get the skill root directory (parent of scripts/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)

OUTPUT_FILE = os.path.join(SKILL_ROOT, "data/raw/open_source.json")

GITHUB_TRENDING_URL = "https://github.com/trending?since=weekly"


def fetch_github_trending():
    """Fetch trending repositories from GitHub."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }
        response = requests.get(GITHUB_TRENDING_URL, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "lxml")
        
        # Try multiple selectors (GitHub HTML structure may change)
        repos = []
        
        # Method 1: Find all article elements
        articles = soup.select("article")
        for article in articles:
            # Check if it has the repository content
            h2 = article.select_one("h2")
            if not h2:
                continue
                
            repo_link = h2.select_one("a")
            if not repo_link:
                continue
            
            # Get repo name from href
            href = repo_link.get("href", "")
            if not href or "/" not in href:
                continue
                
            repo_name = href.strip("/")
            url = "https://github.com" + href
            
            # Get description
            desc_elem = article.select_one("p")
            description = desc_elem.get_text(strip=True) if desc_elem else ""
            
            # Get language
            lang_elem = article.select_one("span[itemprop='programmingLanguage']")
            language = lang_elem.get_text(strip=True) if lang_elem else "Unknown"
            
            repos.append({
                "repo_name": repo_name,
                "url": url,
                "description": description,
                "language": language
            })
        
        # If method 1 failed, try method 2
        if not repos:
            # Try finding by specific class patterns
            for article in soup.find_all("article"):
                links = article.find_all("a", href=True)
                for link in links:
                    href = link.get("href", "")
                    if href.startswith("/") and "/" in href[1:]:
                        # This looks like a repo link
                        repo_name = href.strip("/")
                        if repo_name.count("/") == 1:
                            # Get description from next sibling or p tag
                            parent = link.find_parent("article")
                            desc = ""
                            if parent:
                                p = parent.select_one("p")
                                if p:
                                    desc = p.get_text(strip=True)
                            
                            repos.append({
                                "repo_name": repo_name,
                                "url": "https://github.com" + href,
                                "description": desc,
                                "language": "Unknown"
                            })
                            break
        
        return repos[:10]
        
    except Exception as e:
        print(f"Error fetching GitHub trending: {e}")
        import traceback
        traceback.print_exc()
        return []


def main():
    """Main function to fetch trending repos."""
    os.makedirs(os.path.join(SKILL_ROOT, "data/raw"), exist_ok=True)
    
    print("Fetching GitHub trending repositories...")
    items = fetch_github_trending()
    
    print(f"Found {len(items)} repositories")
    
    with open(OUTPUT_FILE, "w") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    
    print(f"Fetched {len(items)} trending repos -> {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

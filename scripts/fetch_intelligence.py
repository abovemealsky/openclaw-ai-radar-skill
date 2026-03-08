#!/usr/bin/env python3
"""
Fetch AI intelligence from various sources and organize by category.
"""
import json
import os
import sys
from datetime import datetime, timedelta
from dateutil import parser as date_parser
import feedparser
import requests
from bs4 import BeautifulSoup

# Get the skill root directory (parent of scripts/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)

# Set mode: "daily" (24h) or "weekly" (7 days)
MODE = os.environ.get("RADAR_MODE", "daily")
MAX_AGE_DAYS = 1 if MODE == "daily" else 7


def load_sources(category):
    """Load sources for a specific category."""
    source_file = os.path.join(SKILL_ROOT, f"sources/{category}_sources.json")
    try:
        with open(source_file, "r") as f:
            data = json.load(f)
        return data.get("sources", [])
    except FileNotFoundError:
        print(f"Warning: {source_file} not found")
        return []


def fetch_rss_feed(source_url, category):
    """Fetch and parse an RSS/Atom feed."""
    try:
        feed = feedparser.parse(source_url)
        entries = []
        now = datetime.now()
        cutoff_date = now - timedelta(days=MAX_AGE_DAYS)
        
        for entry in feed.entries:
            # Extract published date
            published = ""
            published_dt = None
            
            if hasattr(entry, "published"):
                try:
                    published_dt = date_parser.parse(entry.published)
                    published = published_dt.strftime("%Y-%m-%d")
                except:
                    published = now.strftime("%Y-%m-%d")
            elif hasattr(entry, "updated"):
                try:
                    published_dt = date_parser.parse(entry.updated)
                    published = published_dt.strftime("%Y-%m-%d")
                except:
                    published = now.strftime("%Y-%m-%d")
            
            # Skip old entries
            if published_dt:
                if published_dt.tzinfo is not None:
                    published_dt = published_dt.replace(tzinfo=None)
                if published_dt < cutoff_date:
                    continue
            
            # Extract source name
            source = feed.feed.get("title", source_url)
            
            # Clean title
            title = entry.get("title", "").replace("\n", " ").strip()
            
            # Get link
            link = entry.get("link", "")
            
            entries.append({
                "title": title,
                "link": link,
                "published": published,
                "source": source,
                "category": category
            })
        
        return entries
    except Exception as e:
        print(f"Error fetching {source_url}: {e}")
        return []


def fetch_github_trending():
    """Fetch trending repositories from GitHub."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        url = "https://github.com/trending?since=weekly"
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "lxml")
        repos = []
        
        for article in soup.select("article"):
            h2 = article.select_one("h2")
            if not h2:
                continue
            
            repo_link = h2.select_one("a")
            if not repo_link:
                continue
            
            href = repo_link.get("href", "")
            if not href or "/" not in href:
                continue
            
            repo_name = href.strip("/")
            link = "https://github.com" + href
            
            # Description
            desc_elem = article.select_one("p")
            description = desc_elem.get_text(strip=True) if desc_elem else ""
            
            # Language
            lang_elem = article.select_one("span[itemprop='programmingLanguage']")
            language = lang_elem.get_text(strip=True) if lang_elem else "Unknown"
            
            repos.append({
                "title": repo_name,
                "link": link,
                "description": description,
                "language": language,
                "source": "GitHub Trending",
                "category": "open_source"
            })
        
        return repos[:10]
    except Exception as e:
        print(f"Error fetching GitHub trending: {e}")
        return []


def main():
    """Main function to fetch all intelligence."""
    os.makedirs(os.path.join(SKILL_ROOT, "data/raw"), exist_ok=True)
    
    print(f"Fetching AI intelligence... (mode: {MODE}, max {MAX_AGE_DAYS} days)")
    
    all_items = []
    
    # 1. Model Releases
    print("\n--- Model Releases ---")
    sources = load_sources("model")
    for source in sources:
        print(f"Fetching: {source}")
        items = fetch_rss_feed(source, "model_releases")
        all_items.extend(items)
    
    # 2. Research
    print("\n--- Research ---")
    sources = load_sources("research")
    for source in sources:
        print(f"Fetching: {source}")
        items = fetch_rss_feed(source, "research")
        all_items.extend(items)
    
    # 3. Industry
    print("\n--- Industry ---")
    sources = load_sources("industry")
    for source in sources:
        print(f"Fetching: {source}")
        items = fetch_rss_feed(source, "industry")
        all_items.extend(items)
    
    # 4. Policy
    print("\n--- Policy ---")
    sources = load_sources("policy")
    for source in sources:
        print(f"Fetching: {source}")
        items = fetch_rss_feed(source, "policy")
        all_items.extend(items)
    
    # 5. Open Source (GitHub)
    print("\n--- Open Source ---")
    print("Fetching GitHub trending...")
    items = fetch_github_trending()
    all_items.extend(items)
    
    # Save raw data
    output_file = os.path.join(SKILL_ROOT, "data/raw/intelligence.json")
    with open(output_file, "w") as f:
        json.dump(all_items, f, indent=2, ensure_ascii=False)
    
    # Print summary
    categories = {}
    for item in all_items:
        cat = item.get("category", "unknown")
        categories[cat] = categories.get(cat, 0) + 1
    
    print(f"\n=== Summary ===")
    print(f"Total items: {len(all_items)}")
    for cat, count in categories.items():
        print(f"  {cat}: {count}")
    
    if len(all_items) == 0:
        print("\nNote: If fetching 0 items, it may be because:")
        print("  - Daily mode: no news in last 24 hours")
        print("  - arXiv: does not publish on weekends")
    
    print(f"\nSaved to: {output_file}")


if __name__ == "__main__":
    main()

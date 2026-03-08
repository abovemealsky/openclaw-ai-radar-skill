#!/usr/bin/env python3
"""
Fetch research papers from arXiv.
"""
import json
import os
from datetime import datetime
from dateutil import parser as date_parser
import feedparser

# Get the skill root directory (parent of scripts/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)

SOURCES_FILE = os.path.join(SKILL_ROOT, "sources/research_sources.json")
OUTPUT_FILE = os.path.join(SKILL_ROOT, "data/raw/research.json")


def load_sources():
    """Load arXiv sources from JSON config."""
    with open(SOURCES_FILE, "r") as f:
        data = json.load(f)
    return data.get("sources", [])


def fetch_arxiv_feed(source_url):
    """Fetch arXiv RSS feed."""
    try:
        feed = feedparser.parse(source_url)
        entries = []
        for entry in feed.entries[:10]:
            # Extract published date
            published = ""
            if hasattr(entry, "published"):
                try:
                    dt = date_parser.parse(entry.published)
                    published = dt.strftime("%Y-%m-%d")
                except:
                    published = datetime.now().strftime("%Y-%m-%d")
            
            # Determine category from URL
            source = "arXiv"
            if "cs.AI" in source_url:
                source = "arXiv CS.AI"
            elif "cs.CL" in source_url:
                source = "arXiv CS.CL"
            elif "cs.LG" in source_url:
                source = "arXiv CS.LG"
            
            # Clean title (remove newlines)
            title = entry.get("title", "").replace("\n", " ").strip()
            
            entries.append({
                "title": title,
                "link": entry.get("link", ""),
                "published": published,
                "source": source
            })
        return entries
    except Exception as e:
        print(f"Error fetching {source_url}: {e}")
        return []


def main():
    """Main function to fetch all research papers."""
    os.makedirs("data/raw", exist_ok=True)
    
    sources = load_sources()
    print(f"Fetching research from {len(sources)} sources...")
    
    all_items = []
    for source in sources:
        print(f"Fetching: {source}")
        items = fetch_arxiv_feed(source)
        all_items.extend(items)
    
    with open(OUTPUT_FILE, "w") as f:
        json.dump(all_items, f, indent=2, ensure_ascii=False)
    
    print(f"Fetched {len(all_items)} research papers -> {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

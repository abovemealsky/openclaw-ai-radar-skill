#!/usr/bin/env python3
"""
Normalize items from different sources into a unified format.
"""
import json
import os

NEWS_FILE = "data/raw/news.json"
RESEARCH_FILE = "data/raw/research.json"
OPEN_SOURCE_FILE = "data/raw/open_source.json"
OUTPUT_FILE = "data/processed/items.json"


def load_json(filepath):
    """Load JSON file."""
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: {filepath} not found")
        return []
    except json.JSONDecodeError as e:
        print(f"Error parsing {filepath}: {e}")
        return []


def normalize_news(news_items):
    """Normalize news items."""
    normalized = []
    for item in news_items:
        normalized.append({
            "category": "news",
            "title": item.get("title", ""),
            "source": item.get("source", "news"),
            "url": item.get("link", ""),
            "summary": item.get("title", ""),
            "published": item.get("published", "")
        })
    return normalized


def normalize_research(research_items):
    """Normalize research items."""
    normalized = []
    for item in research_items:
        normalized.append({
            "category": "research",
            "title": item.get("title", ""),
            "source": item.get("source", "arxiv"),
            "url": item.get("link", ""),
            "summary": item.get("title", ""),
            "published": item.get("published", "")
        })
    return normalized


def normalize_open_source(open_source_items):
    """Normalize open source items."""
    normalized = []
    for item in open_source_items:
        normalized.append({
            "category": "open_source",
            "title": item.get("repo_name", ""),
            "source": "github",
            "url": item.get("url", ""),
            "summary": item.get("description", ""),
            "language": item.get("language", ""),
            "published": ""
        })
    return normalized


def main():
    """Main function to normalize all items."""
    os.makedirs("data/processed", exist_ok=True)
    
    print("Normalizing items...")
    
    # Load raw data
    news = load_json(NEWS_FILE)
    research = load_json(RESEARCH_FILE)
    open_source = load_json(OPEN_SOURCE_FILE)
    
    # Normalize
    normalized = []
    normalized.extend(normalize_news(news))
    normalized.extend(normalize_research(research))
    normalized.extend(normalize_open_source(open_source))
    
    # Save
    with open(OUTPUT_FILE, "w") as f:
        json.dump(normalized, f, indent=2, ensure_ascii=False)
    
    print(f"Normalized {len(normalized)} items -> {OUTPUT_FILE}")
    print(f"  - News: {len(news)}")
    print(f"  - Research: {len(research)}")
    print(f"  - Open Source: {len(open_source)}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Generate daily brief from normalized items.
"""
import json
import os
from datetime import datetime

# Get the skill root directory (parent of scripts/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)

ITEMS_FILE = os.path.join(SKILL_ROOT, "data/processed/items.json")
OUTPUT_FILE = os.path.join(SKILL_ROOT, "data/processed/daily_brief.md")


def load_items():
    """Load normalized items."""
    try:
        with open(ITEMS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: {ITEMS_FILE} not found")
        return []
    except json.JSONDecodeError as e:
        print(f"Error parsing {ITEMS_FILE}: {e}")
        return []


def categorize_items(items):
    """Categorize items by type."""
    news = []
    research = []
    open_source = []
    
    for item in items:
        category = item.get("category", "")
        if category == "news":
            news.append(item)
        elif category == "research":
            research.append(item)
        elif category == "open_source":
            open_source.append(item)
    
    return news, research, open_source


def format_item(item, include_source=True):
    """Format a single item as markdown."""
    title = item.get("title", "")
    url = item.get("url", "")
    summary = item.get("summary", "")
    source = item.get("source", "")
    
    lines = []
    if summary and summary != title:
        lines.append(f"- **{title}**")
        lines.append(f"  {summary}")
    else:
        lines.append(f"- **{title}**")
    
    if include_source and source:
        lines.append(f"  Source: {source}")
    
    if url:
        lines.append(f"  [Link]({url})")
    
    return "\n".join(lines)


def generate_brief(news, research, open_source):
    """Generate the daily brief markdown."""
    today = datetime.now().strftime("%Y-%m-%d")
    
    lines = [
        f"# AI Radar — Daily Brief",
        f"",
        f"**Date:** {today}",
        f"",
        f"---",
        f"",
    ]
    
    # Key Updates (News)
    lines.append("## Key Updates")
    lines.append("")
    if news:
        for item in news[:5]:
            title = item.get("title", "")
            url = item.get("url", "")
            source = item.get("source", "")
            
            lines.append(f"- **{title}**")
            lines.append(f"  - Source: {source}")
            if url:
                lines.append(f"  - [Read more]({url})")
            lines.append("")
    else:
        lines.append("*No news updates available today.*")
        lines.append("")
    
    # Research Highlights
    lines.append("## Research Highlights")
    lines.append("")
    if research:
        for item in research[:5]:
            title = item.get("title", "")
            url = item.get("url", "")
            source = item.get("source", "")
            
            lines.append(f"- **{title}**")
            lines.append(f"  - Source: {source}")
            if url:
                lines.append(f"  - [Paper]({url})")
            lines.append("")
    else:
        lines.append("*No research papers available today.*")
        lines.append("")
    
    # Open Source
    lines.append("## Open Source")
    lines.append("")
    if open_source:
        for item in open_source[:5]:
            repo_name = item.get("title", "")
            url = item.get("url", "")
            language = item.get("language", "")
            
            lines.append(f"- **{repo_name}**")
            if language:
                lines.append(f"  - Language: {language}")
            if url:
                lines.append(f"  - [View]({url})")
            lines.append("")
    else:
        lines.append("*No trending repositories available today.*")
        lines.append("")
    
    # Industry Signals
    lines.append("## Industry Signals")
    lines.append("")
    lines.append("AI product launches, research papers, and open-source projects continue to show strong momentum.")
    lines.append("")
    lines.append("Key trends:")
    lines.append("- Agent and workflow automation remain hot topics")
    lines.append("- Multimodal models are gaining adoption")
    lines.append("- Open-source AI tools are becoming more production-ready")
    lines.append("")
    
    # Quick Take
    lines.append("## Quick Take")
    lines.append("")
    lines.append("The AI ecosystem continues to evolve rapidly. Focus on Agent frameworks and multimodal capabilities as key areas to watch.")
    lines.append("")
    
    return "\n".join(lines)


def main():
    """Main function to generate daily brief."""
    print("Generating daily brief...")
    
    items = load_items()
    news, research, open_source = categorize_items(items)
    
    brief = generate_brief(news, research, open_source)
    
    os.makedirs("data/processed", exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        f.write(brief)
    
    print(f"Daily brief generated -> {OUTPUT_FILE}")
    print(f"  - News items: {len(news)}")
    print(f"  - Research papers: {len(research)}")
    print(f"  - Open source repos: {len(open_source)}")


if __name__ == "__main__":
    main()

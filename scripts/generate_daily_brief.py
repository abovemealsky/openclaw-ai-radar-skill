#!/usr/bin/env python3
"""
Generate daily brief from normalized intelligence items.
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
    categories = {
        "model_releases": [],
        "research": [],
        "open_source": [],
        "industry": [],
        "policy": []
    }
    
    for item in items:
        category = item.get("category", "industry")
        if category in categories:
            categories[category].append(item)
        else:
            categories["industry"].append(item)
    
    return categories


def generate_brief(categories):
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
    
    # Category titles
    category_titles = {
        "model_releases": "Model Releases",
        "research": "Research Highlights",
        "open_source": "Open Source",
        "industry": "Industry Developments",
        "policy": "Policy & Governance"
    }
    
    # Generate each section
    for cat_key, cat_title in category_titles.items():
        lines.append(f"## {cat_title}")
        lines.append("")
        
        items = categories.get(cat_key, [])
        if items:
            # Limit to 5 items per category
            for item in items[:5]:
                title = item.get("title", "")
                url = item.get("url", "")
                source = item.get("source", "")
                
                lines.append(f"- **{title}**")
                if source:
                    lines.append(f"  - Source: {source}")
                if url:
                    lines.append(f"  - [Link]({url})")
                lines.append("")
        else:
            lines.append(f"*No items in this category.*")
            lines.append("")
    
    # Quick Take
    lines.append("## Quick Take")
    lines.append("")
    lines.append("The AI ecosystem continues to evolve rapidly. Focus on model releases, agent frameworks, and regulatory developments as key areas to watch.")
    lines.append("")
    
    return "\n".join(lines)


def main():
    """Main function to generate daily brief."""
    print("Generating daily brief...")
    
    items = load_items()
    categories = categorize_items(items)
    
    brief = generate_brief(categories)
    
    os.makedirs(os.path.join(SKILL_ROOT, "data/processed"), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        f.write(brief)
    
    # Print summary
    print(f"Daily brief generated -> {OUTPUT_FILE}")
    print("Items per category:")
    for cat, items_list in categories.items():
        print(f"  - {cat}: {len(items_list)}")


if __name__ == "__main__":
    main()

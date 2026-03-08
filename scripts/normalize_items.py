#!/usr/bin/env python3
"""
Normalize intelligence items into a unified format.
"""
import json
import os

# Get the skill root directory (parent of scripts/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)

INPUT_FILE = os.path.join(SKILL_ROOT, "data/raw/intelligence.json")
OUTPUT_FILE = os.path.join(SKILL_ROOT, "data/processed/items.json")


def load_items():
    """Load raw intelligence items."""
    try:
        with open(INPUT_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: {INPUT_FILE} not found")
        return []
    except json.JSONDecodeError as e:
        print(f"Error parsing {INPUT_FILE}: {e}")
        return []


def normalize_item(item):
    """Normalize a single item to standard format."""
    # Handle GitHub items which have different structure
    if item.get("category") == "open_source":
        return {
            "category": "open_source",
            "title": item.get("title", ""),
            "source": item.get("source", "GitHub"),
            "url": item.get("link", ""),
            "summary": item.get("description", item.get("title", "")),
            "language": item.get("language", ""),
            "published": item.get("published", "")
        }
    
    # Handle RSS feed items
    return {
        "category": item.get("category", "industry"),
        "title": item.get("title", ""),
        "source": item.get("source", ""),
        "url": item.get("link", ""),
        "summary": item.get("title", ""),  # Use title as summary for now
        "published": item.get("published", "")
    }


def main():
    """Main function to normalize items."""
    os.makedirs(os.path.join(SKILL_ROOT, "data/processed"), exist_ok=True)
    
    print("Normalizing intelligence items...")
    
    items = load_items()
    normalized = [normalize_item(item) for item in items]
    
    # Count by category
    categories = {}
    for item in normalized:
        cat = item.get("category", "unknown")
        categories[cat] = categories.get(cat, 0) + 1
    
    # Save
    with open(OUTPUT_FILE, "w") as f:
        json.dump(normalized, f, indent=2, ensure_ascii=False)
    
    print(f"Normalized {len(normalized)} items -> {OUTPUT_FILE}")
    print("Categories:")
    for cat, count in categories.items():
        print(f"  - {cat}: {count}")


if __name__ == "__main__":
    main()

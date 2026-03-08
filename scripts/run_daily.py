#!/usr/bin/env python3
"""
Run the daily or weekly AI Radar pipeline.
"""
import subprocess
import sys
import os

# Change to script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)
os.chdir(SCRIPT_DIR)

# Get mode from argument or environment
MODE = "daily"
if len(sys.argv) > 1:
    MODE = sys.argv[1].lower()
    if MODE not in ["daily", "weekly"]:
        print(f"Invalid mode: {MODE}. Use 'daily' or 'weekly'")
        sys.exit(1)

# Set environment variable for scripts to use
os.environ["RADAR_MODE"] = MODE


def run_script(script_name):
    """Run a Python script and handle errors."""
    print(f"\n{'='*50}")
    print(f"Running: {script_name} ({MODE} mode)")
    print("="*50)
    
    result = subprocess.run(
        [sys.executable, script_name],
        capture_output=True,
        text=True,
        cwd=SCRIPT_DIR
    )
    
    if result.returncode != 0:
        print(f"Error running {script_name}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        return False
    
    print(result.stdout)
    return True


def main():
    """Run the full pipeline."""
    mode_str = "Daily" if MODE == "daily" else "Weekly"
    print("="*50)
    print(f"AI Radar - {mode_str} Brief Pipeline")
    print("="*50)
    print(f"Mode: {MODE} (last {'24 hours' if MODE == 'daily' else '7 days'})")
    
    # Pipeline scripts in order
    scripts = [
        "fetch_news.py",
        "fetch_arxiv.py",
        "fetch_github.py",
        "normalize_items.py",
        "generate_daily_brief.py"
    ]
    
    for script in scripts:
        if not run_script(script):
            print(f"\n❌ Pipeline failed at {script}")
            sys.exit(1)
    
    print("\n" + "="*50)
    print(f"✅ AI Radar {mode_str.lower()} brief generated successfully!")
    print("="*50)
    print(f"\nOutput file: {SKILL_ROOT}/data/processed/daily_brief.md")


if __name__ == "__main__":
    main()

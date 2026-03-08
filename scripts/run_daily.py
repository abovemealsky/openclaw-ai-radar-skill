#!/usr/bin/env python3
"""
Run the daily AI Radar pipeline.
"""
import subprocess
import sys
import os

# Change to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def run_script(script_name):
    """Run a Python script and handle errors."""
    print(f"\n{'='*50}")
    print(f"Running: {script_name}")
    print("="*50)
    
    result = subprocess.run(
        [sys.executable, script_name],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"Error running {script_name}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        return False
    
    print(result.stdout)
    return True


def main():
    """Run the full daily pipeline."""
    print("="*50)
    print("AI Radar - Daily Brief Pipeline")
    print("="*50)
    
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
    print("✅ AI Radar daily brief generated successfully!")
    print("="*50)
    print("\nOutput file: data/processed/daily_brief.md")


if __name__ == "__main__":
    main()

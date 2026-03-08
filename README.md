# AI Radar

AI Radar is an OpenClaw skill that generates high-signal AI intelligence briefs from:
- model releases
- research papers
- open-source projects
- industry news

Instead of listing every AI headline, AI Radar highlights what actually matters and explains why it matters.

## Features

AI Radar summarizes developments across four categories.

### Key Updates
Important announcements from major AI labs. Examples:
- OpenAI
- Anthropic
- Google DeepMind
- Meta AI

### Research Highlights
Notable papers from:
- arXiv
- Hugging Face papers
- Papers With Code

### Open Source
Trending AI repositories and tools from:
- GitHub Trending
- Hugging Face models

### Industry Signals
Patterns or shifts happening in the AI ecosystem.

## MVP Status

Current version supports:
- ✅ Fetch AI news from RSS sources
- ✅ Fetch arXiv papers
- ✅ Fetch GitHub trending repositories
- ✅ Generate daily brief in Markdown format

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/abovemealsky/openclaw-ai-radar-skill.git
cd openclaw-ai-radar-skill
pip install -r requirements.txt
```

## Usage

### Generate Daily Brief

```bash
cd scripts
python run_daily.py
```

### Individual Scripts

You can also run each script individually:

```bash
python scripts/fetch_news.py       # Fetch AI news
python scripts/fetch_arxiv.py      # Fetch research papers
python scripts/fetch_github.py      # Fetch GitHub trending
python scripts/normalize_items.py   # Normalize data
python scripts/generate_daily_brief.py  # Generate brief
```

## Output

Generated files are saved to:
- `data/raw/news.json` - Raw news data
- `data/raw/research.json` - Raw research data
- `data/raw/open_source.json` - Raw GitHub data
- `data/processed/items.json` - Normalized items
- `data/processed/daily_brief.md` - Final daily brief (Markdown)

## Configuration

Copy `config.example.json` to `config.json` and adjust settings:

```json
{
  "update_frequency": "daily",
  "max_items_per_section": 5
}
```

## Project Structure

```
openclaw-ai-radar-skill/
├── SKILL.md                    # OpenClaw skill definition
├── README.md                   # This file
├── requirements.txt             # Python dependencies
├── config.example.json         # Configuration template
├── prompts/                    # Prompt templates
│   ├── daily_brief.md
│   ├── weekly_brief.md
│   └── analyst_summary.md
├── sources/                    # Data source configs
│   ├── news_sources.json
│   ├── research_sources.json
│   └── open_source_sources.json
├── scripts/                    # Python scripts
│   ├── fetch_news.py
│   ├── fetch_arxiv.py
│   ├── fetch_github.py
│   ├── normalize_items.py
│   ├── generate_daily_brief.py
│   └── run_daily.py
├── data/                       # Data files
│   ├── raw/                   # Raw fetched data
│   └── processed/             # Processed & generated
├── examples/                  # Example outputs
│   ├── daily_output.md
│   └── weekly_output.md
```

## Example Output

See `examples/daily_output.md` for a sample daily brief.

## License

MIT

---

Built with ❤️ by OpenClaw

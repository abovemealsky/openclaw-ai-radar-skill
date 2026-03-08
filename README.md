# AI Radar

AI Radar is a structured AI intelligence skill that provides high-signal briefings on artificial intelligence developments. Instead of overwhelming you with every headline, AI Radar organizes information into meaningful categories and highlights what actually matters.

## Five Intelligence Layers

AI Radar monitors five key areas of AI development:

1. **Model Releases** - Major AI model launches, product updates, and API announcements from OpenAI, Anthropic, Google, Meta, and other labs.

2. **Research** - Important papers from arXiv, technical innovations, and research signals that shape the future of AI.

3. **Open Source** - Trending repositories, popular models, and open-source tools that developers are actively using.

4. **Industry** - Company news, market trends, product launches, and commercial applications of AI technology.

5. **Policy & Governance** - Regulatory developments, safety initiatives, and policy discussions around AI.

## Target Audience

AI Radar is designed for:
- **AI Product Managers** - Stay informed about competitive landscape
- **Researchers** - Track papers and technical innovations
- **Developers** - Discover new tools and frameworks
- **Founders** - Monitor market trends and opportunities
- **Analysts** - Get structured intelligence for analysis

## Signal Over Noise

AI Radar focuses on delivering signal, not noise. Each briefing:
- Organizes information into clear categories
- Highlights why each development matters
- Provides links to original sources
- Keeps content concise and actionable

## Zero-Config, No API Key Required

AI Radar runs completely offline without any external API dependencies:
- No OpenAI API key needed
- No Anthropic API key needed
- No Google API key needed
- Fetches directly from public RSS feeds and web pages

## Installation

```bash
git clone https://github.com/abovemealsky/openclaw-ai-radar-skill.git
cd openclaw-ai-radar-skill
pip install -r requirements.txt
```

## Usage

### Generate Daily Brief (last 24 hours)

```bash
cd scripts
python run_daily.py daily
```

### Generate Weekly Brief (last 7 days)

```bash
cd scripts
python run_daily.py weekly
```

## Output

Generated files are saved to:
- `data/raw/intelligence.json` - Raw fetched data
- `data/processed/items.json` - Normalized items
- `data/processed/daily_brief.md` - Formatted brief (Markdown)

## Configuration

The skill uses these source categories:
- `sources/model_sources.json` - AI model and product blogs
- `sources/research_sources.json` - Academic papers and research
- `sources/open_source_sources.json` - GitHub and HuggingFace
- `sources/industry_sources.json` - Tech news and industry coverage
- `sources/policy_sources.json` - Policy and governance news

## Example Output

See `examples/daily_output.md` for a sample daily brief.

## Project Structure

```
openclaw-ai-radar-skill/
├── SKILL.md                    # OpenClaw skill definition
├── README.md                   # This file
├── requirements.txt             # Python dependencies
├── config.example.json         # Configuration template
├── prompts/                    # Prompt templates
│   ├── daily_brief.md
│   └── weekly_brief.md
├── sources/                    # Data source configs
│   ├── model_sources.json
│   ├── research_sources.json
│   ├── open_source_sources.json
│   ├── industry_sources.json
│   └── policy_sources.json
├── scripts/                    # Python scripts
│   ├── fetch_intelligence.py
│   ├── normalize_items.py
│   ├── generate_daily_brief.py
│   └── run_daily.py
├── data/                       # Data files
│   ├── raw/                   # Raw fetched data
│   └── processed/             # Processed & generated
└── examples/                  # Example outputs
    └── daily_output.md
```

## License

MIT

---

Built with ❤️ by OpenClaw

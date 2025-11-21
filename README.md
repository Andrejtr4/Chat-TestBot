# EnBW Playwright Test Generator

An interactive AI agent that automatically generates Playwright test code from natural language descriptions. Simply describe what you want to test, and the agent generates ready-to-run test code using GPT-4.

## What It Does

- **AI-Powered Test Generation**: Describe a test scenario in plain language (e.g., "test clicking the tariff button and filling the postal code")
- **Interactive Chat Interface**: Simple CLI where you chat with the agent about tests you want to generate
- **Playwright Integration**: Generates valid Playwright test code that you can immediately run
- **OpenAI GPT-4**: Uses advanced language model to understand intent and generate high-quality test code
- **Bonus Features**: Includes web scraper for EnBW.com and Datev CSV exporter for data analysis

## Installation

1. **Install dependencies** (uses `uv` package manager): https://docs.astral.sh/uv/getting-started/installation/#next-steps
   ```bash
   pip install uv
   uv sync
   ```

3. **Set up environment** - Create a `.env` file with your OpenAI API key:
   ```bash
   echo "OPENAPI_KEY=your-openai-api-key-here" > .env
   ```
   Get your API key from [OpenAI platform](https://platform.openai.com/api-keys)

## Quick Start

**Run the interactive test generator:**
```bash
uv run main.py
```

Then interact with the agent:
```
You: test clicking the tariff button on the EnBW website
Agent: [Generates Playwright test code for that scenario]

You: add a step to fill in postal code 70173
Agent: [Generates updated test code with that step]

You: save
Agent: [Saves generated test to tests/generated_test.py]
```

## How to Use

### 1. Start the Agent
```bash
uv run main.py
```

### 2. Describe Your Test
Type natural language descriptions of what you want to test:
```
test visiting the EnBW website and navigating to the tariff page
test clicking the compare tariffs button and checking the result
test scrolling through the tariff details section
```

### 3. Generate Code
The agent generates complete Playwright test code that you can:
- View in the chat
- Copy and paste
- Modify as needed
- Save to a file (type `save`)

### 4. Run Tests
Once you have generated test code:
```bash
# Install pytest if needed
pip install pytest

# Run the generated test
pytest tests/generated_test.py -v
```

## Bonus: Web Scraper

**Scrape and analyze EnBW.com content:**
```bash
uv run python scout/client.py
```

This will:
1. Scrape key pages from https://www.enbw.com
2. Analyze content with GPT-4
3. Export structured data to CSV (Datev format)

Output file: `enbw_export_YYYYMMDD_HHMMSS.csv`

## Troubleshooting

### "No module named 'scout'"
**Solution**: Always run from project root directory:
```bash
# ✅ Correct
cd /Users/andreas/Documents/EnBW/Praxisphasen/3.\ Praxisphase/mcp-intro
uv run python scout/client_test_generator.py

# ❌ Wrong
cd scout
python client_test_generator.py
```

### "OPENAPI_KEY not found"
**Solution**: Verify `.env` file exists in project root with correct key:
```bash
cat .env  # Should show: OPENAPI_KEY=sk-proj-...
```

### Agent returns no output
**Solution**: 
1. Check API key is valid: Visit https://platform.openai.com/api-keys
2. Verify .env file: `cat .env | grep OPENAPI_KEY`
3. Check internet connection
4. Try simpler prompt: instead of long description, use shorter request

### Import warnings in IDE
**Note**: IDE may show red squiggles for imports even though they work fine. This is normal with uv-managed environments. Everything works correctly at runtime.

## Project Structure

```
mcp-intro/
├── README.md                          # This file
├── pyproject.toml                     # Project configuration & dependencies
├── .env                              # OpenAI API key (not in git)
├── uv.lock                           # Dependency lock file
│
├── scout/                            # Main package
│   ├── client_test_generator.py      # Interactive test generation CLI
│   ├── client.py                     # Web scraper + CSV exporter
│   │
│   ├── agents/                       # AI agent logic
│   │   ├── playwright_test_generator.py      # Core LangGraph agent
│   │   └── test_generator_mcp_server.py      # MCP server wrapper
│   │
│   ├── my_mcp/                       # MCP server configurations
│   │   ├── config.py
│   │   ├── mcp_config.json
│   │   └── local_servers/
│   │       ├── enbw.py              # EnBW web scraper server
│   │       └── weather.py
│   │
│   └── tests/                        # Generated test files will go here
│       └── __init__.py
```

## Technology Stack

- **Python 3.13+** - Runtime
- **LangGraph** - Agentic orchestration framework
- **LangChain** - LLM integration framework
- **OpenAI API** - GPT-4 language model
- **Playwright** - Browser automation
- **MCP (Model Context Protocol)** - Server framework for tools
- **BeautifulSoup4** - HTML parsing for scraping
- **httpx** - HTTP client for web requests

## Next Steps

1. Make sure `.env` has valid `OPENAPI_KEY`
2. Run: `uv run python scout/client_test_generator.py`
3. Describe a test you want in plain English
4. Watch the agent generate Playwright code
5. Save the code and run it with pytest

## Questions?

Common issues are covered in the **Troubleshooting** section above. If you encounter something else, check:
- `.env` file exists and contains valid API key
- Running from project root directory
- Dependencies installed: `uv sync`

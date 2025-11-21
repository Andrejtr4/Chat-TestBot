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

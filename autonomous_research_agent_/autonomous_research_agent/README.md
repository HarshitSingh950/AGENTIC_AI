# Autonomous Research Agent (LangChain)

A GitHub-ready Python project for the assignment **"Autonomous Research Agent"**.

This project builds an AI research agent that:
- accepts a topic as input,
- searches the web,
- gathers knowledge from Wikipedia,
- analyzes the collected information,
- and generates a structured final report.

## Features

- Uses **LangChain** for agent orchestration
- Uses an **LLM** from **OpenAI** or **Anthropic**
- Includes **2 tools**:
  - `web_search` → live web search using Tavily
  - `wikipedia_search` → background knowledge using Wikipedia
- Produces a report with the required sections:
  - Cover Page
  - Title
  - Introduction
  - Key Findings
  - Challenges
  - Future Scope
  - Conclusion

## Project Structure

```text
autonomous_research_agent/
├── .env.example
├── README.md
├── requirements.txt
├── sample_outputs/
│   ├── sample_output_ai_healthcare.md
│   └── sample_output_ai_education.md
└── src/
    ├── __init__.py
    ├── main.py
    ├── prompts.py
    └── tools.py
```

## Installation

```bash
pip install -r requirements.txt
```

## Environment Setup

Create a `.env` file in the project root and copy values from `.env.example`.

Example:

```env
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

If you want to use Anthropic instead:

```env
LLM_PROVIDER=anthropic
LLM_MODEL=claude-sonnet-4-5
ANTHROPIC_API_KEY=your_anthropic_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

## How It Works

### Step 1: Research phase
A LangChain agent is created with two tools:
- `web_search(query)`
- `wikipedia_search(query)`

The agent investigates the given topic and produces structured research notes.

### Step 2: Report writing phase
The same LLM is then used to convert the research notes into a polished markdown report.

## Run the Project

From the project root:

```bash
python -m src.main "Impact of AI in Healthcare"
```

You can also select a provider and model explicitly:

```bash
python -m src.main "Impact of AI in Healthcare" --provider openai --model gpt-4o-mini
```

Generated reports are saved in the `outputs/` folder.

## Example Topics

- `Impact of AI in Healthcare`
- `Role of AI in Education`
- `Blockchain in Supply Chain Management`
- `Future of Renewable Energy`

## Assignment Mapping

### Requirements checklist

- **Use LangChain** → Yes
- **Use any LLM (OpenAI / Anthropic)** → Yes
- **Use at least 2 tools** → Yes
- **Web Search Tool** → Yes
- **Knowledge Tool (Wikipedia / PDF)** → Yes, Wikipedia
- **Implement an Agent (ReAct or similar)** → Yes, tool-using LangChain agent
- **Generate structured report** → Yes

## Notes for Submission

For your final submission, you can:
1. Upload this folder to a GitHub repository.
2. Add screenshots or terminal outputs if your instructor wants proof of execution.
3. Include the two sample reports from `sample_outputs/`.

## Possible Enhancements

- Add PDF ingestion as an additional knowledge source
- Export reports to PDF or DOCX
- Add citations and source scoring
- Save intermediate research notes as JSON
- Add Streamlit or Gradio UI


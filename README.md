# Autonomous Research Agent (LangChain)

## Objective
Build an AI agent that can automatically research a topic and generate a structured report.

## Problem Statement
Create an Autonomous Research Agent using LangChain that can:
- Search information from the web
- Analyze and summarize data
- Generate a detailed report

## Features
- Takes a topic as input
- Uses a Web Search Tool
- Uses a Wikipedia Knowledge Tool
- Uses LangChain Agent
- Generates a structured report

## Requirements Fulfilled
- LangChain used
- OpenAI LLM used
- Two tools implemented:
  - Web Search Tool
  - Knowledge Tool (Wikipedia)
- Agent implemented

## Project Structure
```text
autonomous-research-agent/
├── main.py
├── requirements.txt
├── .env.example
├── README.md
└── sample_outputs/
    ├── sample_output_1_ai_healthcare.md
    └── sample_output_2_online_education.md
```

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/autonomous-research-agent.git
cd autonomous-research-agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create `.env` file
Create a `.env` file and add your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

## Run the project
```bash
python main.py
```

## Example Topic
```text
Impact of AI in Healthcare
```

## Output Format
The report contains:
- Cover Page
- Title
- Introduction
- Key Findings
- Challenges
- Future Scope
- Conclusion
- Sources Used

## Sample Topics
1. Impact of AI in Healthcare
2. Role of Artificial Intelligence in Online Education

## Submission
- Source Code (GitHub)
- 2 Sample Outputs

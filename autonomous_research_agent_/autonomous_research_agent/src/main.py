from __future__ import annotations

import argparse
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from langchain.agents import create_agent

from src.prompts import RESEARCH_SYSTEM_PROMPT, REPORT_PROMPT
from src.tools import web_search, wikipedia_search


OUTPUT_DIR = Path("outputs")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Autonomous Research Agent using LangChain"
    )
    parser.add_argument(
        "topic",
        type=str,
        help='Research topic, for example: "Impact of AI in Healthcare"',
    )
    parser.add_argument(
        "--provider",
        choices=["openai", "anthropic"],
        default=os.getenv("LLM_PROVIDER", "openai"),
        help="LLM provider to use",
    )
    parser.add_argument(
        "--model",
        default=os.getenv("LLM_MODEL", "gpt-4o-mini"),
        help="Model name for the selected provider",
    )
    parser.add_argument(
        "--output-dir",
        default=str(OUTPUT_DIR),
        help="Directory where the generated report will be saved",
    )
    return parser.parse_args()


def build_model(provider: str, model_name: str):
    if provider == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(model=model_name, temperature=0)

    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic

        return ChatAnthropic(model=model_name, temperature=0)

    raise ValueError(f"Unsupported provider: {provider}")


def extract_text(result: Any) -> str:
    """Safely extract the final assistant text from a LangChain agent response."""
    if isinstance(result, str):
        return result

    if isinstance(result, dict) and "messages" in result and result["messages"]:
        last = result["messages"][-1]
        content = getattr(last, "content", last.get("content", ""))

        if isinstance(content, str):
            return content

        if isinstance(content, list):
            parts = []
            for item in content:
                if isinstance(item, str):
                    parts.append(item)
                elif isinstance(item, dict):
                    parts.append(str(item.get("text", "")))
                else:
                    parts.append(str(item))
            return "\n".join(part for part in parts if part)

        return str(content)

    return str(result)


def sanitize_filename(text: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "_", text).strip("_").lower()
    return cleaned[:80] or "research_report"


def create_research_notes(agent, topic: str) -> str:
    user_prompt = f"""
Research the topic: {topic}

Instructions:
- Use the web search tool.
- Use the Wikipedia search tool.
- Gather reliable, balanced insights.
- Organize the result as structured research notes.
- Keep the output concise but informative.
""".strip()

    result = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": user_prompt},
            ]
        }
    )
    return extract_text(result)


def create_final_report(model, topic: str, research_notes: str) -> str:
    prompt = REPORT_PROMPT.format(topic=topic, research_notes=research_notes)
    response = model.invoke(prompt)
    return extract_text(response)


def save_report(topic: str, report_text: str, output_dir: str) -> Path:
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{sanitize_filename(topic)}_{timestamp}.md"
    path = out_dir / filename
    path.write_text(report_text, encoding="utf-8")
    return path


def main() -> None:
    load_dotenv()
    args = parse_args()

    model = build_model(args.provider, args.model)
    tools = [web_search, wikipedia_search]

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=RESEARCH_SYSTEM_PROMPT,
    )

    print(f"\n[1/3] Researching topic: {args.topic}\n")
    research_notes = create_research_notes(agent, args.topic)
    print(research_notes)

    print("\n[2/3] Writing final report...\n")
    final_report = create_final_report(model, args.topic, research_notes)

    report_path = save_report(args.topic, final_report, args.output_dir)

    print("[3/3] Done. Report saved to:")
    print(report_path.resolve())
    print("\nPreview:\n")
    print(final_report)


if __name__ == "__main__":
    main()

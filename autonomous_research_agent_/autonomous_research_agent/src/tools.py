from __future__ import annotations

import os
from typing import List

from tavily import TavilyClient
from langchain_community.retrievers import WikipediaRetriever


MAX_WEB_RESULTS = int(os.getenv("MAX_WEB_RESULTS", "5"))
MAX_WIKI_DOCS = int(os.getenv("MAX_WIKI_DOCS", "3"))
MAX_SNIPPET_CHARS = int(os.getenv("MAX_SNIPPET_CHARS", "800"))


def _truncate(text: str, limit: int = MAX_SNIPPET_CHARS) -> str:
    if not text:
        return ""
    clean = " ".join(text.split())
    return clean if len(clean) <= limit else clean[: limit - 3] + "..."


def web_search(query: str) -> str:
    """Search the live web for recent and relevant information about a topic."""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "TAVILY_API_KEY is missing. Add it to your environment or .env file."

    client = TavilyClient(api_key=api_key)

    try:
        response = client.search(query=query, max_results=MAX_WEB_RESULTS)
    except Exception as exc:  # pragma: no cover
        return f"Web search failed: {exc}"

    results = response.get("results", [])
    if not results:
        return "No web results found."

    formatted = []
    for i, item in enumerate(results, start=1):
        title = item.get("title", "Untitled")
        url = item.get("url", "")
        content = _truncate(item.get("content", ""))
        formatted.append(
            f"Result {i}\nTitle: {title}\nURL: {url}\nSnippet: {content}"
        )

    return "\n\n".join(formatted)



def wikipedia_search(query: str) -> str:
    """Search Wikipedia for background knowledge and concise topic summaries."""
    try:
        retriever = WikipediaRetriever(load_max_docs=MAX_WIKI_DOCS)
        docs = retriever.invoke(query)
    except Exception as exc:  # pragma: no cover
        return f"Wikipedia lookup failed: {exc}"

    if not docs:
        return "No Wikipedia results found."

    entries: List[str] = []
    for i, doc in enumerate(docs, start=1):
        title = doc.metadata.get("title", f"Wikipedia Doc {i}")
        source = doc.metadata.get("source", "wikipedia.org")
        summary = _truncate(doc.page_content)
        entries.append(
            f"Entry {i}\nTitle: {title}\nSource: {source}\nSummary: {summary}"
        )

    return "\n\n".join(entries)

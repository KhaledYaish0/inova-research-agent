import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

tavily_api_key = os.getenv("TAVILY_API_KEY")


def search_web(query: str) -> str:
    if not tavily_api_key:
        return "Search is unavailable because TAVILY_API_KEY is missing."

    client = TavilyClient(api_key=tavily_api_key)

    result = client.search(query=query, max_results=3)

    formatted = []
    for item in result.get("results", []):
        title = item.get("title", "No title")
        content = item.get("content", "No content")
        url = item.get("url", "No URL")
        formatted.append(f"Title: {title}\nContent: {content}\nURL: {url}")

    return "\n\n".join(formatted) if formatted else "No search results found."
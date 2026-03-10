from typing import TypedDict, Optional


class AgentState(TypedDict):
    question: str
    route: Optional[str]
    search_results: Optional[str]
    response: Optional[str]
from app.agent.state import AgentState
from app.llm import ask_llm
from app.agent.tools import search_web


def router_node(state: AgentState) -> AgentState:
    question = state["question"]

    prompt = f"""
You are a routing assistant.

Decide whether the user's question can be answered using general knowledge
or if it requires fresh/external information from the web.

Return only one word:
- general
- search

Question: {question}
""".strip()

    decision = ask_llm(
        prompt,
        system_prompt="You are a strict classifier. Return only 'general' or 'search'."
    ).strip().lower()

    if "search" in decision:
        route = "search"
    else:
        route = "general"

    print(f"[Router] Question: {question}")
    print(f"[Router] Decision: {route}")

    return {
        **state,
        "route": route
    }


def general_node(state: AgentState) -> AgentState:
    print("[General] Answering directly.")
    answer = ask_llm(state["question"])

    return {
        **state,
        "response": answer
    }


def search_node(state: AgentState) -> AgentState:
    print(f"[Search] Running search for: {state['question']}")
    results = search_web(state["question"])

    return {
        **state,
        "search_results": results
    }


def answer_with_search_node(state: AgentState) -> AgentState:
    print("[SearchAnswer] Building final answer from search results.")

    prompt = f"""
Answer the user's question using the search results below.

Question:
{state['question']}

Search Results:
{state.get('search_results', '')}
""".strip()

    answer = ask_llm(
        prompt,
        system_prompt="You are a helpful research assistant. Use the provided search results to answer clearly."
    )

    return {
        **state,
        "response": answer
    }
from fastapi import FastAPI, HTTPException
from langchain_core.messages import AIMessage, HumanMessage

from app.agent.graph import agent_graph
from app.database import (
    DatabaseConfigurationError,
    SessionLocal,
    get_engine,
)
from app.models import Base, Conversation
from app.schemas import QueryRequest, QueryResponse

app = FastAPI(title="Inova Research Agent API")

try:
    Base.metadata.create_all(bind=get_engine())
except DatabaseConfigurationError as exc:
    raise RuntimeError(f"Application startup failed: {exc}") from exc


@app.get("/")
def root():
    return {"message": "Inova Research Agent API is running."}


@app.get("/health")
def health():
    return {"status": "OK!"}


def build_thread_messages(thread_id: str, latest_user_text: str):
    db = SessionLocal()
    try:
        history = (
            db.query(Conversation)
            .filter(Conversation.thread_id == thread_id)
            .order_by(Conversation.created_at.asc(), Conversation.id.asc())
            .all()
        )
    finally:
        db.close()

    messages = []
    for item in history:
        messages.append(HumanMessage(content=item.question))
        messages.append(AIMessage(content=item.response))

    messages.append(HumanMessage(content=latest_user_text))
    return messages


from app.database import get_database_url

@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")

    try:
        print("DEBUG DATABASE_URL:", get_database_url())
        print("DEBUG thread_id:", request.thread_id)
        print("DEBUG text:", request.text)

        messages = build_thread_messages(request.thread_id, request.text)

        result = agent_graph.invoke(
            {
                "messages": messages,
                "route": None,
                "search_results": None,
            }
        )

        assistant_response = result["messages"][-1].content
        print("DEBUG assistant_response:", assistant_response)

        db = SessionLocal()
        try:
            conversation = Conversation(
                thread_id=request.thread_id,
                question=request.text,
                response=assistant_response,
            )

            print("DEBUG before add")
            db.add(conversation)

            print("DEBUG before flush")
            db.flush()

            print("DEBUG before commit")
            db.commit()

            db.refresh(conversation)
            print("DEBUG saved row id:", conversation.id)

        finally:
            db.close()

        return QueryResponse(response=assistant_response)

    except Exception as exc:
        print("DEBUG ERROR:", repr(exc))
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/history/{thread_id}")
def get_history(thread_id: str):
    db = SessionLocal()
    try:
        history = (
            db.query(Conversation)
            .filter(Conversation.thread_id == thread_id)
            .order_by(Conversation.created_at.asc(), Conversation.id.asc())
            .all()
        )

        return {
            "thread_id": thread_id,
            "messages": [
                {
                    "id": item.id,
                    "question": item.question,
                    "response": item.response,
                    "created_at": item.created_at,
                }
                for item in history
            ],
        }
    finally:
        db.close()
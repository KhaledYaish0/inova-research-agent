from fastapi import FastAPI, HTTPException
from app.schemas import QueryRequest, QueryResponse
from app.agent.graph import agent_graph

app = FastAPI(title="Inova Research Agent API")


@app.get("/")
def root():
    return {"message": "Inova Research Agent API is running."}


@app.get("/health")
def health():
    return {"status": "OK!"}


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")

    try:
        result = agent_graph.invoke(
            {
                "question": request.text,
                "route": None,
                "search_results": None,
                "response": None,
            }
        )

        return QueryResponse(response=result["response"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
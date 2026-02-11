# api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

from src.models.trademark import TrademarkApplication
from src.rag.input_adapter import structured_object_to_query
from src.rag.generate_answer import generate_rag_answer

app = FastAPI(
    title="TMEP Assist API",
    description="AI-powered Trademark Risk Assessment using RAG + TMEP",
    version="1.0.0"
)


class TrademarkRequest(BaseModel):
    data: Dict[str, Any]


@app.post("/analyze")
def analyze_trademark(request: TrademarkRequest):

    try:
        # Convert JSON → structured object
        app_obj = TrademarkApplication(request.data)

        # Convert structured object → deterministic query
        query = structured_object_to_query(app_obj)

        # Generate RAG answer
        result = generate_rag_answer(
            query=query,
            top_k=5
        )

        return {
            "status": "success",
            "analysis": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

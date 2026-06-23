from fastapi import APIRouter, HTTPException
from backend.models.schemas import QueryRequest, QueryResponse
from src.ingestion.embedder import Embedder
from src.extraction.conversation import ConversationEngine
from qdrant_client import QdrantClient

router = APIRouter()
embedder = Embedder()
qdrant = QdrantClient(host="localhost", port=6333)

# Store conversations in memory by conversation_id
conversations: dict = {}

def get_conversation(conversation_id: str) -> ConversationEngine:
    if conversation_id not in conversations:
        conversations[conversation_id] = ConversationEngine(embedder)
    return conversations[conversation_id]

def get_context(query: str, limit: int = 5) -> list:
    vector = embedder.embed_query(query)
    results = qdrant.query_points(
        collection_name="finsight",
        query=vector,
        limit=limit
    ).points
    return [r.payload["text"] for r in results]

@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        conversation = get_conversation(request.conversation_id)
        context = get_context(request.question)
        
        if not context:
            raise HTTPException(
                status_code=404, 
                detail="No documents found. Please upload a document first."
            )

        answer = conversation.chat(request.question, context)
        
        return QueryResponse(
            question=request.question,
            answer=answer,
            sources=context[:3]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reset/{conversation_id}")
async def reset_conversation(conversation_id: str):
    if conversation_id in conversations:
        conversations[conversation_id].reset()
    return {"message": f"Conversation {conversation_id} reset"}
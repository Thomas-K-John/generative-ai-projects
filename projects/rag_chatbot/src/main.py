import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag_retrieval import HybridRAGRetrieverModel

app = FastAPI(title="RAG-Based Chatbot Development for Government Technology")
retriever = HybridRAGRetrieverModel(db_path="../db/chroma_db")
executor = ThreadPoolExecutor(max_workers=10)

class MessageRequest(BaseModel):
    query: str

async def run_in_thread(func, *args):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, func, *args)

@app.post("/chat")
async def query_endpoint(request: MessageRequest):
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Empty query")
    try:
        result = await run_in_thread(retriever.invoke, query)
        return {"query": query, "response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "message": "System is healthy"}

@app.get("/stats")
def system_statistics():
    """System Statistics"""
    return {"status": "ok", "message": "CPU Count:" + str(os.cpu_count())}


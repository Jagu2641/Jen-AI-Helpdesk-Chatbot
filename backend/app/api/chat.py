from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.embeddings import embed_query
from app.services.vectordb import search_chunks
from app.services.llm import generate_answer
from app.services.reranker import rerank_documents

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

@router.post("/chat")
async def chat(request: QuestionRequest):
    question = request.question
    
    if not question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    
    try:
        query_embedding = embed_query(question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding Failed: {str(e)}")
    
    try:
        results = search_chunks(query_embedding, top_k=5)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search Failed: {str(e)}")
    
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    if not documents:
        return {
            "question": question,
            "answer": "I could not find relevant information in the uploaded documents.",
            "sources": []
        }

    # try:
    #     answer = generate_answer(question, documents)
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Answer generation failed: {str(e)}")


    # return {
    #     "question": question,
    #     "answer": answer,
    #     "sources": [
    #         {
    #             "text": doc,
    #             "metadata": meta
    #         }
    #         for doc, meta in zip(documents, metadatas)
    #     ]
    # }

    reranked = rerank_documents(question, documents, metadatas, top_n=3)

    best_docs = [item["text"] for item in reranked]

    answer = generate_answer(question, best_docs)

    return {
        "question": question,
        "answer": answer,
        "sources": reranked
    }

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.parser import extract_text
from app.services.chunker import chunk_text
from app.services.embeddings import embed_texts
from app.services.vectordb import add_chunks

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    allowed_types = ["application/pdf", 
                     "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                     ]
    
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Only PDF and DOCX are allowed")
    
    content = await file.read()

    try:
        text = extract_text(file.filename, file.content_type, content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract text: {str(e)}")
    
    if not text.strip():
        raise HTTPException(status_code=400, detail="No readable text found in file")

    try:
        chunks = chunk_text(text, chunk_size=500, overlap=100)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to chunk text: {str(e)}")
    
    try:
        embeddings = embed_texts(chunks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate embeddings: {str(e)}")

    embedding_dimension = len(embeddings[0]) if embeddings else 0

    try:
        add_chunks(chunks, embeddings, source=file.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store in vector DB: {str(e)}")

    return {
        "filename": file.filename, 
        "characters_extracted": len(text),
        "number_of_chunks": len(chunks),
        "number_of_embeddings": len(embeddings),
        "embedding_dimension": embedding_dimension,
        "first_chunk_preview": chunks[0][:300] if chunks else "",
        
        }
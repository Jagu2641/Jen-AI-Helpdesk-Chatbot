# JEN-AI Helpdesk Chatbot (RAG + Reranking)

A full-stack AI helpdesk chatbot that answers questions from uploaded documents using Retrieval-Augmented Generation (RAG). The system processes PDF and DOCX files, stores document chunks in a vector database, retrieves relevant context through semantic search, reranks retrieved chunks for better precision, and generates grounded answers using an LLM.

## Features

- Upload PDF and DOCX documents
- Extract and chunk document text
- Generate embeddings for semantic retrieval
- Store embeddings in Chroma vector database
- Retrieve relevant chunks based on user questions
- Rerank retrieved chunks using a cross-encoder
- Generate grounded answers with an LLM
- Display source chunks in the UI for transparency
- React frontend for document upload and chat interaction
- FastAPI backend for document processing and RAG pipeline

## Tech Stack

### Frontend
- React
- Vite
- Tailwind CSS v4

### Backend
- FastAPI
- Python

### AI / Retrieval
- Sentence Transformers
- ChromaDB
- OpenAI API
- Cross-Encoder Reranker

## How It Works

1. A user uploads a PDF or DOCX file.
2. The backend extracts the text from the document.
3. The text is split into overlapping chunks.
4. Each chunk is converted into an embedding.
5. Chunks and embeddings are stored in ChromaDB.
6. When the user asks a question, the question is embedded.
7. Chroma retrieves the most relevant chunks.
8. A reranker reorders the retrieved chunks for better relevance.
9. The top reranked chunks are passed to the LLM.
10. The LLM generates a grounded answer using only the retrieved context.

## Project Structure

```text
Jen-AI-Helpdesk-Chatbot/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   └── main.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── .gitignore
└── README.md

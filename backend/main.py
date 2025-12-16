from fastapi import FastAPI
from app.api import router as api_router
import uvicorn
import os
from llama_index.core import set_global_handler # <-- Import baru

# 1. Aktifkan Handler Langchain (LangSmith) saat server nyala
# GANTI JADI INI:
set_global_handler("simple")

app = FastAPI(title="Legal Chatbot RAG")

app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "Legal Chatbot API is running!"}

if __name__ == "__main__":
    # Reload=False biar stabil
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
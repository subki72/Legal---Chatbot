# ⚖️ AI Legal Assistant - Indonesian Law

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![LlamaIndex](https://img.shields.io/badge/LlamaIndex-Advanced_RAG-orange?style=for-the-badge)

An intelligent chatbot designed to assist users in understanding Indonesian Law regulations. Unlike traditional chatbots, this system employs **Advanced RAG (Retrieval-Augmented Generation)** with **Re-ranking** capabilities to ensure high accuracy and context-aware responses based on official legal documents (UU LLAJ, etc.).

---

##  Key Features

* **Advanced RAG Architecture:** Uses a retrieve-then-rerank approach to fetch the most relevant legal articles before generating answers.
* **High-Performance LLM:** Powered by **Llama 3** (via Groq API) for fast and accurate reasoning.
* **Transparent Citations:** Every answer includes references to the specific legal documents and page numbers used.
* **Dockerized:** Fully containerized with Docker Compose for easy deployment and scalability.
* **Monitoring:** Integrated with LangSmith/Terminal Logging for tracking token usage and latency.

---

## Tech Stack

* **Core Framework:** [LlamaIndex](https://www.llamaindex.ai/)
* **LLM Provider:** [Groq](https://groq.com/) (Llama 3.3 model)
* **Vector Database:** [ChromaDB](https://www.trychroma.com/) (Persistent storage)
* **Embedding Model:** HuggingFace (`sentence-transformers`)
* **Backend:** FastAPI
* **Frontend:** Streamlit
* **DevOps:** Docker & Docker Compose

---

## Project Structure

```bash
Legal-Chatbot/
├── backend/             # FastAPI Server & RAG Engine
├── frontend/            # Streamlit User Interface
├── Data/                # PDF Legal Documents & Vector Store
├── docker-compose.yml   # Orchestration for services
├── Dockerfile.backend   # Backend container config
├── Dockerfile.frontend  # Frontend container config
└── requirements.txt     # Python dependencies

import os
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq
from llama_index.core.postprocessor import SentenceTransformerRerank 
import chromadb
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CHROMA_DB_DIR = os.path.join(BASE_DIR, "Data", "vector_store")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_chat_engine():
    if not os.path.exists(CHROMA_DB_DIR):
        raise ValueError(f"Database tidak ditemukan di {CHROMA_DB_DIR}")
        
    db = chromadb.PersistentClient(path=CHROMA_DB_DIR)
    chroma_collection = db.get_or_create_collection("legal_docs")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    
    # 2. Embedding Model (Sama kayak Ingest)
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    
    # 3. Load Index
    index = VectorStoreIndex.from_vector_store(
        vector_store,
        embed_model=embed_model,
    )
    
    # 4. LLM (Otak Llama 3.3)
    llm = Groq(model="llama-3.3-70b-versatile", api_key=GROQ_API_KEY)

    # 5. ADVANCED RAG: Re-ranker
    reranker = SentenceTransformerRerank(
        model="cross-encoder/ms-marco-MiniLM-L-6-v2", top_n=3
    )

    # 6. Chat Engine dengan Re-ranking
    chat_engine = index.as_chat_engine(
        chat_mode="context",
        llm=llm,
        node_postprocessors=[reranker], 
        similarity_top_k=10, 
        system_prompt=(
            "Anda adalah asisten hukum profesional (AI Legal Assistant). "
            "Jawab pertanyaan pengguna HANYA berdasarkan konteks dokumen UU yang diberikan. "
            "Sebutkan Dasar Hukum (Pasal/Ayat) secara spesifik. "
            "Gunakan Bahasa Indonesia formal. Jika tidak ada di dokumen, katakan tidak tahu."
        )
    )
    
    return chat_engine
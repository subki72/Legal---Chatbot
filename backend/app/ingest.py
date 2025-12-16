import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import chromadb

# 1. Konfigurasi Path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "Data", "raw")
CHROMA_DB_DIR = os.path.join(BASE_DIR, "Data", "vector_store")

def ingest_data():
    print(f"📂 Membaca dokumen dari: {DATA_DIR}")
    
    if not os.path.exists(DATA_DIR) or not os.listdir(DATA_DIR):
        print("❌ Error: Folder Data/raw kosong atau tidak ditemukan!")
        return

    # 2. Load Dokumen PDF
    reader = SimpleDirectoryReader(input_dir=DATA_DIR, recursive=True)
    documents = reader.load_data()
    print(f"📄 Ditemukan {len(documents)} halaman dokumen.")

    # 3. Setup Vector Database (ChromaDB)
    db = chromadb.PersistentClient(path=CHROMA_DB_DIR)
    chroma_collection = db.get_or_create_collection("legal_docs")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # 4. Setup Embedding Model (Biar Gratis & Ringan pakai HuggingFace lokal)
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

    # 5. Proses Indexing (Chunking -> Embedding -> Save)
    print("🚀 Sedang memproses (Chunking & Embedding)... Tunggu bentar.")
    index = VectorStoreIndex.from_documents(
        documents, 
        storage_context=storage_context,
        embed_model=embed_model,
        show_progress=True
    )

    print("✅ Selesai! Data hukum berhasil disimpan ke Vector Database.")

if __name__ == "__main__":
    ingest_data()
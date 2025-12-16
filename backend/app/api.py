from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.engine import get_chat_engine
import time 

router = APIRouter()

print("⚙️ Memuat AI Engine...")
chat_engine = get_chat_engine()
print("✅ AI Engine Siap!")

class ChatRequest(BaseModel):
    query: str

@router.post("/chat")
async def chat_endpoint(query: str):
    try:
        # 1. Mulai Monitoring (Start Stopwatch)
        start_time = time.time()
        print(f"\n{'='*10} PERTANYAAN BARU {'='*10}")
        print(f"🗣️  User: {query}")
        
        # 2. Suruh AI Mikir
        response = chat_engine.chat(query)
        
        # 3. Stop Monitoring (Hitung Durasi)
        end_time = time.time()
        latency = end_time - start_time
        
        # 4. Hitung Token (Estimasi Kasar: 1 kata ≈ 1.3 token)
        input_tokens = len(query.split()) * 1.3
        output_tokens = len(response.response.split()) * 1.3
        total_tokens = int(input_tokens + output_tokens)
        
        # 5. CETAK LAPORAN KE TERMINAL (Ini yang dinilai Dosen)
        print(f"AI: {response.response[:50]}...") # Tampilin dikit jawabannya
        print(f"\n[MONITORING DASHBOARD]")
        print(f"  Latency (Waktu Mikir): {latency:.2f} detik")
        print(f" Total Token Usage    : ~{total_tokens} tokens")
        print(f"Sumber Dokumen     : {len(response.source_nodes)} referensi")
        print(f"{'='*35}\n")
        
        # --- Proses Data untuk Frontend ---
        answer_text = response.response
        sources = []
        for node in response.source_nodes:
            meta = node.node.metadata
            file_name = meta.get('file_name', 'Dokumen')
            page = meta.get('page_label', '?')
            sources.append(f"{file_name} (Hal. {page})")
        
        sources = list(set(sources))
            
        return {
            "response": answer_text,
            "sources": sources,
            "latency": f"{latency:.2f}s",
            "tokens": total_tokens
        }
            
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
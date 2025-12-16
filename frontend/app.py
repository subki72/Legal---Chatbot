import streamlit as st
import requests
import os
# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="AI Legal Assistant",
    page_icon="⚖️",
    layout="centered"
)

st.title("⚖️ AI Asisten Hukum Indonesia")
st.markdown("---")

# 2. Inisialisasi History Chat (Biar gak lupa ingatan)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Tampilkan Chat Terdahulu
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Kalau ada data tambahan (sumber/metrics), tampilin juga
        if "extras" in message:
            with st.expander("Detail Referensi & Monitoring"):
                st.info(f" Sumber: {', '.join(message['extras']['sources'])}")
                st.caption(f" Waktu Mikir: {message['extras']['latency']} |  Token: {message['extras']['tokens']}")

# 4. Input User
if prompt := st.chat_input("Tanya seputar UU Lalu Lintas..."):
    # Tampilkan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 5. Proses ke Backend
    with st.chat_message("assistant"):
        with st.spinner("Sedang menganalisis dokumen hukum..."):
            try:
                # LOGIKA BARU: Cek apakah ada settingan URL khusus dari Docker?
                # Kalau ada pakai itu, kalau gak ada pakai localhost (127.0.0.1)
                backend_url = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
                
                response = requests.post(
                    f"{backend_url}/chat",  # <-- Pakai variabel backend_url
                    params={"query": prompt}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data['response']
                    sources = data['sources']
                    latency = data.get('latency', 'N/A') # Ambil data monitoring
                    tokens = data.get('tokens', 'N/A')   # Ambil data monitoring
                    
                    # Tampilkan Jawaban Utama
                    st.markdown(answer)
                    
                    # Tampilkan Data Pendukung (Advanced RAG Proof)
                    with st.expander(" Detail Referensi & Monitoring"):
                        st.info(f"Sumber: {', '.join(sources)}")
                        st.caption(f"Waktu Mikir: {latency} |  Token: {tokens}")
                    
                    # Simpan ke history
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": answer,
                        "extras": {"sources": sources, "latency": latency, "tokens": tokens}
                    })
                    
                else:
                    st.error(f"Gagal menghubungi backend: {response.text}")
                    
            except Exception as e:
                st.error(f"Terjadi kesalahan koneksi: {e}")
import streamlit as st
import requests
import time

st.title("🔄 Data Sensor SUHU dan kelembapan")

# Tempat kosong untuk menampilkan data yang akan diperbarui
placeholder = st.empty()

# Tentukan URL ngrok dengan HTTPS
url = "https://0989-103-136-58-244.ngrok-free.app/api/data"

# Jalankan loop update otomatis menggunakan st.experimental_rerun()
while True:
    try:
        # Ambil data dari API Flask melalui ngrok
        response = requests.get(url)
        data = response.json()

        with placeholder.container():
            st.markdown("### 📊 Data Sensor:")
            st.write(f"🌡️ Suhu       : {data['temperature']} °C")
            st.write(f"💧 Kelembaban : {data['humidity']} %")
            st.write(f"📌 Status     : **{data['status']}**")

    except Exception as e:
        st.error(f"Gagal mengambil data: {e}")

    # Tunggu 2 detik sebelum update lagi
    time.sleep(2)
    st.experimental_rerun()  # Memaksa streamlit untuk refresh

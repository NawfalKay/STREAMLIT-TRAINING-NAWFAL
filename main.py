import streamlit as st
import requests
import time

st.title("🔄data sensor")

# Tempat kosong untuk menampilkan data yang akan diperbarui
placeholder = st.empty()

# Jalankan loop update otomatis
while True:
    try:
        response = requests.get("https://0989-103-136-58-244.ngrok-free.app/api/data")
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

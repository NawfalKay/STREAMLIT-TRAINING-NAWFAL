import streamlit as st
import requests
import time

st.title("🔄 SUHU dan kelembapan")

# Tempat kosong untuk menampilkan data yang akan diperbarui
placeholder = st.empty()

# Tentukan URL ngrok dengan HTTPS
url = "https://8c8c-103-136-58-244.ngrok-free.app/api/data"

# Jalankan loop update otomatis
while True:
    try:
        # Ambil data dari API Flask melalui ngrok dengan timeout handling
        response = requests.get(url, timeout=5)  # Set timeout 5 detik
        response.raise_for_status()  # Memastikan status 200 OK

        # Debug: Cetak response text untuk memastikan isinya
        st.write(f"Response Text: {response.text}")  # Cek isi response

        # Konversi response menjadi JSON
        data = response.json()

        with placeholder.container():
            st.markdown("### 📊 Data Sensor:")
            st.write(f"🌡️ Suhu       : {data['temperature']} °C")
            st.write(f"💧 Kelembaban : {data['humidity']} %")
            st.write(f"📌 Status     : **{data['status']}**")

    except requests.exceptions.Timeout:
        st.error("Waktu habis! Tidak dapat terhubung ke server.")
    except requests.exceptions.RequestException as e:
        st.error(f"Gagal mengambil data: {e}")

    # Tunggu 2 detik sebelum update lagi
    time.sleep(2)

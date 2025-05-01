import streamlit as st
import requests
import time

st.title("🔄 Realtime Dashboard dari Flask API")

# Tempat kosong untuk menampilkan data yang akan diperbarui
placeholder = st.empty()

# Tentukan URL ngrok
url = "https://27a7-103-136-58-244.ngrok-free.app/api/data"

# Jalankan loop update otomatis
while True:
    try:
        # Ambil data dari API Flask dengan timeout handling
        response = requests.get(url, timeout=5)  # Timeout 5 detik

        # Periksa status code dari respons
        if response.status_code == 200:
            # Konversi respons ke JSON
            data = response.json()

            # Periksa apakah data valid
            if 'temperature' in data and 'humidity' in data and 'status' in data:
                with placeholder.container():
                    st.markdown("### 📊 Data Sensor:")
                    st.write(f"🌡️ Suhu       : {data['temperature']} °C")
                    st.write(f"💧 Kelembaban : {data['humidity']} %")
                    st.write(f"📌 Status     : **{data['status']}**")
            else:
                st.error("Data yang diterima tidak lengkap atau tidak valid.")
        else:
            st.error(f"Server Flask mengembalikan kesalahan: {response.status_code}")

    except requests.exceptions.Timeout:
        st.error("Waktu habis! Tidak dapat terhubung ke server.")
    except requests.exceptions.RequestException as e:
        st.error(f"Gagal mengambil data: {e}")
    
    # Tunggu 2 detik sebelum update lagi
    time.sleep(2)

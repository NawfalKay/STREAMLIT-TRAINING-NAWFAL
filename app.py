import streamlit as st
import requests
import time

st.title("🔄 Realtime Dashboard dari Flask API")

# Tempat kosong untuk menampilkan data yang akan diperbarui
placeholder = st.empty()

# Tentukan URL ngrok dengan HTTPS
url = "https://27a7-103-136-58-244.ngrok-free.app/api/data"

# Jalankan loop update otomatis
while True:
    try:
        # Ambil data dari API Flask melalui ngrok dengan timeout handling
        response = requests.get(url, timeout=5)  # Set timeout 5 detik

        # Pastikan status 200 OK
        response.raise_for_status()

        # Cek apakah respons JSON valid
        try:
            data = response.json()
        except ValueError:
            st.error(f"Data yang diterima bukan JSON: {response.text}")
            break

        with placeholder.container():
            st.markdown("### 📊 Data Sensor:")
            st.write(f"🌡️ Suhu       : {data['temperature']} °C")
            st.write(f"💧 Kelembaban : {data['humidity']} %")
            st.write(f"📌 Status     : **{data['status']}**")

    except requests.exceptions.Timeout:
        st.error("Waktu habis! Tidak dapat terhubung ke server.")
    except requests.exceptions.RequestException as e:
        st.error(f"Gagal mengambil data: {e}")
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")

    # Tunggu 2 detik sebelum update lagi
    time.sleep(2)

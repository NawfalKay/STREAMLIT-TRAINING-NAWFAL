import streamlit as st
from flask import Flask, request, jsonify
import threading

# Data global untuk menyimpan suhu dan kelembapan
sensor_data = {"temperature": None, "humidity": None}

# Membuat aplikasi Flask
app = Flask(__name__)

@app.route('/update_data', methods=['POST'])
def update_data():
    global sensor_data
    data = request.json
    if data:
        sensor_data["temperature"] = data.get("temperature")
        sensor_data["humidity"] = data.get("humidity")
        return jsonify({"status": "success", "message": "Data updated successfully"}), 200
    return jsonify({"status": "error", "message": "Invalid data"}), 400

# Menjalankan Flask di thread terpisah
def run_flask():
    app.run(host="0.0.0.0", port=8501)

flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()

# Streamlit UI untuk menampilkan data
st.title("Real-time Sensor Data")
st.subheader("Temperature and Humidity from DHT22 Sensor")

# Placeholder untuk menampilkan data
temperature_placeholder = st.empty()
humidity_placeholder = st.empty()

# Display the data in real-time
while True:
    if sensor_data["temperature"] is not None and sensor_data["humidity"] is not None:
        # Update temperature and humidity data in real-time
        temperature_placeholder.metric(label="Temperature (°C)", value=f"{sensor_data['temperature']:.2f} °C")
        humidity_placeholder.metric(label="Humidity (%)", value=f"{sensor_data['humidity']:.2f} %")
    else:
        st.write("Waiting for sensor data...")

    # Add a small delay to avoid high CPU usage
    time.sleep(1)

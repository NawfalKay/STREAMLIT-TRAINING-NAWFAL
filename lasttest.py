import streamlit as st
import json
import time

# Data global untuk menyimpan suhu dan kelembapan
sensor_data = {"temperature": None, "humidity": None}

# Menampilkan data suhu dan kelembapan
st.title("Real-time Sensor Data")
st.subheader("Temperature and Humidity from DHT22 Sensor")

temperature_placeholder = st.empty()
humidity_placeholder = st.empty()

# Endpoint untuk menerima data HTTP POST
from http.server import BaseHTTPRequestHandler, HTTPServer

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        global sensor_data
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode())
        
        # Update global sensor_data
        sensor_data["temperature"] = data["temperature"]
        sensor_data["humidity"] = data["humidity"]
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"status": "success"}')
        
# Server HTTP untuk menerima data
def run_server():
    server_address = ('', 8501)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("Starting server on port 8501...")
    httpd.serve_forever()

# Run the server in a separate thread
import threading
server_thread = threading.Thread(target=run_server)
server_thread.start()

# Real-time Data Display Loop
while True:
    if sensor_data["temperature"] is not None and sensor_data["humidity"] is not None:
        temperature_placeholder.metric(label="Temperature (°C)", value=f"{sensor_data['temperature']:.2f} °C")
        humidity_placeholder.metric(label="Humidity (%)", value=f"{sensor_data['humidity']:.2f} %")
    else:
        st.write("Waiting for sensor data...")
    
    time.sleep(1)  # Delay to avoid high CPU usage

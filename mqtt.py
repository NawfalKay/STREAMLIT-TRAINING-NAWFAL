import streamlit as st
import paho.mqtt.client as mqtt
import json
import time

# MQTT Setup
BROKER = "broker.emqx.io"  # Broker yang digunakan
TOPIC_SENSOR = "/Phaethon/Nawfal_Kaysan_Rehma_Ely/data_sensor"
CLIENT_ID = ""  # Tanpa CLIENT_ID, Paho MQTT akan membuatkan ID unik

# Global variable to store sensor data
sensor_data = {"temperature": None, "humidity": None}

# MQTT callback function to handle incoming messages
def on_message(client, userdata, msg):
    global sensor_data
    try:
        # Parse the JSON data received from the MQTT broker
        sensor_data = json.loads(msg.payload.decode())
        st.write(f"Received data: {sensor_data}")  # Tampilkan data yang diterima
    except Exception as e:
        st.error(f"Error parsing data: {e}")

# Setup MQTT client
def setup_mqtt():
    client = mqtt.Client(CLIENT_ID)
    client.on_message = on_message
    try:
        client.connect(BROKER)
        client.subscribe(TOPIC_SENSOR)
        st.write("Connected to MQTT Broker")
    except Exception as e:
        st.error(f"Failed to connect to MQTT: {e}")
    return client

# Main function for Streamlit app
def main():
    st.title("🔄 Dashboard Monitoring Suhu dan Kelembaban")

    # Start MQTT client and loop in the background
    client = setup_mqtt()
    client.loop_start()  # Start the MQTT client loop

    # Placeholder for displaying real-time sensor data
    placeholder = st.empty()

    # Display real-time sensor data
    while True:
        if sensor_data["temperature"] is not None:
            placeholder.markdown("📊 Data Sensor")
            placeholder.write(f"🌡️ Suhu       : {sensor_data['temperature']} °C")
            placeholder.write(f"💧 Kelembaban : {sensor_data['humidity']} %")
            st.write(f"Data terkini: {sensor_data}")
        else:
            placeholder.write("Data belum tersedia.")
        
        time.sleep(1)  # Gunakan delay ringan untuk memberi waktu bagi Streamlit untuk merender halaman

if __name__ == "__main__":
    main()

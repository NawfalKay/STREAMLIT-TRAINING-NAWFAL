import streamlit as st
import paho.mqtt.client as mqtt
import json

# MQTT Setup
BROKER = "broker.emqx.io"  # Ganti dengan broker MQTT yang Anda gunakan
TOPIC_SENSOR = "/Phaethon/Nawfal_Kaysan_Rehma_Ely/data_sensor"
CLIENT_ID = "streamlit-client"  # Ganti dengan ID klien unik jika diperlukan

# Global variable to store sensor data
sensor_data = {"temperature": None, "humidity": None}

# MQTT callback function to handle incoming messages
def on_message(client, userdata, msg):
    global sensor_data
    try:
        # Parse the JSON data received from the MQTT broker
        sensor_data = json.loads(msg.payload.decode())
    except Exception as e:
        st.error(f"Error parsing data: {e}")

# Setup MQTT client
def setup_mqtt():
    client = mqtt.Client(CLIENT_ID)
    client.on_message = on_message
    client.connect(BROKER)
    client.subscribe(TOPIC_SENSOR)
    return client

# Main function for Streamlit app
def main():
    st.title("🔄 Dashboard Monitoring Suhu dan Kelembaban")

    # Start MQTT client and loop in the background
    client = setup_mqtt()
    client.loop_start()  # Start the MQTT client loop

    # Display real-time sensor data
    st.header("📊 Data Sensor")
    while True:
        if sensor_data["temperature"] is not None:
            st.write(f"🌡️ Suhu       : {sensor_data['temperature']} °C")
            st.write(f"💧 Kelembaban : {sensor_data['humidity']} %")
        else:
            st.write("Data belum tersedia.")
        st.experimental_rerun()  # Refresh the page periodically

if __name__ == "__main__":
    main()

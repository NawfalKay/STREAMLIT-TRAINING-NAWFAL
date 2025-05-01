import streamlit as st
import paho.mqtt.client as mqtt
import json

# MQTT Setup
BROKER = "broker.emqx.io"  # Ganti dengan broker MQTT yang Anda gunakan
TOPIC_SENSOR = "sensor/data"

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
    client = mqtt.Client()  # Tanpa CLIENT_ID, Paho MQTT akan membuatkan ID unik
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

    # Placeholder for displaying real-time sensor data
    placeholder = st.empty()

    # Display real-time sensor data
    while True:
        # Check if data is available
        if sensor_data["temperature"] is not None:
            # Update the display
            placeholder.markdown("📊 Data Sensor")
            placeholder.write(f"🌡️ Suhu       : {sensor_data['temperature']} °C")
            placeholder.write(f"💧 Kelembaban : {sensor_data['humidity']} %")
        else:
            placeholder.write("Data belum tersedia.")

        # Wait for the next event and avoid busy-wait
        st.experimental_rerun()

if __name__ == "__main__":
    main()

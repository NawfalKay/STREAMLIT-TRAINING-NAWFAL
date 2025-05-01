import streamlit as st
import paho.mqtt.client as mqtt
import json
import threading
import time

# MQTT Configuration
BROKER = "broker.emqx.io"
PORT = 1883
TOPIC_SENSOR = "/Phaethon/Nawfal_Kaysan_Rehma_Ely/data_sensor"
CLIENT_ID = "streamlit_client"

# Global variable to store sensor data
sensor_data = {"temperature": None, "humidity": None}

# MQTT callback functions
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    # Subscribe to the topic
    client.subscribe(TOPIC_SENSOR)

def on_message(client, userdata, msg):
    global sensor_data
    try:
        # Parse the JSON data from the MQTT message
        data = json.loads(msg.payload.decode())
        print(f"Data received from MQTT: {data}")  # Log data received
        sensor_data = data
    except Exception as e:
        print("Error parsing message:", e)

# MQTT client setup
def mqtt_thread():
    client = mqtt.Client(CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    client.loop_forever()

# Start the MQTT client in a separate thread
mqtt_thread = threading.Thread(target=mqtt_thread, daemon=True)
mqtt_thread.start()

# Streamlit UI setup
st.title("Real-time Sensor Data")
st.subheader("Temperature and Humidity from DHT22 Sensor")

# Placeholder for displaying data
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

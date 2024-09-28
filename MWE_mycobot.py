import streamlit as st
import paho.mqtt.client as mqtt
from pymycobot.mycobot import MyCobot
import time

# Initialize MyCobot
mycobot = MyCobot('/dev/ttyUSB0', 115200)  # Adjust port as necessary

# MQTT setup
mqtt_broker = "broker.hivemq.com"
mqtt_port = 1883
mqtt_topic = "mycobot/commands"

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    command = msg.payload.decode()
    if command == "move_home":
        mycobot.send_angles([0, 0, 0, 0, 0, 0], 50)
    elif command == "grab":
        mycobot.set_gripper_state(0, 50)
    elif command == "release":
        mycobot.set_gripper_state(1, 50)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_broker, mqtt_port, 60)
client.loop_start()

# Streamlit interface
st.title("MyCobot 280 Control Panel")

if st.button("Move to Home Position"):
    mycobot.send_angles([0, 0, 0, 0, 0, 0], 50)
    st.success("Moving to home position")

if st.button("Grab"):
    mycobot.set_gripper_state(0, 50)
    st.success("Gripper closed")

if st.button("Release"):
    mycobot.set_gripper_state(1, 50)
    st.success("Gripper opened")

# Display current joint angles
if st.button("Get Joint Angles"):
    angles = mycobot.get_angles()
    st.write("Current Joint Angles:", angles)

# MQTT message sender
message = st.text_input("Send MQTT Command")
if st.button("Send MQTT Message"):
    client.publish(mqtt_topic, message)
    st.success(f"Sent: {message}")

# Keep the script running
while True:
    time.sleep(0.1)

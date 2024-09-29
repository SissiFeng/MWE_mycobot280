
# MWE_mycobot280

## Install the required libraries:

```bash
pip install streamlit paho-mqtt pymycobot
```

## This script does the following:

1. Initializes the MyCobot 280 robotic arm using the `pymycobot` library.
2. Sets up an MQTT client to subscribe to commands and publish messages.
3. Creates a Streamlit interface with buttons to control the robot and display its status.

## To run the Streamlit app:

Save the script as `mycobot_control.py` and run:

```bash
streamlit run mycobot_control.py
```

## This MWE provides basic functionality to:

- Move the robot to its home position.
- Control the gripper (grab and release).
- Get current joint angles.
- Send and receive MQTT messages.

> **Note:** You may need to adjust the serial port (e.g., `/dev/ttyUSB0`) based on your system configuration. Also, this example uses a public MQTT broker for demonstration purposes. In a production environment, you should use a secure, private MQTT broker.

This example serves as a starting point. You can expand it by:
- Adding more complex movement commands.
- Implementing error handling.
- Enhancing the user interface based on specific requirements.

---
title: Robot Arm Simulator
emoji: 🦾
colorFrom: blue
colorTo: red
sdk: streamlit
sdk_version: 1.21.0
app_file: robot_arm_simulator.py
pinned: false
---

# Robot Arm Simulator

This Streamlit app simulates a robot arm moving and manipulating bottles in a laboratory setting. Users can control the arm's movement, grab and release bottles, and run a predefined bottle transfer task.

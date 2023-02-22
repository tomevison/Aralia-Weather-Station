# Aralia-Weather-Station
Simple ESP32 based weather station that communicates with Ignition SCADA via MQTT. The sensor will take regular temperature and humidity readings to be displayed on Ignition SCADA historical chart.

There are 3 seperate subsystems that are required for overall system to run.
- ESP32 Firmware
- MQTT Broker [Eclipse Mosquitto](https://mosquitto.org/)
- MQTT > SQL Bridge service

import paho.mqtt.client as mqtt
import mariadb
import sys

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("$SYS/#")
    client.subscribe("esp32/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user="ignition",
            password="xxxxxxxxxxxxxxxxxx",
            host="localhost",
            port=3306,
            database="tr_ignition",
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    # Get Cursor
    cur = conn.cursor()
    print(msg.topic+" "+str(msg.payload.decode("utf-8")))
    
    if msg.topic=="esp32/dht/temperature":    
        try:
            cur.execute("UPDATE mqtt_bridge SET temp = ? WHERE id = 1", (msg.payload.decode("utf-8"),))
            conn.commit()
        except mariadb.Error as e:
            print(f"Error: {e}")

    if msg.topic=="esp32/dht/humidity":    
        try:
            cur.execute("UPDATE mqtt_bridge SET humd = ? WHERE id = 1", (msg.payload.decode("utf-8"),))
            conn.commit()
        except mariadb.Error as e:
            print(f"Error: {e}")

    if msg.topic=="esp32/wifi/rssi":    
        try:
            cur.execute("UPDATE mqtt_bridge SET rssi = ? WHERE id = 1", (msg.payload.decode("utf-8"),))
            conn.commit()
        except mariadb.Error as e:
            print(f"Error: {e}")

sys.stdout.write("script started")
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("10.40.40.4", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

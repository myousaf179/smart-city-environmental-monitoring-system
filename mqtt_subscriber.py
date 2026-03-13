import os
import paho.mqtt.client as mqtt

BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "localhost")
BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", "1883"))
TOPIC = os.getenv("MQTT_TOPIC", "city/sensors/environment")

def on_connect(client, userdata, flags, reason_code, properties=None):
    client.subscribe(TOPIC, qos=1)
    print(f"Subscribed to {TOPIC}")

def on_message(client, userdata, msg):
    print(msg.topic, msg.payload.decode("utf-8"))

def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="mqtt_subscriber")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    client.loop_forever()

if __name__ == "__main__":
    main()

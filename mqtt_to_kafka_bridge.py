import json
import os

import paho.mqtt.client as mqtt
from kafka import KafkaProducer

BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "localhost")
BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "city/sensors/environment")

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "sensor_stream")

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS.split(","),
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda v: v.encode("utf-8"),
    acks="all",
)

def on_connect(client, userdata, flags, reason_code, properties=None):
    client.subscribe(MQTT_TOPIC, qos=1)
    print(f"Bridge subscribed to {MQTT_TOPIC}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
        sensor_id = payload.get("sensor_id", "unknown")
        producer.send(KAFKA_TOPIC, key=sensor_id, value=payload)
        producer.flush()
        print(f"MQTT -> Kafka, {sensor_id}")
    except Exception as exc:
        print("bridge error:", exc)

def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="mqtt_to_kafka_bridge")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    client.loop_forever()

if __name__ == "__main__":
    main()

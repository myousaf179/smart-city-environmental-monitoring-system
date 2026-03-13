import json
import os
import random
import time
from datetime import datetime, timezone

import paho.mqtt.client as mqtt

BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "localhost")
BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", "1883"))
TOPIC = os.getenv("MQTT_TOPIC", "city/sensors/environment")

SENSOR_IDS = [f"sensor_{i}" for i in range(1, 6)]

def build_payload(sensor_id: str) -> dict:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    return {
        "sensor_id": sensor_id,
        "timestamp": now,
        "temperature": round(random.uniform(18.0, 40.0), 1),
        "humidity": random.randint(20, 90),
        "aqi": random.randint(20, 220),
        "noise": random.randint(30, 95),
    }

def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="sensor_simulator")
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    client.loop_start()

    print(f"Publishing to mqtt://{BROKER_HOST}:{BROKER_PORT}/{TOPIC}")
    try:
        while True:
            for sensor_id in SENSOR_IDS:
                payload = build_payload(sensor_id)
                client.publish(TOPIC, json.dumps(payload), qos=1)
                print("sent", payload)
            time.sleep(2)
    except KeyboardInterrupt:
        pass
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()

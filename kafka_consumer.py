import json
import os
import sqlite3
from pathlib import Path

from kafka import KafkaConsumer

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "sensor_stream")
SQLITE_DB = Path(os.getenv("SQLITE_DB", "storage/sensor_data.db"))
CSV_FILE = Path(os.getenv("CSV_FILE", "storage/sensor_data.csv"))

SQLITE_DB.parent.mkdir(parents=True, exist_ok=True)
CSV_FILE.parent.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(SQLITE_DB)
cur = conn.cursor()
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS sensor_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sensor_id TEXT,
        timestamp TEXT,
        temperature REAL,
        humidity REAL,
        aqi INTEGER,
        noise INTEGER
    )
    """
)
conn.commit()

if not CSV_FILE.exists():
    CSV_FILE.write_text("sensor_id,timestamp,temperature,humidity,aqi,noise\n", encoding="utf-8")

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS.split(","),
    auto_offset_reset="latest",
    enable_auto_commit=True,
    group_id="sensor_consumer_group",
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
)

print(f"Consuming from {KAFKA_TOPIC}")

for message in consumer:
    record = message.value
    row = (
        record.get("sensor_id"),
        record.get("timestamp"),
        record.get("temperature"),
        record.get("humidity"),
        record.get("aqi"),
        record.get("noise"),
    )

    cur.execute(
        "INSERT INTO sensor_data (sensor_id, timestamp, temperature, humidity, aqi, noise) VALUES (?, ?, ?, ?, ?, ?)",
        row,
    )
    conn.commit()

    with CSV_FILE.open("a", encoding="utf-8") as f:
        f.write(",".join(map(str, row)) + "\n")

    print("stored", row)

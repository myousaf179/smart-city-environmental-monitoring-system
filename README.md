# Smart City Environmental Monitoring Pipeline

This project simulates a smart city environmental monitoring system using IoT sensors and a real time data streaming pipeline.

Environmental sensors publish data using MQTT. The data is forwarded to Kafka for streaming, processed by a consumer, stored in structured format, and automatically aggregated using Apache Airflow.

The system demonstrates how modern data platforms handle IoT streaming data pipelines.

---

# System Architecture

The pipeline follows this workflow:

Sensors → MQTT Broker → Kafka → Kafka Consumer → Sensor Storage → Airflow Workflow → Aggregated Results

Components used in the system:

• MQTT (Mosquitto) for IoT messaging
• Apache Kafka for data streaming
• Python for simulation and data processing
• CSV and SQLite for storage
• Apache Airflow for workflow automation
• Docker for infrastructure services

---

# Project Structure

```
smart_city_iot_pipeline
│
├── mqtt_simulator.py
├── mqtt_subscriber.py
├── mqtt_to_kafka_bridge.py
├── kafka_consumer.py
├── dashboard_app.py
│
├── docker-compose.yml
├── requirements.txt
│
├── mosquitto
│   └── mosquitto.conf
│
├── airflow
│   └── dags
│       └── sensor_aggregation_dag.py
│
└── storage
    ├── sensor_data.db
    ├── sensor_data.csv
    └── aggregation_results.csv
```

---

# Requirements

Software required

• Python 3.10 or later
• Docker Desktop
• Git
• Windows PowerShell or Terminal

Python libraries used

• paho-mqtt
• kafka-python
• pandas
• streamlit
• matplotlib
• apache-airflow

---

# Installation

Clone the repository

```
git clone https://github.com/your-repo/smart_city_iot_pipeline.git
```

Move into the project folder

```
cd smart_city_iot_pipeline
```

Create virtual environment

```
python -m venv venv
```

Allow PowerShell to run scripts (required once)

```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Activate virtual environment

```
venv\Scripts\Activate.ps1
```

Upgrade pip

```
python -m pip install --upgrade pip
```

Install dependencies

```
pip install -r requirements.txt
```

---

# Start Infrastructure

Start the messaging and streaming services using Docker

```
docker compose down
docker compose pull
docker compose up -d
```

Verify containers

```
docker ps
```

Running containers should include

• mosquitto
• zookeeper
• kafka
• airflow-webserver
• airflow-scheduler

---

# Running the Data Pipeline

Open separate terminals and activate the virtual environment before running scripts.

---

# 1 Run MQTT Sensor Simulator

```
python mqtt_simulator.py
```

This script simulates multiple IoT sensors sending environmental data every few seconds.

Example message

```
{
 "sensor_id": "sensor_1",
 "timestamp": "2026-03-10T10:00:00",
 "temperature": 28.5,
 "humidity": 65,
 "aqi": 120,
 "noise": 55
}
```

---

# 2 Verify MQTT Messages

```
python mqtt_subscriber.py
```

This confirms that messages are reaching the MQTT broker correctly.

---

# 3 Run MQTT to Kafka Bridge

```
python mqtt_to_kafka_bridge.py
```

This script reads MQTT messages and forwards them to the Kafka topic

```
sensor_stream
```

---

# 4 Run Kafka Consumer

```
python kafka_consumer.py
```

The consumer reads Kafka messages and stores them into structured storage.

Output files

```
storage/sensor_data.db
storage/sensor_data.csv
```

Each record includes

• sensor_id
• timestamp
• temperature
• humidity
• aqi
• noise

---

# 5 Run Web Dashboard

```
streamlit run dashboard_app.py
```

Open the dashboard in the browser

```
http://localhost:8501
```

The dashboard displays

• Total records collected
• Number of sensors
• Latest environmental readings
• Average environmental metrics
• Temperature trends

---

# Phase 2 Workflow Automation using Airflow

Apache Airflow is used to automate the data processing workflow.

An Airflow DAG runs every 5 minutes and performs automated aggregation on the collected sensor data.

Airflow tasks include

1 Load stored sensor data
2 Compute environmental statistics
3 Store aggregated results

Metrics calculated

• Average temperature
• Maximum AQI
• Average humidity
• Noise level statistics

Output file

```
storage/aggregation_results.csv
```

---

# Access Airflow Interface

Open Airflow UI

```
http://localhost:8080
```

You can monitor workflow execution and DAG runs from the interface.

DAG name

```
sensor_aggregation_dag
```

The DAG automatically executes every five minutes.

---

# Example Aggregated Results

Example output from aggregation_results.csv

```
timestamp,avg_temperature,max_aqi,avg_humidity,avg_noise
2026-03-13 11:10:00,27.4,210,68,54
```

---

# Data Storage

The system stores data in multiple formats

Sensor data

```
storage/sensor_data.db
storage/sensor_data.csv
```

Aggregated analytics

```
storage/aggregation_results.csv
```

---

# Reset for Fresh Demo

Delete stored data files

```
storage/sensor_data.db
storage/sensor_data.csv
storage/aggregation_results.csv
```

Restart the pipeline to generate new data.

---

# Future Improvements

Possible system extensions

• Advanced Airflow orchestration
• Real time Kafka monitoring
• Cloud deployment (AWS or Azure)
• Grafana dashboards
• Smart pollution alert systems

---

# Author

Muhammad Yousaf
Deptt of Computer Science 
University of Engineering and Technology Mardan

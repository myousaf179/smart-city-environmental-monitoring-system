from datetime import datetime, timedelta
from pathlib import Path
import sqlite3

import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator

DB_PATH = Path("storage/sensor_data.db")
OUTPUT_PATH = Path("storage/aggregation_results.csv")


def load_and_aggregate():
    if not DB_PATH.exists():
        print("Database not found")
        return

    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM sensor_data", conn)
    conn.close()

    if df.empty:
        print("No data available")
        return

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    summary = pd.DataFrame([{
        "total_records": len(df),
        "average_temperature": df["temperature"].mean(),
        "max_aqi": df["aqi"].max(),
        "average_humidity": df["humidity"].mean(),
        "min_noise": df["noise"].min(),
        "max_noise": df["noise"].max(),
        "average_noise": df["noise"].mean(),
        "last_updated": datetime.now().isoformat()
    }])

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved aggregation to {OUTPUT_PATH}")


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="sensor_aggregation_dag",
    default_args=default_args,
    description="Aggregate sensor data every 5 minutes",
    schedule_interval="*/5 * * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["iot", "aggregation"],
) as dag:

    aggregate_task = PythonOperator(
        task_id="load_and_aggregate",
        python_callable=load_and_aggregate,
    )
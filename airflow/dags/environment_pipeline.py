from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

def summarize_data():
    import sqlite3
    import pandas as pd
    from pathlib import Path

    db_path = Path("storage/sensor_data.db")
    summary_path = Path("storage/daily_summary.csv")

    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM sensor_data", conn)
    conn.close()

    if df.empty:
        print("No data found")
        return

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["date"] = df["timestamp"].dt.date
    summary = df.groupby("date")[["temperature", "humidity", "aqi", "noise"]].mean().reset_index()
    summary.to_csv(summary_path, index=False)
    print(f"Saved {summary_path}")

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="environment_pipeline",
    default_args=default_args,
    description="Process IoT sensor data",
    schedule_interval="*/5 * * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["iot", "environment"],
) as dag:
    process_task = PythonOperator(
        task_id="summarize_data",
        python_callable=summarize_data,
    )

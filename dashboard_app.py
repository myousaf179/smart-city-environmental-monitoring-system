import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

DB_PATH = Path("storage/sensor_data.db")
CSV_PATH = Path("storage/sensor_data.csv")

st.set_page_config(page_title="Smart City IoT Dashboard", layout="wide")
st.title("Smart City Environmental Monitoring")

col1, col2, col3 = st.columns(3)
if DB_PATH.exists():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM sensor_data ORDER BY id DESC", conn)
    conn.close()
else:
    df = pd.DataFrame()

with col1:
    st.metric("Total records", len(df))
with col2:
    st.metric("Sensors", df["sensor_id"].nunique() if not df.empty else 0)
with col3:
    st.metric("CSV exists", "Yes" if CSV_PATH.exists() else "No")

st.subheader("Latest records")
st.dataframe(df.head(20), use_container_width=True)

if not df.empty:
    st.subheader("Average metrics by sensor")
    agg = df.groupby("sensor_id")[["temperature", "humidity", "aqi", "noise"]].mean()
    st.dataframe(agg, use_container_width=True)

    st.subheader("Temperature trend")
    st.line_chart(df.sort_values("id").set_index("id")[["temperature"]])

st.caption("This dashboard shows MQTT, Kafka, storage, and Airflow outputs in one place.")

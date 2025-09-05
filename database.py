import sqlite3
from datetime import datetime

DB_NAME = 'sensor_data.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            temperature REAL,
            humidity REAL,
            gas_level REAL
        )
    ''')
    conn.commit()
    conn.close()

def save_reading(temperature, humidity, gas_level):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()
    cursor.execute('''
        INSERT INTO sensor_data (timestamp, temperature, humidity, gas_level)
        VALUES (?, ?, ?, ?)
    ''', (timestamp, temperature, humidity, gas_level))
    conn.commit()
    conn.close()

def get_latest_readings(limit=10):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM sensor_data
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows


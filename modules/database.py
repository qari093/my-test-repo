import sqlite3

def init_db():
    conn = sqlite3.connect("sensor_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data (
            timestamp TEXT,
            temperature REAL,
            humidity REAL,
            light REAL
        )
    """)
    conn.commit()
    conn.close()

def save_to_db(data):
    conn = sqlite3.connect("sensor_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sensor_data (timestamp, temperature, humidity, light)
        VALUES (?, ?, ?, ?)
    """, (
        time.strftime("%Y-%m-%d %H:%M:%S"),
        data["temperature"],
        data["humidity"],
        data["light"]
    ))
    conn.commit()
    conn.close()

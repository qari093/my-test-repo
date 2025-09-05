from flask import Flask, render_template, send_from_directory
import sqlite3
import pandas as pd
import os

app = Flask(__name__)

# 🔹 Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "sensor-logs.csv")
DB_PATH = os.path.join(BASE_DIR, "sensor_data.db")

# 🔹 Function to get the latest sensor reading from the database
def get_latest_reading():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT timestamp, temperature, humidity, light
            FROM sensor_data
            ORDER BY id DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        conn.close()
        return row
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

# 🔹 Route for the live dashboard
@app.route("/")
def index():
    reading = get_latest_reading()
    return render_template("index.html", reading=reading)

# 🔹 Route to display full sensor logs from CSV
@app.route("/logs")
def show_logs():
    if not os.path.exists(CSV_PATH):
        return "<h3>sensor-logs.csv not found. Please generate or upload the file.</h3>"

    try:
        df = pd.read_csv(CSV_PATH)
        if df.empty:
            return "<h3>Log file is empty. No data to display.</h3>"
        return render_template(
            "logs.html",
            tables=[df.to_html(classes="table table-striped", index=False)],
            titles=df.columns.values
        )
    except Exception as e:
        return f"<h3>Error loading logs: {e}</h3>"

# 🔹 Optional: Serve static files like logs directly
@app.route("/download/logs")
def download_logs():
    if os.path.exists(CSV_PATH):
        return send_from_directory(BASE_DIR, "sensor-logs.csv", as_attachment=True)
    return "<h3>File not found.</h3>"

# 🔹 Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)

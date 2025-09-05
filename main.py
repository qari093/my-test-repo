import os
import time
import logging
import argparse
import csv
import random
from dotenv import load_dotenv
from twilio.rest import Client
import smtplib
from email.message import EmailMessage

# ✅ Database integration
from database import init_db, save_reading

# ✅ Config imports
from modules.config import (
    TEMP_MIN, TEMP_MAX,
    HUMIDITY_MIN, HUMIDITY_MAX,
    LIGHT_THRESHOLD,
    LOOP_INTERVAL,
    ALERT_ENABLED,
    EMAIL_ADDRESS, EMAIL_RECEIVER,
    TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE, RECEIVER_PHONE,
    LOG_FILE, LOG_LEVEL,
    ENABLE_DIAGNOSTICS
)

# Load environment variables
load_dotenv()
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Setup logging
logging.basicConfig(
    filename=LOG_FILE,
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def parse_args():
    parser = argparse.ArgumentParser(description="Control Tower Monitoring System")
    parser.add_argument("--diagnostics", action="store_true", help="Run diagnostics and exit")
    parser.add_argument("--once", action="store_true", help="Run one sensor cycle and exit")
    parser.add_argument("--test-alerts", action="store_true", help="Trigger alert test with fixed values")
    return parser.parse_args()

def run_diagnostics():
    print("🔍 Running diagnostics...")
    logging.info("Running system diagnostics...")
    print(f"✅ Temperature range: {TEMP_MIN}–{TEMP_MAX} °C")
    print(f"✅ Humidity range: {HUMIDITY_MIN}–{HUMIDITY_MAX} %")
    print(f"✅ Light threshold: {LIGHT_THRESHOLD} lux")
    print("✅ Diagnostics passed.\n")

def read_sensors(test_mode=False):
    if test_mode:
        # 🚨 Simulated alert values
        return {
            "temperature": 48.5,
            "humidity": 85.0,
            "light": 30.0
        }
    else:
        return {
            "temperature": round(random.uniform(10, 40), 2),
            "humidity": round(random.uniform(20, 90), 2),
            "light": round(random.uniform(30, 100), 2)
        }

def check_thresholds(data):
    alerts = []
    if data["temperature"] < TEMP_MIN or data["temperature"] > TEMP_MAX:
        alerts.append(f"🌡️ Temperature out of range: {data['temperature']}°C")
    if data["humidity"] < HUMIDITY_MIN or data["humidity"] > HUMIDITY_MAX:
        alerts.append(f"💧 Humidity out of range: {data['humidity']}%")
    if data["light"] < LIGHT_THRESHOLD:
        alerts.append(f"💡 Low light level: {data['light']} lux")
    return alerts

def send_email_alert(alerts):
    msg = EmailMessage()
    msg["Subject"] = "🚨 Control Tower Alert"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_RECEIVER
    msg.set_content("\n".join(alerts))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        logging.info("📧 Email alert sent.")
    except Exception as e:
        logging.error(f"❌ Email alert failed: {e}")

def send_sms_alert(alerts):
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body="🚨 ALERT:\n" + "\n".join(alerts),
            from_=TWILIO_PHONE,
            to=RECEIVER_PHONE
        )
        logging.info(f"📱 SMS alert sent: SID {message.sid}")
    except Exception as e:
        logging.error(f"❌ SMS alert failed: {e}")

def log_to_csv(data):
    with open("sensor_log.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            time.strftime("%Y-%m-%d %H:%M:%S"),
            data["temperature"],
            data["humidity"],
            data["light"]
        ])

def main():
    args = parse_args()

    if args.diagnostics:
        run_diagnostics()
        return

    # ✅ Initialize database
    init_db()

    print("🟢 Control Tower is live. Monitoring sensors...\n")

    try:
        while True:
            data = read_sensors(test_mode=args.test_alerts)
            log_to_csv(data)
            save_reading(data["temperature"], data["humidity"], data["light"])  # ✅ Save to DB
            logging.info(f"Sensor data: {data}")
            alerts = check_thresholds(data)

            if ALERT_ENABLED and alerts:
                send_email_alert(alerts)
                send_sms_alert(alerts)
                print("🚨 Alert triggered:")
                for alert in alerts:
                    print(f"   - {alert}")
            else:
                print(f"✅ All systems normal. Temp: {data['temperature']}°C | Humidity: {data['humidity']}% | Light: {data['light']} lux")

            if args.once:
                break

            time.sleep(LOOP_INTERVAL)

    except KeyboardInterrupt:
        print("\n🛑 Control Tower shutdown requested. Exiting gracefully...")
        logging.info("System manually stopped by user.")

if __name__ == "__main__":
    main()

import logging
from datetime import datetime
import random

# Setup logging (can be overridden by main.py if needed)
logging.basicConfig(
    filename="sensor.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Thresholds
TEMP_ALERT_THRESHOLD = 41.0

def read_temperature():
    """Simulate reading temperature from a sensor."""
    temperature = round(random.uniform(20.0, 45.0), 2)
    logging.info(f"Temperature reading: {temperature}°C")

    if temperature >= TEMP_ALERT_THRESHOLD:
        logging.warning(f"⚠️ High temperature alert: {temperature}°C")

    return temperature

def log_to_file(temp):
    """Log temperature to a separate text file with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("temperature_log.txt", "a") as file:
        file.write(f"[{timestamp}] - Temp: {temp}°C\n")

def stop():
    """Gracefully stop the sensor module."""
    print("Sensors module stopped")
    logging.info("Sensors module stopped")

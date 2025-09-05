# =========================
# 🚀 Control Tower Settings
# =========================

# 🌡️ Temperature thresholds (°C)
TEMP_MIN = 15.0  # Minimum safe temperature
TEMP_MAX = 35.0  # Maximum safe temperature

# 💧 Humidity thresholds (%)
HUMIDITY_MIN = 30  # Minimum acceptable humidity
HUMIDITY_MAX = 70  # Maximum acceptable humidity

# 💡 Light level threshold (lux)
LIGHT_THRESHOLD = 70  # Minimum light level required

# 🔄 Monitoring loop interval (seconds)
LOOP_INTERVAL = 5  # Time between sensor checks

# 🛑 Alert cooldown (seconds)
# Prevents repeated alerts within this time window
ALERT_COOLDOWN = 300  # 5 minutes

# ⚠️ Alert system toggle
ALERT_ENABLED = True  # Master switch for alerts

# 📧 Email alert configuration
EMAIL_ADDRESS = "projectzen455@gmail.com"         # Sender email
EMAIL_RECEIVER = "projectzen455@gmail.com"        # Receiver email
# EMAIL_PASSWORD is loaded securely from .env

# 📱 SMS alert configuration (Twilio)
TWILIO_SID = "AC9a2e2547b04a1d0a43dbc8da3e"
TWILIO_AUTH_TOKEN = "98SXFEBWR5PLVMAS2HQV88MB"
TWILIO_PHONE = "+4916091475999"
RECEIVER_PHONE = "+4916091475999"

# 🗂️ Logging settings
LOG_FILE = "tower.log"       # Log file path
LOG_LEVEL = "INFO"           # Logging verbosity: DEBUG, INFO, WARNING, ERROR

# 🧪 Diagnostics
ENABLE_DIAGNOSTICS = True    # Run system checks on startup

# 🧰 Environment mode
ENVIRONMENT = "production"   # Options: development, testing, production

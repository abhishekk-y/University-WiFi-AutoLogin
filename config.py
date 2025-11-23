"""
Configuration settings for the Auto WiFi Login system
"""
import os

# Base directory for the application
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# File paths
CREDENTIALS_FILE = os.path.join(BASE_DIR, 'credentials.json')
ENCRYPTION_KEY_FILE = os.path.join(BASE_DIR, 'encryption.key')
LOG_FILE = os.path.join(BASE_DIR, 'autologin.log')

# Authentication settings
AUTH_URL_PATTERN = "172.16.2.1:1000/fgtauth"
LOGIN_URL = "http://172.16.2.1:1000/fgtauth"

# Network settings
TEST_URLS = [
    "http://www.google.com",
    "http://www.microsoft.com",
    "http://www.cloudflare.com"
]

# Timing settings (in seconds)
CHECK_INTERVAL = 2   # Check every 2 seconds for instant detection
REQUEST_TIMEOUT = 2  # Quick timeout for HTTP requests
RETRY_DELAY = 2      # Fast retry on failed login

# Form field names (update these based on actual form inspection)
USERNAME_FIELD = "username"
PASSWORD_FIELD = "password"

# Logging settings
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
LOG_BACKUP_COUNT = 3

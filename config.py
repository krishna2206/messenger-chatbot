import os
from dotenv import load_dotenv

load_dotenv()

# Facebook app configuration
FB_ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")
FB_VERIFY_TOKEN = os.getenv("FB_VERIFY_TOKEN")
ADMIN_USER_ID = os.getenv("ADMIN_USER_ID")

# Chatbot configuration
PACKAGES = os.getenv("PACKAGES")

# Database configuration
DB_TYPE = os.getenv("DB_TYPE")

DB_FILE = os.getenv("DB_FILE")
DB_ENCRYPTION_KEY = os.getenv("DB_ENCRYPTION_KEY")

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = int(os.getenv("DB_PORT"))
DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")

# Application configuration
APP_URL = os.getenv("APP_URL")
APP_LOCATION = os.getenv("APP_LOCATION")
WEB_CONCURRENCY = os.getenv("WEB_CONCURRENCY")

# Local app configuration
APP_HOST = os.getenv("APP_HOST")
APP_PORT = int(os.getenv("APP_PORT"))

# URLs
FILES_URL = f"{APP_URL}/files"
STATIC_ASSETS_URL = f"{APP_URL}/files/static"
TEMP_FOLDER_URL = f"{APP_URL}/files/tmp"
CACHE_FOLDER_URL = f"{APP_URL}/files/cache"
THUMBNAILS_FOLDER_URL = f"{APP_URL}/files/cache/thumbnails"

# Paths
FILES_FOLDER = f"{APP_LOCATION}/files"
STATIC_FOLDER = f"{FILES_FOLDER}/static"
TEMP_FOLDER = f"{FILES_FOLDER}/tmp"
CACHE_FOLDER = f"{FILES_FOLDER}/cache"
THUMBNAILS_FOLDER = f"{FILES_FOLDER}/cache/thumbnails"

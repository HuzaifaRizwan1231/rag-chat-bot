import os
from dotenv import load_dotenv

# initialize
load_dotenv()

# Frontend URL
FRONTEND_URL = os.getenv("FRONTEND_URL")

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
AES_SECRET_KEY = os.getenv("AES_SECRET_KEY")
AES_IV = os.getenv("AES_IV")

# Allowed Models
ALLOWED_GEMINI_MODELS = ["gemini-2.5-flash"]

# GEMINI model configs
MAX_OUTPUT_TOKENS = 500
TEMPERATURE = 0.7

# Mysql Configs
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQL_PORT = os.getenv("MYSQL_PORT")

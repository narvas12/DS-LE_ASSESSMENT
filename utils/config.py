import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = os.getenv("BASE_URL", "https://api.3commas.io").rstrip('/')

if not API_KEY or not API_SECRET:
    raise ValueError("API_KEY and API_SECRET must be set in the .env file.")

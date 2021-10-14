import os
from dotenv import load_dotenv

load_dotenv()

ADDRESS = os.getenv("ADDRESS")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
API_TOKEN = os.getenv("API_TOKEN")
ALGOD_URL = os.getenv("ALGOD_URL")
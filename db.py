from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

if not MONGO_URL or not DB_NAME:
    raise ValueError("MONGO_URL and DB_NAME must be set in the environment variables.")

try:
    client = MongoClient(MONGO_URL)

    db = client[DB_NAME]

    collection = db['actions']

    print("MongoDB connection established successfully.")
except Exception as e:
    print(f"Error connecting to MongoDB: {str(e)}")

from pymongo import MongoClient, ASCENDING
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
import time
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get MongoDB host from environment or use default
MONGO_HOST = os.getenv('MONGO_HOST', 'mongodb')
MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))
MAX_RETRIES = 30
RETRY_INTERVAL = 2

def get_db_connection():
    """Establish MongoDB connection with retries"""
    for attempt in range(MAX_RETRIES):
        try:
            client = MongoClient(
                f"mongodb://{MONGO_HOST}:{MONGO_PORT}", 
                serverSelectionTimeoutMS=5000
            )
            # Test connection
            client.server_info()
            logger.info("Successfully connected to MongoDB")
            return client
        except (ServerSelectionTimeoutError, ConnectionFailure) as e:
            if attempt < MAX_RETRIES - 1:
                logger.warning(f"MongoDB connection attempt {attempt + 1} failed, retrying in {RETRY_INTERVAL}s...")
                time.sleep(RETRY_INTERVAL)
            else:
                logger.error("Failed to connect to MongoDB after maximum retries")
                raise

# Establish connection
client = get_db_connection()
db = client.katana

# Initialize collections and create indexes
COLLECTIONS = {
    'vim': 'id',
    'nfvo': 'id', 
    'wim': 'id',
    'ems': 'id',
    'policy': 'id',
    'nsd': 'nsd-id',
    'vnfd': 'vnfd-id',
    'func': 'id',
    'location': 'id'
}

for collection, field in COLLECTIONS.items():
    db[collection].create_index([(field, ASCENDING)], unique=True)
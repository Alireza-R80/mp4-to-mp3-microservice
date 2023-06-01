from config import settings
from pymongo import MongoClient

clinet = MongoClient(f"mongodb://{settings.mongodb_host}:{settings.mongodb_port}")

videos_db = clinet["videos"]
mp3s_db = clinet["mp3s"]

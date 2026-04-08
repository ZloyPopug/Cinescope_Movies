import os
from dotenv import load_dotenv

load_dotenv()

class DbCreds:
    DB_USERNAME = os.getenv("DB_USER_NAME")
    DB_PASSWORD = os.getenv("DB_USER_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
from sqlalchemy import create_engine

import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL")

try:
    engine = create_engine(DB_URL)
    conn = engine.connect()
    print("Connection Successful")
    conn.close()
except Exception as e:
    print("Connection Failed:", e)
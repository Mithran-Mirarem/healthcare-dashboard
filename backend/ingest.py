import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from pathlib import Path

# Correct .env path
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path, encoding="utf-8")

DB_URL = os.getenv("DB_URL")

print("DB_URL =", DB_URL)  # debug

engine = create_engine(DB_URL)

try:
    df = pd.read_csv("data/raw.csv")

    df.dropna(inplace=True)

    df['admission_date'] = pd.to_datetime(df['admission_date'])
    df['discharge_date'] = pd.to_datetime(df['discharge_date'])

    df['length_of_stay'] = (df['discharge_date'] - df['admission_date']).dt.days

    df = df[df['length_of_stay'] >= 0]

    df.to_sql("patients", engine, if_exists="replace", index=False)

    print("Data loaded successfully:", len(df), "rows")

except Exception as e:
    print("Error:", e)
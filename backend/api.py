from fastapi import FastAPI
from sqlalchemy import create_engine
import pandas as pd

app = FastAPI()

import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL)
def load_data():
    return pd.read_sql("SELECT * FROM patients", engine)
@app.get("/kpis")
def get_kpis():
    df = load_data()

    total_patients = len(df)
    avg_stay = df['length_of_stay'].mean()
    total_revenue = df['cost'].sum()

    return {
        "total_patients": int(total_patients),
        "avg_length_of_stay": float(round(avg_stay, 2)),
        "total_revenue": float(total_revenue)
    }
@app.get("/admissions_trend")
def admissions_trend():
    df = load_data()

    trend = df.groupby(df['admission_date'].dt.date).size().reset_index(name='count')

    return trend.to_dict(orient="records")
@app.get("/diagnosis_distribution")
def diagnosis_distribution():
    df = load_data()

    diag = df['diagnosis'].value_counts().reset_index()
    diag.columns = ['diagnosis', 'count']

    return diag.to_dict(orient="records")
@app.get("/department_stats")
def department_stats():
    df = load_data()

    dept = df.groupby('department').agg({
        'patient_id': 'count',
        'cost': 'sum',
        'length_of_stay': 'mean'
    }).reset_index()

    dept.columns = ['department', 'patients', 'total_cost', 'avg_stay']

    return dept.to_dict(orient="records")
@app.get("/readmission_rate")
def readmission_rate():
    df = load_data()

    # fake logic: same patient appears multiple times
    readmissions = df['patient_id'].duplicated().sum()
    total = len(df)

    rate = (readmissions / total) * 100

    return {"readmission_rate_percent": round(rate, 2)}
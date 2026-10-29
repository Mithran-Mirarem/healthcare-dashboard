import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import os
from dotenv import load_dotenv
from pathlib import Path

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Healthcare Dashboard", layout="wide")

# Load env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL)

st.title("Healthcare Analytics Dashboard")

# ------------------ LOGIN ------------------
def login():
    st.sidebar.title("Login")

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if username == "admin" and password == "1234":
        return True
    elif username or password:
        st.sidebar.error("Invalid credentials")
        return False

    return False

if not login():
    st.stop()

# ------------------ LOAD DATA ------------------
@st.cache_data
def load_data():
    return pd.read_sql("SELECT * FROM patients", engine)

with st.spinner("Loading data..."):
    df = load_data()

st.markdown("## ➕ Add New Patient")

with st.form("patient_form"):
    col1, col2 = st.columns(2)

    with col1:
        patient_id = st.number_input("Patient ID", min_value=1)
        admission_date = st.date_input("Admission Date")
        discharge_date = st.date_input("Discharge Date")
        diagnosis = st.text_input("Diagnosis")

        severity = st.selectbox("Severity", ["Low", "Medium", "High"])
        treatment = st.selectbox("Treatment", ["Medication", "Surgery", "ICU Care"])

    with col2:
        department = st.selectbox("Department", ["General", "ICU", "Emergency", "Surgery"])
        cost = st.number_input("Cost", min_value=0)
        age = st.number_input("Age", min_value=0)
        gender = st.selectbox("Gender", ["Male", "Female"])

        insurance = st.selectbox("Insurance", ["Yes", "No"])
        payment_type = "Insurance" if insurance == "Yes" else "Cash"

        bed_type = st.selectbox("Bed Type", ["General", "ICU", "Private"])
        doctor = st.selectbox("Doctor", ["Dr. Smith", "Dr. John", "Dr. Lee"])

    submit = st.form_submit_button("Add Patient")

if submit:
    length_of_stay = (pd.to_datetime(discharge_date) - pd.to_datetime(admission_date)).days

    new_data = pd.DataFrame([{
        "patient_id": patient_id,
        "admission_date": admission_date,
        "discharge_date": discharge_date,
        "diagnosis": diagnosis,
        "department": department,
        "cost": cost,
        "age": age,
        "gender": gender,
        "severity": severity,
        "treatment": treatment,
        "insurance": insurance,
        "payment_type": payment_type,
        "bed_type": bed_type,
        "doctor": doctor,
        "length_of_stay": length_of_stay
    }])

    new_data.to_sql("patients", engine, if_exists="append", index=False)

    st.success("✅ Patient added successfully!")

    st.cache_data.clear()
    st.rerun()
# ------------------ FILTERS ------------------
st.sidebar.header("Filters")

# Department filter
dept = st.sidebar.selectbox("Department", ["All"] + list(df['department'].unique()))
if dept != "All":
    df = df[df['department'] == dept]

# Date filter (FIXED)
date_range = st.sidebar.date_input(
    "Select Date Range",
    [df['admission_date'].min(), df['admission_date'].max()]
)

if len(date_range) == 2:
    start_date, end_date = date_range
    df = df[
        (df['admission_date'] >= pd.to_datetime(start_date)) &
        (df['admission_date'] <= pd.to_datetime(end_date))
    ]

# ------------------ KPIs ------------------
st.markdown("## KPIs Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Patients", len(df))
col2.metric("Avg Stay", round(df['length_of_stay'].mean(), 2))
col3.metric("Total Revenue", int(df['cost'].sum()))

# Bed occupancy
total_days = df['length_of_stay'].sum()
capacity = 1000
occupancy_rate = (total_days / (capacity * 365)) * 100

col4.metric("Bed Occupancy %", round(occupancy_rate, 2))

# ------------------ CHARTS ------------------
st.markdown("## Trends & Analysis")

# Trend
trend = df.groupby(df['admission_date'].dt.date).size().reset_index(name='count')
fig1 = px.line(trend, x='admission_date', y='count', title="Admissions Over Time")

# Diagnosis
diag = df['diagnosis'].value_counts().reset_index()
diag.columns = ['diagnosis', 'count']
fig2 = px.bar(diag, x='diagnosis', y='count', title="Diagnosis Distribution")

# Revenue
dept_data = df.groupby('department')['cost'].sum().reset_index()
fig3 = px.pie(dept_data, names='department', values='cost', title="Revenue by Department")

# Layout
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1, key="trend")

with col2:
    st.plotly_chart(fig2, key="diag")

st.plotly_chart(fig3, key="pie")

# ------------------ DATA TABLE ------------------
st.markdown("### Raw Data Preview")
st.dataframe(df.head(50))
import pandas as pd
import random
from datetime import datetime, timedelta

NUM_RECORDS = 1000

diagnoses = ["Flu", "Covid", "Fever", "Infection", "Diabetes", "Hypertension"]
departments = ["General", "ICU", "Emergency", "Surgery", "Cardiology"]
genders = ["Male", "Female"]
severity_levels = ["Low", "Medium", "High"]
treatments = ["Medication", "Surgery", "ICU Care"]
bed_types = ["General", "ICU", "Private"]
doctors = ["Dr. Smith", "Dr. John", "Dr. Lee", "Dr. Kumar"]

data = []
start_date = datetime(2023, 1, 1)

for i in range(1, NUM_RECORDS + 1):

    admission = start_date + timedelta(days=random.randint(0, 365))
    stay_days = random.randint(1, 10)
    discharge = admission + timedelta(days=stay_days)

    diagnosis = random.choice(diagnoses)
    department = random.choice(departments)

    age = random.randint(1, 90)
    gender = random.choice(genders)

    severity = random.choice(severity_levels)
    treatment = random.choice(treatments)

    insurance = random.choice(["Yes", "No"])
    payment = "Insurance" if insurance == "Yes" else "Cash"

    bed = random.choice(bed_types)
    doctor = random.choice(doctors)

    # smarter cost logic
    if department == "ICU":
        cost = random.randint(8000, 20000)
    elif department == "Surgery":
        cost = random.randint(10000, 25000)
    else:
        cost = random.randint(1000, 6000)

    data.append([
        i, admission, discharge, diagnosis, department, cost,
        age, gender, severity, treatment, insurance, payment, bed, doctor
    ])

df = pd.DataFrame(data, columns=[
    "patient_id", "admission_date", "discharge_date",
    "diagnosis", "department", "cost",
    "age", "gender", "severity", "treatment",
    "insurance", "payment_type", "bed_type", "doctor"
])

df.to_csv("data/raw.csv", index=False)

print("Dataset created with", len(df), "rows")
import pandas as pd
import random
from app.database import engine
from app.database import Base
from app import models  # VERY IMPORTANT
print("DATABASE PATH:", engine.url)
# Create tables before inserting
Base.metadata.create_all(bind=engine)
from app.database import SessionLocal
from app.models import User, Consumption

db = SessionLocal()

# ============================================
# LOAD CUSTOMER FILE
# ============================================
customer_df = pd.read_csv("data/raw/customer.csv")

import random

def generate_mobile():
    return str(random.randint(6000000000, 9999999999))

# ============================================
# CLEAN & FIX MOBILE COLUMN SAFELY
# ============================================

cleaned_mobiles = []
seen = set()

for value in customer_df["MOBILE"]:

    # Convert everything safely to string
    mobile = str(value).replace(".0", "").strip()

    # Fix invalid / null values
    if mobile == "nan" or not mobile.isdigit() or len(mobile) != 10:
        mobile = generate_mobile()

    # Fix duplicates
    if mobile in seen:
        new_mobile = generate_mobile()
        while new_mobile in seen:
            new_mobile = generate_mobile()
        mobile = new_mobile

    seen.add(mobile)
    cleaned_mobiles.append(mobile)

customer_df["MOBILE"] = cleaned_mobiles

print("Mobile cleaning completed.")
print("Total unique mobiles:", customer_df["MOBILE"].nunique())

# ============================================
# CLEAN & FIX METER SERIAL SAFELY
# ============================================

def generate_meter():
    return "MTR" + str(random.randint(1000000, 9999999))

cleaned_meters = []
seen_meters = set()

for value in customer_df["MTR_SRL_NO"]:

    meter = str(value).strip()

    # Fix null or invalid
    if meter == "nan" or meter == "":
        meter = generate_meter()

    # Fix duplicates
    if meter in seen_meters:
        new_meter = generate_meter()
        while new_meter in seen_meters:
            new_meter = generate_meter()
        meter = new_meter

    seen_meters.add(meter)
    cleaned_meters.append(meter)

customer_df["MTR_SRL_NO"] = cleaned_meters

print("Meter cleaning completed.")
print("Total unique meters:", customer_df["MTR_SRL_NO"].nunique())
# ============================================
# INSERT CUSTOMERS INTO DATABASE
# ============================================

customer_objects = []

for _, row in customer_df.iterrows():
    customer_objects.append(
        User(
            acct_id=str(row["ACCT_ID"]),
            name=row["NAME"],
            address=row["ADDRESS"],
            mobile=row["MOBILE"],
            tariff_type=row["TARIFF_TYPE"],
            s_t=row["S/T"],
            mtr_srl_no=str(row["MTR_SRL_NO"]),
            load=row["LOAD"],
            metr_status=row["METR_STATUS"]
        )
    )

db.bulk_save_objects(customer_objects)
db.commit()

print("Customers uploaded successfully!")

# ============================================
# INSERT CONSUMPTION DATA
# ============================================

consume_df = pd.read_csv("data/cleaned_consume.csv")

consumption_objects = []

for _, row in consume_df.iterrows():
    consumption_objects.append(
        Consumption(
            acct_id=str(row["ACCT_ID"]),
            year=int(row["YEAR"]),
            month=row["MONTH"],
            kwh=row["KWH"]
        )
    )

db.bulk_save_objects(consumption_objects)
db.commit()

print("Consumption uploaded successfully!")

db.close()
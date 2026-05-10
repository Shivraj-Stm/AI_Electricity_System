from fastapi import APIRouter, HTTPException
from app.database import SessionLocal
from app.models import User, Consumption
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, timedelta
import random


router = APIRouter(prefix="/user", tags=["User"])


# ================= OTP TEMP STORAGE =================
otp_store = {}

def generate_otp():
    return str(random.randint(100000, 999999))


# ================= SEND OTP =================
class RegisterRequest(BaseModel):
    identifier: str   # mobile or meter number


@router.post("/send-otp")
def send_otp(data: RegisterRequest):

    db: Session = SessionLocal()

    try:
        user = db.query(User).filter(
            (User.mobile == data.identifier) |
            (User.mtr_srl_no == data.identifier)
        ).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        otp = generate_otp()

        # store OTP using the identifier entered
        otp_store[data.identifier] = {
            "otp": otp,
            "expires_at": datetime.utcnow() + timedelta(minutes=2),
            "attempts": 0
        }

        print("Generated OTP:", otp)

        return {"message": "OTP sent successfully"}

    finally:
        db.close()


# ================= VERIFY OTP =================
class VerifyOTP(BaseModel):
    identifier: str
    otp: str


@router.post("/verify-otp")
def verify_otp(data: VerifyOTP):

    record = otp_store.get(data.identifier)

    if not record:
        raise HTTPException(status_code=400, detail="OTP not requested")

    if datetime.utcnow() > record["expires_at"]:
        raise HTTPException(status_code=400, detail="OTP expired")

    # safe comparison
    if str(record["otp"]) != str(data.otp):
        record["attempts"] += 1
        raise HTTPException(status_code=400, detail="Invalid OTP")

    db: Session = SessionLocal()

    try:
        user = db.query(User).filter(
            (User.mobile == data.identifier) |
            (User.mtr_srl_no == data.identifier)
        ).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # remove OTP after successful login
        del otp_store[data.identifier]

        return {
            "status": "success",
            "acct_id": user.acct_id
        }

    finally:
        db.close()


# ================= USER DASHBOARD =================
@router.get("/dashboard/{acct_id}")
def get_dashboard(acct_id: str):

    db: Session = SessionLocal()

    try:
        user = db.query(User).filter(User.acct_id == acct_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        consumptions = (
            db.query(Consumption)
            .filter(Consumption.acct_id == acct_id)
            .order_by(Consumption.year.desc())
            .limit(6)
            .all()
        )

        last_6_months = [
            {
                "year": c.year,
                "month": c.month,
                "units": c.kwh
            }
            for c in consumptions
        ]

        return {
            "acct_id": user.acct_id,
            "name": user.name,
            "address": user.address,
            "mobile": user.mobile,
            "tariff": user.tariff_type,
            "meter_number": user.mtr_srl_no,
            "connection_status": user.metr_status,
            "load": user.load,
            "last_6_months": last_6_months
        }

    finally:
        db.close()

# ================= USER HISTORY===================
@router.get("/history/{acct_id}")
def get_history(acct_id: str):

    db: Session = SessionLocal()

    try:
        user = db.query(User).filter(User.acct_id == acct_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        records = (
            db.query(Consumption)
            .filter(Consumption.acct_id == user.acct_id)
            .all()
        )

        month_order = {
            "Jan":1,"Feb":2,"Mar":3,"Apr":4,
            "May":5,"Jun":6,"Jul":7,"Aug":8,
            "Sep":9,"Oct":10,"Nov":11,"Dec":12
        }

        records = sorted(
            records,
            key=lambda r: (r.year, month_order.get(r.month, 0))
        )

        TARIFF_RATE = 7

        history = [
            {
                "year": r.year,
                "month": r.month,
                "units": r.kwh,
                "bill": round(r.kwh * TARIFF_RATE),
                "status": "Paid"
            }
            for r in records
        ]

        return history

    finally:
        db.close()

@router.get("/bill/{acct_id}")
def get_bill(acct_id: str):

    db: Session = SessionLocal()

    try:
        records = (
            db.query(Consumption)
            .filter(Consumption.acct_id == acct_id)
            .order_by(Consumption.year.desc())
            .all()
        )

        if not records:
            raise HTTPException(status_code=404, detail="No data found")

        TARIFF_RATE = 7

        # latest month → current bill
        latest = records[0]
        current_bill = round(latest.kwh * TARIFF_RATE)

        # previous month → last payment
        previous = records[1] if len(records) > 1 else None

        last_payment_amount = round(previous.kwh * TARIFF_RATE) if previous else 0
        last_payment_date = f"{previous.month} {previous.year}" if previous else "N/A"

        # simulate partial payment (demo)
        paid = current_bill * 0.35
        remaining = current_bill - paid

        return {
            "month": latest.month,
            "year": latest.year,
            "units": latest.kwh,
            "current_bill": current_bill,

            "last_payment_amount": last_payment_amount,
            "last_payment_date": last_payment_date,

            "paid": paid,
            "remaining": remaining
        }

    finally:
        db.close()
#============pay=============
#@router.post("/pay/{acct_id}")
def pay_bill(acct_id: str):

    db: Session = SessionLocal()

    try:
        records = (
            db.query(Consumption)
            .filter(Consumption.acct_id == acct_id)
            .order_by(Consumption.year.desc())
            .all()
        )

        if not records:
            raise HTTPException(status_code=404, detail="No data found")

        TARIFF_RATE = 7

        # calculate total
        total = sum(round(r.kwh * TARIFF_RATE) for r in records)

        # simulate payment → mark all as paid
        paid = total
        remaining = 0

        return {
            "message": "Payment successful",
            "paid": paid,
            "remaining": remaining
        }

    finally:
        db.close()   
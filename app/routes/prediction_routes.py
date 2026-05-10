from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import pandas as pd
import joblib
from datetime import datetime

router = APIRouter()

# ------------------ Load Model ------------------
model = joblib.load("ml/best_prediction_model.pkl")
print("Loaded model features:", model.feature_names_in_)

# ------------------ Request Model ------------------
class PredictionRequest(BaseModel):
    acct_id: int
    months: int


# ------------------ Response Model ------------------
class PredictionItem(BaseModel):
    month: str
    predicted_units: float


class PredictionResponse(BaseModel):
    predictions: List[PredictionItem]


# ------------------ Season Function ------------------
def get_season(month):
    if month in [3,4,5]:
        return 1   # Summer
    elif month in [6,7,8]:
        return 2   # Monsoon
    elif month in [9,10,11]:
        return 3   # Autumn
    else:
        return 4   # Winter


# ------------------ Prediction Route ------------------
@router.post("/predict", response_model=PredictionResponse)
def predict(data: PredictionRequest):

    df = pd.read_csv("data/cleaned_consume.csv")

    user_data = df[df["ACCT_ID"] == data.acct_id].copy()

    if len(user_data) < 3:
        return PredictionResponse(predictions=[])

    user_data["DATE"] = pd.to_datetime(
        user_data["MONTH"] + " " + user_data["YEAR"].astype(str),
        format="%b %Y"
    )

    user_data = user_data.sort_values("DATE")

    lag_1 = user_data.iloc[-1]["KWH"]
    lag_2 = user_data.iloc[-2]["KWH"]
    lag_3 = user_data.iloc[-3]["KWH"]

    predictions = []

    for i in range(1, data.months + 1):

        #  correct future date
        future_date = datetime.now().replace(day=1)
        future_date = pd.Timestamp(future_date) + pd.DateOffset(months=i-1)

        month_num = future_date.month
        year_num = future_date.year
        season = get_season(month_num)

        input_data = pd.DataFrame([{
            "lag_1": lag_1,
            "lag_2": lag_2,
            "lag_3": lag_3,
            "month_num": month_num,
            "year_num": year_num,
            "season": season
        }])

        predicted_units = model.predict(input_data)[0]

        #  correct month name
        month_name = future_date.strftime("%b %Y")

        predictions.append({
            "month": month_name,
            "predicted_units": round(predicted_units, 2)
        })

        # update lag values
        lag_3 = lag_2
        lag_2 = lag_1
        lag_1 = predicted_units

    return PredictionResponse(predictions=predictions)
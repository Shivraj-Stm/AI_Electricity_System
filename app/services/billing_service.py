import pandas as pd

def get_bill_history():
    df = pd.read_csv("app/data/cleaned_consume.csv")

    # Optional: rename columns for frontend clarity
    df = df.rename(columns={
        "consumption": "units",
        "bill_amount": "amount"
    })

    return df.to_dict(orient="records")
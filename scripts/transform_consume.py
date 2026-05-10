import pandas as pd

# Load file
df = pd.read_csv("data/raw/consume.csv")

# Clean account id
df["ACCT_ID"] = df["ACCT_ID"].astype(str).str.replace(".0", "", regex=False)

# Define months
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

years = ["2022", "2023", "2024"]

final_rows = []

col_index = 1  # start after ACCT_ID

for year in years:
    for month in months:
        col_name = df.columns[col_index]

        for i, row in df.iterrows():
            final_rows.append({
                "ACCT_ID": row["ACCT_ID"],
                "YEAR": int(year),
                "MONTH": month,
                "KWH": row[col_name]
            })

        col_index += 1

# Create clean dataframe
df_clean = pd.DataFrame(final_rows)

# Remove null values
df_clean = df_clean.dropna()

print("Preview of cleaned data:")
print(df_clean.head())

# Save cleaned file
df_clean.to_csv("data/cleaned_consume.csv", index=False)

print("\nCleaned file saved successfully!")
import pandas as pd
import numpy as np
import joblib

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor

# ------------LOAD DATASET----------
df = pd.read_csv("data/cleaned_consume.csv")

# ------------ CREATE DATE COLUMN----------------
df["DATE"] = pd.to_datetime(
    df["MONTH"] + " " + df["YEAR"].astype(str),
    format="%b %Y"
)
df = df.sort_values(["ACCT_ID", "DATE"])
# ----------- ADD SEASON FEATURE -------------
def get_season(month):
    if month in [3,4,5]:
        return 1   # Summer
    elif month in [6,7,8]:
        return 2   # Monsoon
    elif month in [9,10,11]:
        return 3   # Autumn
    else:
        return 4   # Winter

df["season"] = df["DATE"].dt.month.apply(get_season)


# ----------------- CREATE LAG FEATURES------------------
df["lag_1"] = df.groupby("ACCT_ID")["KWH"].shift(1)
df["lag_2"] = df.groupby("ACCT_ID")["KWH"].shift(2)
df["lag_3"] = df.groupby("ACCT_ID")["KWH"].shift(3)

df = df.dropna()


# --------------- FEATURE ENGINEERING-------------------
df["month_num"] = df["DATE"].dt.month
df["year_num"] = df["DATE"].dt.year


# ----------------- DROP UNUSED COLUMNS-------------------
df = df.drop(columns=["ACCT_ID", "YEAR", "MONTH", "DATE"], errors="ignore")


# ----------------- FINAL FEATURES-------------------
df = df[[
    "lag_1",
    "lag_2",
    "lag_3",
    "month_num",
    "year_num",
    "season",
    "KWH"
]]


# ------------- FEATURES & TARGET-------------------
X = df.drop("KWH", axis=1)
y = df["KWH"]


# ----------------- TRAIN-TEST SPLIT-------------------
split_index = int(len(df) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]


# ----------------- EVALUATION FUNCTION-------------------
def evaluate_model(name, model):
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, pred)
    mse = mean_squared_error(y_test, pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, pred)

    print("\nModel:", name)
    print("MAE :", round(mae, 2))
    print("RMSE:", round(rmse, 2))
    print("R2  :", round(r2, 4))

    print("\nSample Predictions:")
    for i in range(5):
        print("Actual:", y_test.iloc[i], "Predicted:", round(pred[i], 2))

    

    return rmse, model


# ----------------- RANDOM FOREST BASE------------------
rf_base = RandomForestRegressor(random_state=42)
rmse_rf_base, rf_base = evaluate_model("RF Base", rf_base)


# ----------------- RANDOM FOREST TUNED------------------
rf_params = {
    "n_estimators": [100, 200, 300],
    "max_depth": [5, 10, 7],
    "min_samples_split": [2, 5, 10]
}

rf_search = RandomizedSearchCV(
    RandomForestRegressor(random_state=42),
    rf_params,
    n_iter=5,
    cv=2,
    n_jobs=-1
)

rf_search.fit(X_train, y_train)
rf_tuned = rf_search.best_estimator_
rmse_rf_tuned, rf_tuned = evaluate_model("RF Tuned", rf_tuned)


# ----------------- XGBOOST BASE------------------
xgb_base = XGBRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=5,
    random_state=42
)

rmse_xgb_base, xgb_base = evaluate_model("XGB Base", xgb_base)

# ----------------- XGBOOST TUNED------------------
xgb_params = {
    "n_estimators": [100, 200, 300],
    "max_depth": [3, 5, 7],
    "learning_rate": [0.01, 0.05, 0.1]
}

xgb_search = RandomizedSearchCV(
    XGBRegressor(random_state=42),
    xgb_params,
    n_iter=5,
    cv=2,
    n_jobs=-1
)

xgb_search.fit(X_train, y_train)
xgb_tuned = xgb_search.best_estimator_
rmse_xgb_tuned, xgb_tuned = evaluate_model("XGB Tuned", xgb_tuned)

# ----------------- LIGHTGBM BASE------------------
lgb_base = LGBMRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=5,
    random_state=42,
    verbose=-1
)

rmse_lgb_base, lgb_base = evaluate_model("LGB Base", lgb_base)


# ----------------- LIGHTGBM TUNED------------------
lgb_params = {
    "n_estimators": [100, 200, 300],
    "max_depth": [3, 5, 7],
    "learning_rate": [0.01, 0.05, 0.1],
    "num_leaves": [20, 30]
}

lgb_search = RandomizedSearchCV(
    LGBMRegressor(random_state=42, verbose=-1),
    lgb_params,
    n_iter=5,
    cv=2,
    n_jobs=-1
)
lgb_search.fit(X_train, y_train)
lgb_tuned = lgb_search.best_estimator_
rmse_lgb_tuned, lgb_tuned = evaluate_model("LGB Tuned", lgb_tuned)

# ----------------- SAVE ALL MODELS-------------------
models = {
    "rf_base": rf_base,
    "rf_tuned": rf_tuned,
    "xgb_base": xgb_base,
    "xgb_tuned": xgb_tuned,
    "lgb_base": lgb_base,
    "lgb_tuned": lgb_tuned
}
joblib.dump(models, "all_models.pkl")

# ----------------- SAVE SCORES-------------------
model_scores = {
    "rf_base": rmse_rf_base,
    "rf_tuned": rmse_rf_tuned,
    "xgb_base": rmse_xgb_base,
    "xgb_tuned": rmse_xgb_tuned,
    "lgb_base": rmse_lgb_base,
    "lgb_tuned": rmse_lgb_tuned
}
joblib.dump(model_scores, "model_scores.pkl")

# ----------------- SAVE FEATURES-------------------
joblib.dump(X.columns.tolist(), "features.pkl")
print("\n All models saved successfully!")

# ----------------- FIND BEST MODEL-------------------
best_model_name = min(model_scores, key=model_scores.get)
best_rmse = model_scores[best_model_name]

print("\n Best Model:", best_model_name)
print(" Best RMSE:", round(best_rmse, 2))

# ----------------- SAVE BEST MODEL-------------------
best_model = models[best_model_name]
joblib.dump(best_model, "ml/best_prediction_model.pkl")

print(" Best model saved separately!")
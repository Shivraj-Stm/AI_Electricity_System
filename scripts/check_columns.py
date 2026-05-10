import pandas as pd

customer = pd.read_csv("data/raw/customer.csv")
consume = pd.read_csv("data/raw/consume.csv")

print("Customer Columns:")
print(customer.columns)

print("\nConsume Columns:")
print(consume.columns)
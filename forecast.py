import pandas as pd

df = pd.read_excel("Shyan_Synthetic_Travel_Cost_Data.xlsx", sheet_name="Trips")
print("Dataset loaded successfully!")
print(df.head())
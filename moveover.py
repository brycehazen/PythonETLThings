import pandas as pd
import numpy as np

df = pd.read_csv("C:/users/bhoward/desktop/stoof/input/2-14 Corpus Christi  6-23-22.csv" , encoding = "Latin")
pd.set_option('display.max_columns', None)

df = df[(df['ConsCodeImpID'].str.startswith('*',na=False))|(df['ConsID'].notna())]
df['ConsID'] = np.where(((df['ConsID'].isna())&(df['ConsCodeImpID'].notna())),df['ConsCodeImpID'],df['ConsID'])

df.to_csv( "C:/users/bhoward/desktop/stoof/output/Moved.csv" ,index=True)




import pandas as pd
import glob
import os

df = pd.read_csv("C:/Users/bhoward/Desktop/Stoof/Input/MASTER - 2022 All Parishes Information .csv" , encoding = "ISO-8859-1")

df_new = df.drop_duplicates(subset=['ConsID'])
    
df_new.to_csv( "C:/Users/bhoward/Desktop/Stoof/Output/DupesRemoved.csv", index=False )


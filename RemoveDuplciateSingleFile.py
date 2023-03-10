import pandas as pd
import glob
import os

df = pd.read_csv("C:/Users/bhoward/Desktop/Stoof/Input/BLANK_PR.CSV" , encoding='latin-1', low_memory=False)

# df['CnAdrPrf_Addrline1_EDIT'] = df['CnAdrPrf_Addrline1'].str.strip()
# df['CnAdrPrf_Addrline1_EDIT'] = df['CnAdrPrf_Addrline1'].str.lower()

# df["CnAdrPrf_Addrline1_EDIT"] = df['CnAdrPrf_Addrline1_EDIT'].str.replace('[^\w\s]','')

df_new = df.drop_duplicates(subset=['Constituent ID'])
    
df_new.to_csv( "C:/Users/bhoward/Desktop/Stoof/Output/EXPORTBLANK_PR.csv", index=False )


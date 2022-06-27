import pandas as pd
import glob
import os
import numpy as np

df = pd.read_csv("C:/Users/file.csv" , encoding = "ISO-8859-1")

df['title'] = df['CnBio_Title_1'].apply(lambda x: 'Mrs.' if x == 'Mr.' else 'Mr.')

df = df.drop('CnBio_Title_1', 1)

df.to_csv( "C:/Users/bhoward/Folder1/ColumnChangeSPtitleSwap.csv", index=False )






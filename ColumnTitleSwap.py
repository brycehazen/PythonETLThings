import pandas as pd
import glob
import os
import numpy as np

df = pd.read_csv("C:/Users/bhoward/Desktop/Folder/TEST COPYDF.csv" , encoding = "ISO-8859-1")

# df_new = df.drop_duplicates(subset=['constid'])


# df.loc[df_new['CnBio_Title_1'] > 1990, 'First Season'] = 1
# df


# Changes the 'is_electric' column based on value in the 'type' column
# If the 'type' column == 'electric' then the 'is_electric' becomes 'YES'
# df_new =df['CnSpSpBio_Title_1']= df['CnBio_Title_1'].apply(lambda x: 'Mrs.' if (x == 'Mr.') else 'Mr.') 
# df_new =df['CnSpSpBio_Title_1']= df['CnBio_Title_1'].apply(lambda x: 'Mr' if (x == 'Mrs.') else 'Mrs.') 
# df_new = df.loc[(df_new.CnBio_Title_1 = 'Mr.') | (df_new.C > 15), 'C'] = np.nan

# df.loc[df['CnBio_Title_1'] == 'Mr.' ,'CnBio_Title_1'] = 'Mrs.'
df['title'] = df['CnBio_Title_1'].apply(lambda x: 'Mrs.' if x == 'Mr.' else 'Mr.')

df = df.drop('CnBio_Title_1', 1)

df.to_csv( "C:/Users/bhoward/Folder1/ColumnChangeSPtitleSwap.csv", index=False )

def titleChange(change):

    titles = ['Mr.', 'Mrs.', 'Miss', 'Ms.' ]

    for title in titles:
        if title in change
        




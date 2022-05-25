import pandas as pd 
import numpy as np

# Read file
df = pd.read_csv("C:/Users/bhoward/Desktop/Stoof/input/Final copy for mailing - consID only.csv", encoding='latin-1' )

#np.reshape(df.values,(500,28))

# Reshape 14,000 into 28 columns with 500 in each column
# 1 was used to make dataframe and even number to divide 500 by
df = pd.DataFrame(np.reshape(df.values,(500,28)))

# Make cell blank if it has 0
df[df<1] = np.nan 

# Remove first row 
df = df.iloc[1: , :]

# Export file
df.to_csv("C:/Users/bhoward/Desktop/Stoof/output/RowToCol.csv", index = False)

print(df)

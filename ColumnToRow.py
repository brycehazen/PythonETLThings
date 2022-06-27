import pandas as pd


#reads csv to be transposed
df = pd.read_csv("C:/Users/bhoward/Desktop/Folder/TESTJanetCaramelloExportSolicitor.csv" , encoding = "ISO-8859-1")

#uses Melt to take 3 columns to keep, then puts everything else under 2 new columns
df1 = df.melt(id_vars=[ "CnBio_ID" , "CnBio_Import_ID", "CnRelSol_1_01_Import_ID" ,"CnRelSol_1_01_Solicitor_Type","CnRelSol_1_02_Solicitor_Type","CnRelSol_1_03_Solicitor_Type","CnRelSol_1_04_Solicitor_Type"], 
        var_name="Import_ID",
        value_name="Solicitor_Type")

#outputs new file. 
df1.to_csv( "C:/Users/bhoward/Folder1/TESTJanetCaramelloExportSolicitor.csv", index=False )

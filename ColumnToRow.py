import pandas as pd


#reads csv to be transposed
df = pd.read_csv("C:/Users/bhoward/Desktop/Folder/TESTJanetCaramelloExportSolicitor.csv" , encoding = "ISO-8859-1")

#uses Melt to take 3 columns to keep, then puts everything else under 2 new columns
df1 = df.melt(id_vars=[ "CnBio_ID" , "CnBio_Import_ID", "CnRelSol_1_01_Import_ID" ,"CnRelSol_1_01_Solicitor_Type","CnRelSol_1_02_Solicitor_Type","CnRelSol_1_03_Solicitor_Type","CnRelSol_1_04_Solicitor_Type"], 
        var_name="Import_ID",
        value_name="Solicitor_Type")

#outputs new file. 
df1.to_csv( "C:/Users/bhoward/Folder1/TESTJanetCaramelloExportSolicitor.csv", index=False )


########## Example Problem ####################################
# location    name    Jan-2010    Feb-2010    March-2010
# A           "test"  12          20          30
# B           "foo"   18          20          25


#  What I would like is for it to look like
# location    name    Date        Value
# A           "test"  Jan-2010    12       
# A           "test"  Feb-2010    20
# A           "test"  March-2010  30
# B           "foo"   Jan-2010    18       
# B           "foo"   Feb-2010    20
# B           "foo"   March-2010  25


########## Solution ##########################################
# df.melt(id_vars=["location", "name"], 
#         var_name="Date", 
#         value_name="Value")

#   location    name        Date  Value
# 0        A  "test"    Jan-2010     12
# 1        B   "foo"    Jan-2010     18
# 2        A  "test"    Feb-2010     20
# 3        B   "foo"    Feb-2010     20
# 4        A  "test"  March-2010     30
# 5        B   "foo"  March-2010     25
import csv
import pandas as pd


file_path = "C:/Users/bhoward/Desktop/Stoof/Input/EXPORT.CSV"
output_path = "C:/Users/bhoward/Desktop/Stoof/Input/EXPORT_no_errors.csv"

# Open the input file and the output file
with open(file_path, encoding='latin-1') as f_in, open(output_path, 'w', encoding='latin-1', newline='') as f_out:
    # Create a CSV reader and writer objects
    reader = csv.reader(f_in)
    writer = csv.writer(f_out)
    
    # Loop through the rows of the input file
    for i, row in enumerate(reader):
        try:
            # Try to write the row to the output file
            writer.writerow(row)
        except csv.Error as e:
            # If there's an error, print the error message and skip the row
            print(f"Error on line {i}: {e}")
            continue

# Read the cleaned CSV file with pandas
df = pd.read_csv(output_path, low_memory=False)

# Continue with the rest of your script using the `df` dataframe
df_new = df.drop_duplicates(subset=['Gift Attribute Category'])
df_new.to_csv("C:/Users/bhoward/Desktop/Stoof/Output/EXPORTGift Attribute Category.csv", index=False)

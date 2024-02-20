#######################################################################################
######   Use this after running Labels. File must have _clean in the file name    #####
######   This will add two new columns Bishop_Addressee Bishop_Salutation         #####
#######################################################################################
import os
import pandas as pd

def process_file(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Initialize new columns with empty strings to ensure the DataFrame's shape is correct
    df['Bishop_Addressee'] = ''
    df['Bishop_Salutation'] = ''
    
    # Processing each row for the new columns
    for index, row in df.iterrows():
        # Skip row if first and last names are blank
        if pd.isna(row['CnBio_First_Name']) and pd.isna(row['CnBio_Last_Name']):
            continue
        
        # Formulating Bishop_Addressee and Bishop_Salutation
        first_name = row['CnBio_First_Name'] if not pd.isna(row['CnBio_First_Name']) else ''
        last_name = row['CnBio_Last_Name'] if not pd.isna(row['CnBio_Last_Name']) else ''
        spouse_first_name = row['CnSpSpBio_First_Name'] if not pd.isna(row['CnSpSpBio_First_Name']) else ''

        if spouse_first_name:
            addressee = f"{first_name} and {spouse_first_name} {last_name}"
            salutation = f"{first_name} and {spouse_first_name}"
        else:
            addressee = f"{first_name} {last_name}"
            salutation = first_name
        
        df.at[index, 'Bishop_Addressee'] = addressee
        df.at[index, 'Bishop_Salutation'] = salutation
    
    # Insert the new columns at the desired positions
    # Temporarily store the data of the new columns
    bishop_addressee_data = df.pop('Bishop_Addressee')
    bishop_salutation_data = df.pop('Bishop_Salutation')
    
    # Insert the stored data into the specified positions
    df.insert(12, 'Bishop_Addressee', bishop_addressee_data)
    df.insert(13, 'Bishop_Salutation', bishop_salutation_data)

    # Saving the processed file
    new_file_path = os.path.splitext(file_path)[0] + '_BishAddSal.csv'
    df.to_csv(new_file_path, index=False)

def main():
    # Getting the directory where the script is located
    directory = os.path.dirname(os.path.realpath(__file__))
    
    # Processing each CSV file in the directory
    for file in os.listdir(directory):
        if file.endswith('_clean.csv'):
            process_file(os.path.join(directory, file))

if __name__ == "__main__":
    main()

import os
import glob
import pandas as pd
from tqdm import tqdm

def read_csv_files(folder_path):
    df_list = []  # Initialize a list to store DataFrames
    csv_files = glob.glob(os.path.join(folder_path, '*.csv'))  # Find all CSV files in the folder
    # Initialize tqdm progress bar for reading CSV files
    with tqdm(csv_files, desc="Reading CSVs") as pbar:
        for file_path in pbar:  # Loop through each file path in the progress bar
            if "Realm" not in file_path:  # Skip files with 'Realm' in their name
                # Read CSV file into DataFrame
                df = pd.read_csv(file_path, low_memory=False, encoding='ISO-8859-1', dtype=str)
                df_list.append(df)  # Append DataFrame to the list
                # Update progress bar with file name
                pbar.set_postfix({"File": os.path.basename(file_path)})
    return df_list  # Return list of DataFrames

def separate_rows_with_asterisk(dataframes, file_paths):
    remaining_dfs = []  # List for DataFrames excluding asterisk rows
    asterisk_dfs = []  # List for DataFrames including only asterisk rows
    # Initialize tqdm progress bar for separating rows
    with tqdm(zip(dataframes, file_paths), total=len(dataframes), desc="Separating Rows") as pbar:
        for df, file_path in pbar:  # Loop through each DataFrame and corresponding file path
            if 'ConsID' in df.columns:  # Check if 'ConsID' column exists
                # Separate rows based on 'ConsID' containing asterisks
                asterisk_rows = df[df['ConsID'].str.contains('\*', na=False, regex=True)]
                remaining_rows = df[~df['ConsID'].str.contains('\*', na=False, regex=True)]
                asterisk_dfs.append(asterisk_rows)  # Append to asterisk DataFrame list
                remaining_dfs.append(remaining_rows)  # Append to remaining DataFrame list
            else:
                # Print message if 'ConsID' column not found
                print(f"'ConsID' column not found in file '{os.path.basename(file_path)}', skipping...")
            # Update progress bar with file name
            pbar.set_postfix({"File": os.path.basename(file_path)})
    return remaining_dfs, asterisk_dfs  # Return the separated DataFrames

def save_dataframes_to_excel(dataframes, file_path):
    combined_df = pd.concat(dataframes, ignore_index=True)  # Combine DataFrames into one
    # Initialize tqdm progress bar for saving to Excel
    with tqdm([1], desc="Saving to Excel") as pbar:
        with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:  # Initialize Excel writer
            combined_df.to_excel(writer, index=False, sheet_name='Sheet1')  # Write combined DataFrame to Excel
            workbook = writer.book  # Get the workbook
            worksheet = writer.sheets['Sheet1']  # Get the first worksheet
            num_cols = combined_df.shape[1]  # Number of columns in the DataFrame
            text_format = workbook.add_format({'num_format': '@'})  # Define text format
            for col_idx in range(num_cols):  # Loop through each column
                worksheet.set_column(col_idx, col_idx, None, text_format)  # Set column format to text
            pbar.update(1)  # Update progress bar after saving

def find_mismatched_consids(dataframes):
    # Concatenate all provided DataFrames into a single DataFrame
    combined_df = pd.concat(dataframes, ignore_index=True)

    # Initialize an empty DataFrame to store mismatches
    mismatches = pd.DataFrame()

    # Group by 'ConsID' and examine the uniqueness of 'ConsCode' within each group
    grouped = combined_df.groupby('ConsID')
    for cons_id, group in grouped:
        if group['ConsCode'].nunique() > 1:  # More than one unique 'ConsCode' for this 'ConsID'
            mismatches = pd.concat([mismatches, group], ignore_index=True)

    # Sort the mismatches DataFrame by 'ConsID' and then by 'ConsCode'
    mismatches.sort_values(by=['ConsID', 'ConsCode'], inplace=True)

    return mismatches  # Return the DataFrame containing mismatches


def find_deceased(dataframes):
    # Concatenate all provided DataFrames into a single DataFrame
    combined_df = pd.concat(dataframes, ignore_index=True)

    # Filter for deceased records for any combinations 
    return combined_df[(combined_df['Deceased'] == 'Yes') | (combined_df['SRDeceased'] == 'Yes')]

def find_inactive(dataframes):
    # Concatenate all provided DataFrames into a single DataFrame
    combined_df = pd.concat(dataframes, ignore_index=True)

    # Filter for inactive records for any combinations 
    return combined_df[(combined_df['IsInactive'] == 'Yes') | (combined_df['Inactive'] == 'Yes') | (combined_df['SRInactive'] == 'Yes')]

def find_name_is_correct(dataframes):
    # Concatenate all provided DataFrames into a single DataFrame
    combined_df = pd.concat(dataframes, ignore_index=True)

    # Filter for records where 'NameIsCorrect' is 'Yes'
    name_is_correct_records = combined_df[combined_df['NameIsCorrect'] == 'Yes']

    return name_is_correct_records

def analyze_spouse_consistency(dataframe):
    # Initialize an empty DataFrame to store potential mismatches
    inconsistencies = pd.DataFrame()

    # Group by 'ConsID' and examine the uniqueness of 'ConsCode' within each group
    for cons_id, group in dataframe.groupby('ConsID'):
        # Get the unique sets of spouse details for the 'ConsID'
        unique_spouses = group.drop_duplicates(subset=['LastName', 'FirstName', 'SRLastName', 'SRFirstName'])
        # If there is more than one unique set of details, this indicates an inconsistency
        if len(unique_spouses) > 1:
            inconsistencies = pd.concat([inconsistencies, unique_spouses], ignore_index=True)

    return inconsistencies

def process_csv_files():
    # Get the directory where the script is located
    folder_path = os.path.dirname(os.path.realpath(__file__))

    # Read all CSV files in the directory
    dfs = read_csv_files(folder_path)

    # Get paths of all CSV files in the directory for separate_rows_with_asterisk function
    file_paths = glob.glob(os.path.join(folder_path, '*.csv'))

    # Separate rows based on 'ConsID'
    remaining_dfs, asterisk_dfs = separate_rows_with_asterisk(dfs, file_paths)
    # Find mismatches across 'ConsID' and 'ConsCode'
    mismatches = find_mismatched_consids(remaining_dfs + asterisk_dfs)
    # Find records where 'NameIsCorrect' is 'Yes'
    name_is_correct_df = find_name_is_correct(dfs)
    # Pass through untouched dataframe dfs to get inactive and deceased
    df_inactive = find_inactive(dfs)
    df_deceased = find_deceased(dfs)

    # Save the separated DataFrames to Excel files after passing them through to get proper formatting 
    save_dataframes_to_excel(dfs, os.path.join(folder_path, 'Combined_NoEdits.xlsx'))
    save_dataframes_to_excel(remaining_dfs, os.path.join(folder_path, 'Combined_NoAsterisk.xlsx'))
    save_dataframes_to_excel(asterisk_dfs, os.path.join(folder_path, 'Combined_Asterisk.xlsx'))
    save_dataframes_to_excel([df_deceased], os.path.join(folder_path, 'Combined_Deceased.xlsx'))
    save_dataframes_to_excel([df_inactive], os.path.join(folder_path, 'Combined_Inactive.xlsx'))
    save_dataframes_to_excel([mismatches], os.path.join(folder_path, 'Combined_Mismatches.xlsx'))
    save_dataframes_to_excel([name_is_correct_df], os.path.join(folder_path, 'NameIsCorrect.xlsx'))

    return "Processing complete."

# Call function to run the script
process_csv_files()

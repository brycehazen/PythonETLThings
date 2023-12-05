import os
import pandas as pd

def combine_csvs(directory):
    all_dataframes = []
    
    for filename in os.listdir(directory):
        if filename.endswith(".csv") and "Realm" not in filename:
            # Reading CSV with specified encoding and low_memory option
            df = pd.read_csv(os.path.join(directory, filename), encoding='ISO-8859-1', low_memory=False)
            all_dataframes.append(df)
    
    if all_dataframes:
        combined_df = pd.concat(all_dataframes, ignore_index=True)
        # Saving the combined CSV with specified encoding
        combined_df.to_csv(os.path.join(directory, "combined_csv.csv"), index=False, encoding='ISO-8859-1')
        return "CSV files combined successfully, excluding files with 'Realm' in the name."
    else:
        return "No CSV files found or all files contain 'Realm' in the name."

# Example usage
combine_csvs_result = combine_csvs('.')

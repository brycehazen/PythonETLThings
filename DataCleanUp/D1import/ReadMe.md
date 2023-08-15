# CSV Data Cleaner Script

This script processes CSV files in its directory to clean and enhance data. Specifically, it cleans phone number placeholders, splits first names that contain initials or middle names, and guesses the gender based on the first name.

## Features

1. **Phone Number Cleaning**: Removes placeholders like "(   )    -" when no actual phone number is present.
2. **Name Splitting**: If the 'first' column contains entries like "John D" or "John David", it splits them and places "D" or "David" in the 'middle' column.
3. **Gender Guessing**: Adds a 'gender' column and uses the `gender-guesser` library to guess the gender based on the first name.

## Usage

1. Ensure you have Python installed.
2. Install required libraries:
   ```bash
   pip install pandas gender-guesser
3. Place the script in the directory containing the CSV files you wish to process.
4. Run the script:
   ```bash
   python D1NewAdds.py
6. 5. Processed files will be saved in the same directory with "_clean" appended to their names.

## Outputs

- Phone numbers cleaned of placeholders.
- Split first names with middle names or initials moved to the 'middle' column.
- Gender column added, with values guessed based on first names. Possible values include "Male", "Female", "Unknown", and "Ambiguous".




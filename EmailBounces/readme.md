# Email Data Extractor and Processor

Extracts email addresses and names from a given HTML (`Blackbaud.html`), and then merges this data with information from `EmailBounces.csv` to produce a processed CSV file (`BouncedEmailsImport.csv`).

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Script Details](#script-details)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. **Dependencies:** 
    - Python 3.x
    - pandas: `pip install pandas`
    - BeautifulSoup4: `pip install beautifulsoup4`

2. **Setup:** 
    - Clone the repository or download the script.
    - Ensure `Blackbaud.html` and `EmailBounces.csv` are in the same directory as the script.
## Usage

1. Navigate to the script's directory.
2. Run the script:
   \```shell
   python EmailScape.py
   \```
3. Check the output in `BouncedEmailsImport.csv`.

## Script Details

The script operates in the following manner:

1. Reads the HTML content from `Blackbaud.html`.
2. Parses the HTML to extract email addresses and names.
3. Reads data from `EmailBounces.csv`.
4. Merges the extracted email addresses with the bounce data.
5. Outputs the processed data to `BouncedEmailsImport.csv`.

## Contributing

If you find any bugs or wish to propose improvements, feel free to create an issue or a pull request.

## License

This script is available under the MIT License. See `LICENSE` for more information.

# 5-Year Appeal Gifts Visualization

This script takes data from an Excel file titled "5-Year Appeal Gifts by Source.xlsx" and creates visualizations for the given gifts and donors data. The results are saved in a new Excel file with each type of visualization on a different tab.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Visualizations Generated](#visualizations-generated)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Prerequisites
- Python 3.10
- Pandas library
- Matplotlib library
- openpyxl library

To install the necessary libraries, run:
```bash
pip install pandas matplotlib openpyxl
```
---

## Usage
1. Ensure that the Excel file "5-Year Appeal Gifts by Source.xlsx" is in the same directory as the script.
2. Run the script:
```bash
python script_name.py
```
---
3. Once executed, you'll get a new Excel file titled `visualizations.xlsx` in the same directory.

## Visualizations Generated - A1 is empty
- Line Plot for $'s Pledged
- Bar Chart for # Donors
- Stacked Bar Chart for $'s Pledged
- Pie Chart for 2023 $'s Pledged
- Line Plot for # Donors
- Pie Chart for 2023 # Donors
- Columns
```
    ["2023 $'s Pledged",
    "2023 # Donors",
    "2022 $'s Pledged",
    "2022 # Donors",
    "2021 $'s Pledged",
    "2021 # Donors",
    "2020 $'s Pledged",
    "2020 # Donors",
    "2019 $'s Pledged",
    "2019 # Donors"]
```
---
- Rows
```
    ["Pre Appeal Mailing",
    "Non-Donor Letter",
    "In-Pew",
    "Online",
    "Follow-up",
    "Stocks",
    "Credit Card"]
```
---

## Troubleshooting
If you run into any issues:
1. Ensure that the Excel file is correctly formatted and named.
2. Ensure that all required libraries are installed.
3. Ensure that there are no non-numeric characters in the columns that are being plotted.

## License
This project is licensed under the MIT License.


# ParishSync

## Overview

Taking data after it has been run through [ReTestCases](https://github.com/brycehazen/PythonETLThings/tree/main/ReTestCases) and then imported in RE. After improting, you will get an exception file as well as a New Import Control-Summary Report that needs to be saved
as a .csv. These two files will be needed for this process to work. 

## Features

- **Tracking Exceptions**: 
  - After importing records, RE creates a New Import Control-Summary Report - This saved as a csv will be combined with `redata.csv` to output `redataWithExceptions.csv`
  - This will have have the data from redata.csv combined with the reason it was not imported. This will make it easier to know what needs to be corrected as well as track what and why records were not Imported
- **Removing Phone Numbers**: 
  - `removePhones.py` will look at `redata.csv` and compare `PhoneConsID.csv`, this `PhoneConsID.csv` is a collection pulled from SQL of all Phones in RE. If the Phone is already in RE and found in `redata.csv`. Once removed it will output updated_redata.csv.
  - If a record and Phone is not found in `PhoneConsID.csv`, but it caused an exception and was put into `redataWithExceptions.csv`, the script will add it to `PhoneConsID.csv`. This will result in the record not causing an exception in the future.
- **Not Yet added**:
  - Soon I will add an additional part of the script to update constituency codes. This will invlove taking the query created from importing, exporting it back out with all the records ConsCode. Then comparing this ConsCode export to `redata.csv`
# Scripts Overview

This repository contains two Python scripts for data manipulation:

1. `CombineExceptions.py`: Combines exceptions from "New Import Control-Summary Report.csv" and appends them to "updated_redata.csv".
2. `removePhones.py`: Filters and removes phone-related entries from "redata.csv" based on the data in "PhoneConsID.csv".

---

## CombineExceptions.py

### Description:
This script reads data from "New Import Control-Summary Report.csv" and "updated_redata.csv", and then combines specific exceptions from the summary report with the redata file. The combined data is saved to "redataWithExceptions.csv".

### Usage:
```bash
python CombineExceptions.py
```
**Note:** Ensure both "New Import Control-Summary Report.csv" and "updated_redata.csv" are present in the working directory before executing the script.

---

## removePhones.py

### Description:
This script checks for "redataWithExceptions.csv" and, if found, extracts specific phone-related errors to append them to "PhoneConsID.csv". It then reads "redata.csv" and removes phone entries that match those in "PhoneConsID.csv". The updated data is saved to "updated_redata.csv".

### Usage:
```bash
python CombineExceptions.py
```
**Note:** Ensure "redata.csv", "PhoneConsID.csv", and optionally "redataWithExceptions.csv" are present in the working directory before executing the script.

---

## Dependencies

Both scripts require the `pandas` library. Ensure it's installed before executing the scripts.

```bash
pip install pandas
```

---

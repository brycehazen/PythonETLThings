
# ParishSync

## Overview

Taking data after it has been run through [ReTestCases](https://github.com/brycehazen/PythonETLThings/tree/main/ReTestCases). After runing RETestCases, you will get RE_data.csv, this file as well as a PhoneConsID.csv, are need to start this procesS. 

## Features
- **Removing Phone Numbers**: 
  - `removePhones.py` will look at `RE_data.csv` and compare `PhoneConsID.csv`, this `PhoneConsID.csv` is a collection pulled from SQL of all Phones in RE. If the Phone is already in RE and found in `redata.csv`. Once removed it will output updated_redata.csv.
  - If a record and Phone is not found in `PhoneConsID.csv`, but it caused an exception and was put into `RE_DataWithExceptions.csv`, the script will add it to `PhoneConsID.csv`. This will result in the record not causing an exception in the future.
- **Tracking Exceptions**: 
  - After importing records, RE creates a New Import Control-Summary Report - This saved as a csv will be combined with `RE_Data.csv` to output `RE_DataWithExceptions.csv`
  - This will have have the data from redata.csv combined with the reason it was not imported. This will make it easier to know what needs to be corrected as well as track what and why records were not Imported
- **Not Yet added**:
  - Soon I will add an additional part of the script to update constituency codes. This will invlove taking the query created from importing, exporting it back out with all the records ConsCode. Then comparing this ConsCode export to `RE_data.csv`

# Scripts Overview
This repository contains two Python scripts for data manipulation. It is split in to parts.  :
1. `removePhones.py`: BEFORE importing into Raiser's Edge, this filters and removes phone-related entries from "RE_Data.csv"(comes from running [ReTestCases](https://github.com/brycehazen/PythonETLThings/tree/main/ReTestCases)) based on the data in `PhoneConsID.csv` 
2. `CombineExceptions.py`: AFTER improting into Raiser's Edge, "New Import Control-Summary Report is created and needs to be saved as a csv `New Import Control-Summary Report.csv` this then appends them to `updated_RE_Data.csv` outputing `RE_DataWithExceptions.csv`.

---

## removePhones.py

### Description:
1. This script checks for `updated_RE_DataWithExceptions.csv` and, if found, extracts specific phone-related errors to append them to `PhoneConsID.csv`.
2. It then reads `RE_Data.csv` and removes phone entries that match those in `PhoneConsID.csv`.
3. The updated data is saved to `updated_RE_Data.csv`.
4. This script should be ran one more time after running `CombineExceptions.py` since this produces `updated_RE_DataWithExceptions.csv`

### Usage:
```bash
python CombineExceptions.py
```
**Note:** Ensure `RE_Data.csv`, `PhoneConsID.csv`, and optionally `updated_RE_DataWithExceptions.csv`are present in the working directory before executing the script.

---

## CombineExceptions.py

### Description:
1. This script reads data from `New Import Control-Summary Report.csv` and `updated_RE_Data.csv`
2. Then combines specific exceptions from `New Import Control-Summary Report.csv` with  `updated_RE_Data.csv`. The combined data is saved to `updated_RE_DataWithExceptions.csv`.

### Usage:
```bash
python CombineExceptions.py
```
**Note:** Ensure both `New Import Control-Summary Report.csv` and `updated_redata.csv` are present in the working directory before executing the script. You should already ran `removePhones.py` and finihsed importing to Raiser's Edge before this is ran

---



## Dependencies

Both scripts require the `pandas` library. Ensure it's installed before executing the scripts.

```bash
pip install pandas
```

---

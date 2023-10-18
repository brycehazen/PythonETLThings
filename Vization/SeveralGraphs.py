import pandas as pd
import matplotlib.pyplot as plt
import io

# Read the data
df = pd.read_excel("5-Year Appeal Gifts by Source.xlsx", header=0, index_col="Gift Source")

with pd.ExcelWriter('visualizations.xlsx') as writer:

    # 1. Line Plot for $'s Pledged
    plt.figure(figsize=(12, 6))
    pledge_columns = [col for col in df.columns if "$'s Pledged" in str(col) and not df[col].isna().all()]
    for column in pledge_columns:
        plt.plot(df.index, df[column], marker='o', label=column)
    plt.title("5-Year Appeal Gifts by Source ($'s Pledged)")
    plt.xlabel("Source")
    plt.ylabel("Amount")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    worksheet = writer.book.add_worksheet('Line Plot Pledged')
    worksheet.insert_image('A1', '', {'image_data': buf})

    # 2. Bar Chart for # Donors
    donor_columns = [col for col in df.columns if "# Donors" in str(col) and not df[col].isna().all()]
    if not df[donor_columns].empty:
        df[donor_columns].plot(kind="bar", figsize=(12, 6))
        plt.title("5-Year Appeal by Number of Donors")
        plt.ylabel("Number of Donors")
        plt.xlabel("Source")
        plt.xticks(rotation=45)
        plt.grid(axis="y")
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()
        worksheet = writer.book.add_worksheet('Bar Chart Donors')
        worksheet.insert_image('A1', '', {'image_data': buf})

    # 3. Stacked Bar Chart for $'s Pledged
    if not df[pledge_columns].empty:
        df[pledge_columns].plot(kind="bar", stacked=True, figsize=(12, 6))
        plt.title("5-Year Appeal Gifts by Source (Stacked $'s Pledged)")
        plt.ylabel("Amount")
        plt.xlabel("Source")
        plt.xticks(rotation=45)
        plt.grid(axis="y")
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()
        worksheet = writer.book.add_worksheet('Stacked Bar Pledged')
        worksheet.insert_image('A1', '', {'image_data': buf})

    # 4. Pie Chart for 2023 $'s Pledged
    if "2023 $'s Pledged" in df.columns and not df["2023 $'s Pledged"].empty:
        df["2023 $'s Pledged"].plot(kind="pie", autopct='%1.1f%%', startangle=90, figsize=(10, 7))
        plt.title("Appeal Gifts by Source for the year 2023 ($'s Pledged)")
        plt.ylabel("")
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()
        worksheet = writer.book.add_worksheet('Pie Chart 2023 Pledged')
        worksheet.insert_image('A1', '', {'image_data': buf})
        
    # 5. Line Plot for # Donors
    plt.figure(figsize=(12, 6))
    for column in donor_columns:
        plt.plot(df.index, df[column], marker='o', label=column)
    plt.title("5-Year Appeal by Number of Donors")
    plt.xlabel("Source")
    plt.ylabel("Number of Donors")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    worksheet = writer.book.add_worksheet('Line Plot Donors')
    worksheet.insert_image('A1', '', {'image_data': buf})

    # 6. Pie Chart for 2023 # Donors
    if "2023 # Donors" in df.columns and not df["2023 # Donors"].empty:
        df["2023 # Donors"].plot(kind="pie", autopct='%1.1f%%', startangle=90, figsize=(10, 7))
        plt.title("Number of Donors by Source for the year 2023")
        plt.ylabel("")
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()
        worksheet = writer.book.add_worksheet('Pie Chart 2023 Donors')
        worksheet.insert_image('A1', '', {'image_data': buf})

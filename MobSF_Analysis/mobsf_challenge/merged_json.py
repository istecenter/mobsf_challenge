import os
import json
import pandas as pd

EXCEL_FILE = r"C:\Users\moham\OneDrive\Documents\OneDrive\Desktop\apps.xlsx"
JSON_FOLDER = r"C:\Users\moham\OneDrive\Documents\OneDrive\Desktop\results"
OUTPUT_FOLDER = r"C:\Users\moham\OneDrive\Documents\OneDrive\Desktop\merged_json2"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

df = pd.read_excel(EXCEL_FILE)

for root, dirs, files in os.walk(JSON_FOLDER):

    relative_path = os.path.relpath(root, JSON_FOLDER)
    output_dir = os.path.join(OUTPUT_FOLDER, relative_path)
    os.makedirs(output_dir, exist_ok=True)

    for file in files:

        if not file.lower().endswith(".json"):
            continue

        json_path = os.path.join(root, file)

        excel_row = df[df["File Name"].str.replace(".apk", ".json", regex=False) == file]

        if excel_row.empty:
            print(f"{file} not found in Excel")
            continue

        row = excel_row.iloc[0]

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        data["application_info"] = {
            "app_name": row["App Name"],
            "package_name": row["Package Name"],
            "version_name": row["Version Name"],
            "version_code": int(row["Version Code"]),
            "source": row["Source"],
            "file_name": row["File Name"]
        }

        output_path = os.path.join(output_dir, file)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"Merged: {output_path}")

print("Finished.")
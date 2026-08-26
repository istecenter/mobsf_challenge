import os
from androguard.core.apk import APK
from openpyxl import Workbook

APK_FOLDER = r"C:\Users\moham\OneDrive\Documents\OneDrive\Desktop\apks"

OUTPUT_FILE = r"C:\Users\moham\OneDrive\Documents\OneDrive\Desktop\apps.xlsx"

wb = Workbook()
ws = wb.active
ws.title = "APK Information"

ws.append([
    "App Name",
    "Package Name",
    "Version Name",
    "Version Code",
    "Source",
    "Folder",
    "File Name"
])

for root, dirs, files in os.walk(APK_FOLDER):

    for file in files:

        if file.lower().endswith(".apk"):

            apk_path = os.path.join(root, file)

            try:
                apk = APK(apk_path)

                app_name = apk.get_app_name()
                package = apk.get_package()
                version_name = apk.get_androidversion_name()
                version_code = apk.get_androidversion_code()

                source = os.path.basename(root)

                ws.append([
                    app_name,
                    package,
                    version_name,
                    version_code,
                    source,
                    root,
                    file
                ])

                print(f"[✓] {apk_path}")

            except Exception as e:
                print(f"[✗] {apk_path} -> {e}")

wb.save(OUTPUT_FILE)

print(f"\nFinished! File saved as {OUTPUT_FILE}")
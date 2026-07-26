"""
MobSF Batch APK Scanner
"""

import os
import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

SERVER = "http://127.0.0.1:8000"
APIKEY = "facb8978461a35c828f7195ca5a110beed24a067c0f4a64f2d8f9a96bfdf3ec7"

APK_FOLDER = r"C:\Users\moham\OneDrive\Documents\OneDrive\Desktop\apks\Sosyal Medya"
OUTPUT_FOLDER = r"C:\Users\moham\OneDrive\Documents\OneDrive\Desktop\results\Sosyal Medya_Result"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def upload(file_path):
    """Upload APK"""

    print(f"[+] Uploading {os.path.basename(file_path)}")

    multipart_data = MultipartEncoder(
        fields={
            "file": (
                os.path.basename(file_path),
                open(file_path, "rb"),
                "application/octet-stream",
            )
        }
    )

    headers = {
        "Content-Type": multipart_data.content_type,
        "Authorization": APIKEY,
    }

    response = requests.post(
        SERVER + "/api/v1/upload",
        data=multipart_data,
        headers=headers,
    )

    response.raise_for_status()
    return response.json()


def scan(upload_result):
    """Start Scan"""

    print(f"[+] Scanning {upload_result['file_name']}")

    headers = {
        "Authorization": APIKEY,
    }

    response = requests.post(
        SERVER + "/api/v1/scan",
        data=upload_result,
        headers=headers,
    )

    response.raise_for_status()
    return response.json()


def get_json(upload_result):
    """Download JSON Report"""

    print(f"[+] Getting JSON Report")

    headers = {
        "Authorization": APIKEY,
    }

    data = {
        "hash": upload_result["hash"]
    }

    response = requests.post(
        SERVER + "/api/v1/report_json",
        data=data,
        headers=headers,
    )

    response.raise_for_status()
    return response.json()


def save_json(report, apk_name):
    """Save JSON"""

    filename = os.path.splitext(apk_name)[0] + ".json"

    output_file = os.path.join(
        OUTPUT_FOLDER,
        filename
    )

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)

    print(f"[✓] Saved {filename}")


def process_apk(file_path):

    try:

        upload_result = upload(file_path)

        scan(upload_result)

        report = get_json(upload_result)

        save_json(
            report,
            os.path.basename(file_path)
        )

    except Exception as e:

        print(f"[!] Error processing {file_path}")
        print(e)


def main():

    apk_files = [
        f for f in os.listdir(APK_FOLDER)
        if f.lower().endswith(".apk")
    ]

    print(f"Found {len(apk_files)} APK files\n")

    for apk in apk_files:

        process_apk(
            os.path.join(APK_FOLDER, apk)
        )

    print("\nFinished.")


if __name__ == "__main__":
    main()
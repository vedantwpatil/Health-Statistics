from xml.etree import ElementTree
import csv
import os


def extract_apple_watch_hr(xml_path="export.xml"):
    """Extracts heart rate data specifically from Apple Watch"""
    try:
        if not os.path.exists(xml_path):
            raise FileNotFoundError(
                f"XML file not found at: {os.path.abspath(xml_path)}"
            )

        tree = ElementTree.parse(xml_path)
        root = tree.getroot()

        with open("apple_watch_hr.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Timestamp", "BPM", "Device", "Unit"])

            record_count = 0
            for record in root.findall(".//Record"):
                if (
                    record.get("type") == "HKQuantityTypeIdentifierHeartRate"
                    and record.get("sourceName") == "Apple Watch"
                ):
                    writer.writerow(
                        [
                            record.get("startDate"),
                            record.get("value"),
                            record.get("sourceName"),
                            record.get("unit"),
                        ]
                    )
                    record_count += 1

            print(f"Exported {record_count} heart rate records to apple_watch_hr.csv")

    except Exception as e:
        print(f"Error: {str(e)}")
        print("Ensure you've:")
        print("- Exported XML from Health app (Settings > Health > Export)")
        print("- Placed export.xml in the same directory as this script")
        print("- Unzipped the Health export folder")


file_path = "../../data/apple_health_export/export.xml"
extract_apple_watch_hr(file_path)

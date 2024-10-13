import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

# Parse the XML file
tree = ET.parse("apple_health_export/export.xml")  # Changed the file path
root = tree.getroot()

# Extract records into a list of dictionaries
records = [
    elem.attrib
    for elem in root.iter("Record")
    if elem.attrib.get("type") == "HKQuantityTypeIdentifierHeartRate"
]

# Convert to DataFrame
df = pd.DataFrame(records)

# Convert date columns to datetime
date_columns = ["startDate", "endDate", "creationDate"]
for col in date_columns:
    df[col] = pd.to_datetime(df[col])

# Convert value column to numeric
df["value"] = pd.to_numeric(df["value"], errors="coerce")

# Filter for last month's data
one_month_ago = datetime.now() - timedelta(days=30)
last_month_data = df[df["startDate"] >= one_month_ago]

# Create the plot
plt.figure(figsize=(12, 6))
plt.scatter(
    last_month_data["startDate"],
    last_month_data["value"],
    alpha=0.5,
    label="Heart Rate",
)

# Add a trend line
z = np.polyfit(
    last_month_data["startDate"].astype(int) / 10**9, last_month_data["value"], 1
)
p = np.poly1d(z)
plt.plot(
    last_month_data["startDate"],
    p(last_month_data["startDate"].astype(int) / 10**9),
    "r--",
    label="Trend",
)

plt.title("Heart Rate Over Time (Last Month)")
plt.xlabel("Date")
plt.ylabel("Heart Rate (bpm)")
plt.xticks(rotation=45)
plt.legend()

plt.tight_layout()
plt.show()

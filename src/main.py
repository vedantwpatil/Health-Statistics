import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import re

# Parse XML file
print("Parsing XML file...")
tree = ET.parse("apple_health_export/export.xml")
root = tree.getroot()

# Extract workout data
workout_list = [x.attrib for x in root.iter("Workout")]
workout_data = pd.DataFrame(workout_list)

# Extract heart rate data
record_list = [x.attrib for x in root.iter("Record")]
record_data = pd.DataFrame(record_list)
heartrate_data = record_data[record_data["type"] == "HeartRate"]


# Function to convert duration string to timedelta
def parse_duration(duration_str):
    match = re.match(r"PT(\d+H)?(\d+M)?(\d+S)?", duration_str)
    if not match:
        return pd.Timedelta(0)
    hours = int(match.group(1)[:-1]) if match.group(1) else 0
    minutes = int(match.group(2)[:-1]) if match.group(2) else 0
    seconds = int(match.group(3)[:-1]) if match.group(3) else 0
    return pd.Timedelta(hours=hours, minutes=minutes, seconds=seconds)


# Clean and prepare data
workout_data["startDate"] = pd.to_datetime(workout_data["startDate"])
workout_data["endDate"] = pd.to_datetime(workout_data["endDate"])
workout_data["duration"] = workout_data["duration"].apply(parse_duration)
workout_data["durationInMinutes"] = workout_data["duration"].dt.total_seconds() / 60
workout_data["totalEnergyBurned"] = pd.to_numeric(workout_data["totalEnergyBurned"])

heartrate_data["startDate"] = pd.to_datetime(heartrate_data["startDate"])
heartrate_data["value"] = pd.to_numeric(heartrate_data["value"])

# Analyze workout data
print("\nWorkout Analysis:")
print(f"Total workouts: {len(workout_data)}")
print(
    f"Average workout duration: {workout_data['durationInMinutes'].mean():.2f} minutes"
)
print(f"Total calories burned: {workout_data['totalEnergyBurned'].sum():.2f} kcal")

# Visualize workout types
workout_types = workout_data["workoutActivityType"].value_counts()
plt.figure(figsize=(10, 6))
workout_types.plot(kind="pie", autopct="%1.1f%%")
plt.title("Workout Types Distribution")
plt.axis("equal")
plt.savefig("workout_types.png")
plt.close()


# Analyze heart rate data
def calculate_hrv(hr_data):
    # Simplified HRV calculation using RMSSD method
    diff = hr_data["value"].diff()
    return (diff**2).mean() ** 0.5


# Calculate daily HRV
daily_hrv = heartrate_data.groupby(heartrate_data["startDate"]).apply(calculate_hrv)

# Visualize HRV trend
plt.figure(figsize=(12, 6))
daily_hrv.plot()
plt.title("Daily Heart Rate Variability (HRV) Trend")
plt.xlabel("Date")
plt.ylabel("HRV (RMSSD)")
plt.savefig("hrv_trend.png")
plt.close()


# Calculate recovery score (simplified version)
def calculate_recovery_score(hrv):
    return min(100, max(0, hrv / 2))


recovery_scores = daily_hrv.apply(calculate_recovery_score)

print("\nRecovery Analysis:")
print(f"Average Recovery Score: {recovery_scores.mean():.2f}")
print(f"Latest Recovery Score: {recovery_scores.iloc[-1]:.2f}")


# Analyze workout intensity
def calculate_strain(workout):
    workout_hr = heartrate_data[
        (heartrate_data["startDate"] >= workout["startDate"])
        & (heartrate_data["startDate"] <= workout["endDate"])
    ]
    if len(workout_hr) == 0:
        return 0
    avg_hr = workout_hr["value"].mean()
    duration_hours = workout["duration"].total_seconds() / 3600
    # This is a simplified strain calculation
    return (avg_hr * duration_hours) / 10


workout_data["strain"] = workout_data.apply(calculate_strain, axis=1)

print("\nWorkout Intensity Analysis:")
print(f"Average Workout Strain: {workout_data['strain'].mean():.2f}")
print(
    f"Highest Strain Workout: {workout_data.loc[workout_data['strain'].idxmax(), 'workoutActivityType']} (Strain: {workout_data['strain'].max():.2f})"
)

# Visualize strain over time
plt.figure(figsize=(12, 6))
workout_data.plot(x="startDate", y="strain", kind="scatter")
plt.title("Workout Strain Over Time")
plt.xlabel("Date")
plt.ylabel("Strain")
plt.savefig("strain_over_time.png")
plt.close()

print("\nAnalysis complete. Check the generated PNG files for visualizations.")

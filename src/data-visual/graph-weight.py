import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

file_path = "/Users/vedantpatil/Library/CloudStorage/OneDrive-DrexelUniversity/Documents/cs/personal/python-coding/fitness-tracker/data/weight_tracker.xlsx"
df = pd.read_excel(file_path)

# Convert the date column to datetime if it's not already
df["Date"] = pd.to_datetime(df["Date"])

# Sort the dataframe by date
df = df.sort_values("Date")

# Create the plot
plt.figure(figsize=(12, 6))
plt.plot(df["Date"], df["Weight"], marker="o")

# Customize the plot
plt.title("Weight Over Time")
plt.xlabel("Date")
plt.ylabel("Weight")

# Get the current axis
ax = plt.gca()

# Set the date formatter
date_formatter = mdates.DateFormatter("%Y-%m-%d")
ax.xaxis.set_major_formatter(date_formatter)

# Rotate and align the tick labels so they look better
plt.gcf().autofmt_xdate()

# Add grid lines
plt.grid(True, linestyle="--", alpha=0.7)

# Show the plot
plt.tight_layout()
plt.show()

# Optionally, save the plot as an image file
plt.savefig("weight_over_time.png")

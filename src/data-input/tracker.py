from datetime import date
from datetime import datetime
import openpyxl

try:
    file_path = "/Users/vedantpatil/Library/CloudStorage/OneDrive-DrexelUniversity/Documents/cs/personal/python-coding/fitness-tracker/data/weight_tracker.xlsx"

    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    today = date.today()
    time = datetime.now().time()
    weight = input("Enter today's weight to be logged: ")

    try:
        weight = float(weight)
    except ValueError:
        print("Invalid input. Please enter a numeric value for weight.")
        exit(1)

    new_data = [today, time, weight]

    sheet.append(new_data)

    workbook.save(file_path)
    print("Weight logged successfully.")

except FileNotFoundError:
    print("Error: Excel file not found. Please check the file path.")
except PermissionError:
    print(
        "Error: Unable to access the Excel file. It might be open in another program."
    )
except Exception as e:
    print(f"An unexpected error occurred: {e}")

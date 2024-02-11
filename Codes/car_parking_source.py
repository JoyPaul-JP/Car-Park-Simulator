import csv
import os
import datetime
import random
import itertools

# Constants
PARKING_CAPACITY = 8
HOURLY_RATE = 2
CSV_FILE = "car_parking_records.csv"
CSV_COLUMNS = [
    "Serial Number",
    "Ticket Number",
    "Vehicle Registration Number",
    "Parking Space ID",
    "Entry Time",
    "Exit Time",
    "Total Parking Fee",
]

# Initializing parking records
parking_records = []
serial_number_generator = itertools.count(1)  # Initializing a serial number generator

# Checking if the CSV file exists and loading records if available
if os.path.exists(CSV_FILE):
    with open(CSV_FILE, "r") as file:
        reader = csv.DictReader(file)
        parking_records = list(reader)

def read_records_from_csv():
    """
    Reading parking records from the CSV file and updating the global variable parking_records.
    """
    global parking_records
    with open(CSV_FILE, 'r') as file:
        reader = csv.DictReader(file)
        parking_records = list(reader)

def save_records_to_csv():
    """
    Saving parking records to the CSV file.
    """
    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for record in parking_records:
            # Add serial number to each record
            record["Serial Number"] = next(serial_number_generator)
            writer.writerow(record)

def calculate_parking_fee(entry_time):
    """
    Calculating parking fee based on the parking duration.
    """
    now = datetime.datetime.now()
    entry_time = datetime.datetime.strptime(entry_time, '%d/%m/%Y (%A) %H:%M:%S')  # Parsing the entry_time as a datetime object
    parking_duration = (now - entry_time).total_seconds() / 3600  # in hours
    parking_fee = round(parking_duration * HOURLY_RATE, 2)  # Calculating and rounding to two decimal places
    return parking_fee

def generate_ticket_number(reg_number):
    """
    Generating a unique ticket number based on the vehicle registration number and current time.
    """
    now = datetime.datetime.now()
    formatted_date = now.strftime("%d%m%y")
    formatted_time = now.strftime("%H%M%S")
    return formatted_date + reg_number.upper() + formatted_time  # Converting to uppercase

def is_vehicle_already_parked(reg_number):
    """
    Checking if a vehicle with the given registration number is already parked.
    """
    reg_number = reg_number.upper()  # Converting to uppercase
    for record in parking_records:
        if record["Vehicle Registration Number"].upper() == reg_number and record["Exit Time"] == "Parking.....":
            return True
    return False

def get_current_time():
    """
    Getting the current time in a formatted string.
    """
    now = datetime.datetime.now()
    return now.strftime("%d/%m/%Y (%A) %H:%M:%S")

def display_available_spaces():
    """
    Displaying the number of available parking spaces.
    """
    occupied_spaces = len([record for record in parking_records if record["Exit Time"] == "Parking....."])
    available_spaces = PARKING_CAPACITY - occupied_spaces
    return available_spaces

def add_serial_number():
    """
    Assigning serial numbers to records if not already assigned.
    """
    # Checking if there are existing serial numbers in the records
    existing_serial_numbers = set(record.get("Serial Number", None) for record in parking_records)

    for i, record in enumerate(parking_records):
        if "Serial Number" not in record or record["Serial Number"] is None:
            # Assigning a new serial number starting from 1 if it doesn't exist
            new_serial_number = 1
            while new_serial_number in existing_serial_numbers:
                new_serial_number += 1

            # Assigning the new serial number to the record
            record["Serial Number"] = new_serial_number
            existing_serial_numbers.add(new_serial_number)

if __name__ == "__main__":
    pass

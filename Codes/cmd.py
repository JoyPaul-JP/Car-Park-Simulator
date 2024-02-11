from car_parking_source import *

while True:
    # Displaying menu options
    print("\nMenu:")
    print("1. Enter The Car Park (Hourly Rate: £2)")
    print("2. Exit The Car Park")
    print("3. View Available Parking Spaces")
    print("4. Query Parking Record by Ticket Number")
    print("5. Quit")

    # Getting user choice
    choice = input("Enter your choice (1/2/3/4/5): ")

    if choice == "1":
        # Option to enter the car park
        while True:
            if display_available_spaces() == 0:
                print("\nSorry, the car park is full. No free space is available.")
                break  # Returning to the main menu
            else:
                # Getting vehicle registration number
                reg_number = input("\nEnter vehicle Registration Number (or type '0' to return to the Main Menu): ")
                reg_number = ''.join(char for char in reg_number if char.isalnum())
                if reg_number == "0":
                    break  # Returning to the main menu
                if not reg_number:
                    print("\nPlease enter a valid vehicle Registration Number.")
                elif is_vehicle_already_parked(reg_number):
                    print(f'\nThe vehicle holding Registration Number: "{reg_number.upper()}" is parked already.')
                else:
                    available_parking_space_ids = list(range(1, 9))
                    taken_parking_space_ids = set()

                    # Filtering out parking space IDs that are already assigned and have no exit time
                    for record in parking_records:
                        if record["Exit Time"] == "Parking.....":
                            taken_parking_space_ids.add(int(record["Parking Space ID"]))

                    available_parking_space_ids = [space_id for space_id in available_parking_space_ids if
                                                   space_id not in taken_parking_space_ids]

                    if available_parking_space_ids:
                        # Assigning a ticket number and parking space ID
                        ticket_number = generate_ticket_number(reg_number)
                        parking_space_id = random.choice(available_parking_space_ids)
                        entry_time = get_current_time()
                        # Adding parking record to the list
                        parking_records.append({
                            "Serial Number": len(parking_records) + 1,
                            "Ticket Number": ticket_number,
                            "Vehicle Registration Number": reg_number.upper(),  # Converting to uppercase
                            "Parking Space ID": parking_space_id,
                            "Entry Time": entry_time,
                            "Exit Time": "Parking.....",
                            "Total Parking Fee": "Parking....."
                        })
                        # Displaying information to the user
                        print("\nTicket Number:", ticket_number)
                        print("Vehicle Registration Number:", reg_number.upper())
                        print("Parking Space ID:", parking_space_id)
                        print("Entry Time:", entry_time)
                        print("Exit Time: Parking.....")
                        print("Total Parking Fee: Parking.....")
                        print("\nRemaining Parking Spaces:", display_available_spaces(), "\n")
                        save_records_to_csv()
                        break  # Returning to the main menu

    elif choice == "2":
        # Option to exit the car park
        reg_number = input("\nEnter vehicle Registration Number (or type '0' to return to the Main Menu): ")
        reg_number = ''.join(char for char in reg_number if char.isalnum())
        if reg_number == "0":
            continue  # Returning to the main menu
        found = False
        for record in parking_records:
            if record["Vehicle Registration Number"] == reg_number.upper() and record["Exit Time"] == "Parking.....":
                entry_time = record["Entry Time"]
                exit_time = get_current_time()
                parking_fee = calculate_parking_fee(entry_time)
                record["Exit Time"] = exit_time
                record["Total Parking Fee"] = parking_fee
                display_available_spaces()
                print(f"\nParking Fee: £{parking_fee}")
                print(f"Entry Time: {entry_time}\nExit Time: {exit_time}")
                found = True
                break
        if not found:
            print(f'\nUnable to find the vehicle holding Registration Number: "{reg_number.upper()}" in the car park records.')
        else:
            print(f"\nRemaining Parking Spaces: {display_available_spaces()}")
            print(f"\nThank you. See you next time.")
            save_records_to_csv()

    elif choice == "3":
        # Option to view available parking spaces
        print("\nRemaining Parking Spaces:", display_available_spaces(), "\n")

    elif choice == "4":
        # Option to query parking record by ticket number
        ticket_number = input("\nEnter Ticket Number (or type '0' to return to the Main Menu): ")
        ticket_number = ''.join(char for char in ticket_number if char.isalnum())
        if ticket_number == "0":
            continue  # Returning to the main menu
        found = False
        for record in parking_records:
            if record["Ticket Number"] == ticket_number.upper():
                # Display parking record information
                print(f"\nRegistration Number: {record['Vehicle Registration Number']}")
                print(f"Parking Space ID: {record['Parking Space ID']}")
                print(f"Entry Time: {record['Entry Time']}")
                print(f"Exit Time: {record['Exit Time']}")
                print(f"Parking Fee: {record['Total Parking Fee']}")
                found = True
                break
        if not found:
            print(f'\nTicket number: "{ticket_number.upper()}" is not found.')

    elif choice == "5":
        # Option to quit the program
        save_records_to_csv()
        print("\nThank you for using our Car Park Services. Have a great day!")
        break
    else:
        # Invalid choice
        print("\nInvalid choice. Please choose a valid option.")

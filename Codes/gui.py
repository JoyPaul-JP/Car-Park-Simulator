import tkinter as tk
from tkinter import ttk
from car_parking_source import *

class CarParkGUI:
    def __init__(self, master):
        # Initializing the GUI
        self.master = master
        self.master.title("Car Park Management System")

        # Setting a modern theme
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Options Frame
        self.options_frame = ttk.Frame(self.master)
        self.options_frame.grid(row=0, column=0, pady=20)

        # Title Label
        self.title_label = ttk.Label(self.master, text="", font=("Helvetica", 16, "bold"))
        self.title_label.grid(row=1, column=0, pady=10)

        # Input Frame
        self.input_frame = ttk.Frame(self.master)
        self.input_frame.grid(row=2, column=0, pady=10)

        # Output Text Widget
        self.output_text = tk.Text(self.master, height=10, width=50, state=tk.DISABLED, wrap=tk.WORD, bg="#f0f0f0", font=("Helvetica", 10))
        self.output_text.grid(row=3, column=0, pady=20, padx=20, sticky="nsew")

        # Creating a scrollbar for the output text
        scrollbar = ttk.Scrollbar(self.master, command=self.output_text.yview)
        scrollbar.grid(row=3, column=1, pady=20, sticky="nsew")
        self.output_text["yscrollcommand"] = scrollbar.set

        # Variable to track the current mode
        self.current_mode = None

        # Configuring column and row weights
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=0)
        self.master.rowconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=0)
        self.master.rowconfigure(2, weight=0)
        self.master.rowconfigure(3, weight=1)

        # Welcome page
        self.create_welcome_page()

    def create_welcome_page(self):
        # Creating the welcome page with buttons
        ttk.Label(self.options_frame, text="Welcome to Car Park Management System", font=("Helvetica", 18, "bold")).grid(row=0, column=0, pady=20, padx=20, columnspan=5)

        # Creating buttons with command to set the current mode and update the window title
        ttk.Button(self.options_frame, text="Enter The Car Park\n(Hourly Rate: £2)", width=30, command=lambda: self.show_input("Enter Car Park")).grid(row=1, column=0, pady=10, padx=10)
        ttk.Button(self.options_frame, text="Exit The Car Park", width=30, command=lambda: self.show_input("Exit Car Park")).grid(row=1, column=1, pady=10, padx=10)
        ttk.Button(self.options_frame, text="View Available\nParking Spaces", width=30, command=lambda: self.show_input("View Spaces")).grid(row=1, column=2, pady=10, padx=10)
        ttk.Button(self.options_frame, text="Query Parking Record\nby Ticket Number", width=30, command=lambda: self.show_input("Query Record")).grid(row=1, column=3, pady=10, padx=10)
        ttk.Button(self.options_frame, text="Quit", width=30, command=self.quit_application).grid(row=1, column=4, pady=10, padx=10)

        # Setting initial title
        self.title_label["text"] = "Car Park Management System"

    def show_input(self, mode):
        # Clearing output and input frames
        self.clear_output_text()
        for widget in self.input_frame.winfo_children():
            widget.destroy()

        # Setting current mode
        self.current_mode = mode

        # Updating title label
        self.title_label["text"] = self.get_mode_title(mode)

        if mode == "Enter Car Park" or mode == "Exit Car Park":
            # Entry form for entering or exiting the car park
            ttk.Label(self.input_frame, text="Vehicle Registration Number:", font=("Helvetica", 12)).grid(row=0, column=0, pady=5, padx=5)
            self.reg_number_entry = ttk.Entry(self.input_frame, font=("Helvetica", 12))
            self.reg_number_entry.grid(row=0, column=1, pady=5, padx=5, ipady=4)
            self.reg_number_entry.insert(0, "Enter vehicle registration number")  # Default text
            self.reg_number_entry.bind("<FocusIn>", lambda event: self.reg_number_entry.delete(0, tk.END))
            ttk.Button(self.input_frame, text="Enter", command=self.process_input, style="TButton").grid(row=0, column=2, pady=10, padx=10)
            self.reg_number_entry.bind("<Return>", lambda event: self.process_input())  # Bind Enter key to execute
            self.reg_number_entry.focus_set()  # Setting focus to the entry field
        elif mode == "Query Record":
            # Entry form for querying parking records
            ttk.Label(self.input_frame, text="Ticket Number:", font=("Helvetica", 12)).grid(row=0, column=0, pady=5, padx=5)
            self.ticket_number_entry = ttk.Entry(self.input_frame, font=("Helvetica", 12))
            self.ticket_number_entry.grid(row=0, column=1, pady=5, padx=5, ipady=4)
            self.ticket_number_entry.insert(0, "Enter ticket number")  # Default text
            self.ticket_number_entry.bind("<FocusIn>", lambda event: self.ticket_number_entry.delete(0, tk.END))
            ttk.Button(self.input_frame, text="Query", command=self.process_input, style="TButton").grid(row=0, column=2, pady=10, padx=10)
            self.ticket_number_entry.bind("<Return>", lambda event: self.process_input())
            self.ticket_number_entry.focus_set()  # Setting focus to the entry field
        elif mode == "View Spaces":
            # No input is required for "View Spaces"
            self.process_input()

    def process_input(self):
        # Processing user input based on the current mode
        if self.current_mode == "Enter Car Park":
            reg_number = self.reg_number_entry.get().upper()
            self.enter_car_park(reg_number)
        elif self.current_mode == "Exit Car Park":
            reg_number = self.reg_number_entry.get().upper()
            self.exit_car_park(reg_number)
        elif self.current_mode == "Query Record":
            ticket_number = self.ticket_number_entry.get().upper()
            self.query_parking_record(ticket_number)
        elif self.current_mode == "View Spaces":
            self.view_available_spaces()

    def enter_car_park(self, reg_number):
        # Logic for entering a vehicle into the car park
        if not reg_number or reg_number.isspace():
            self.show_message("\nPlease enter a valid vehicle Registration Number.")
            return

        reg_number = ''.join(char for char in reg_number if char.isalnum())

        if self.display_available_spaces() == 0:
            self.show_message("\nSorry, the car park is full. No free space is available.")
            return

        if is_vehicle_already_parked(reg_number):
            self.show_message(f'\nThe vehicle holding Registration Number: "{reg_number.upper()}" is parked already.')
            return

        available_parking_space_ids = list(range(1, 9))
        taken_parking_space_ids = set()

        for record in parking_records:
            if record["Exit Time"] == "Parking.....":
                taken_parking_space_ids.add(int(record["Parking Space ID"]))

        available_parking_space_ids = [space_id for space_id in available_parking_space_ids if
                                       space_id not in taken_parking_space_ids]

        if available_parking_space_ids:
            ticket_number = generate_ticket_number(reg_number)
            parking_space_id = random.choice(available_parking_space_ids)
            entry_time = get_current_time()

            parking_records.append({
                "Serial Number": len(parking_records) + 1,
                "Ticket Number": ticket_number,
                "Vehicle Registration Number": reg_number,
                "Parking Space ID": parking_space_id,
                "Entry Time": entry_time,
                "Exit Time": "Parking.....",
                "Total Parking Fee": "Parking....."
            })

            self.update_output_text(f"Ticket Number: {ticket_number}\n"
                                    f"Vehicle Registration Number: {reg_number}\n"
                                    f"Parking Space ID: {parking_space_id}\n"
                                    f"Entry Time: {entry_time}\n"
                                    f"Exit Time: Parking.....\n"
                                    f"Total Parking Fee: Parking.....\n"
                                    f"\nRemaining Parking Spaces: {self.display_available_spaces()}")

            # Clearing input field after processing
            self.reg_number_entry.delete(0, tk.END)

            # Setting focus to the entry field
            self.reg_number_entry.focus_set()

            save_records_to_csv()
        else:
            self.show_message("\nSorry, the car park is full. No free spaces are available.")

    def exit_car_park(self, reg_number):
        # Logic for exiting a vehicle from the car park
        reg_number = ''.join(char for char in reg_number if char.isalnum())
        if not reg_number or reg_number.isspace():
            self.show_message("\nPlease enter a valid vehicle Registration Number.")
            return

        found = False
        for record in parking_records:
            if record["Vehicle Registration Number"] == reg_number and record["Exit Time"] == "Parking.....":
                entry_time = record["Entry Time"]
                exit_time = get_current_time()
                parking_fee = calculate_parking_fee(entry_time)

                record["Exit Time"] = exit_time
                record["Total Parking Fee"] = parking_fee
                save_records_to_csv()

                self.show_message(f"Parking Fee: £{parking_fee}\n"
                                  f"Entry Time: {entry_time}\n"
                                  f"Exit Time: {exit_time}\n"
                                  f"\nRemaining Parking Spaces: {self.display_available_spaces()}\n"
                                  f"\nThank you. See you next time.")
                found = True
                break

        if not found:
            self.show_message(
                f'\nUnable to find the vehicle holding Registration Number: "{reg_number}" in the car park records.')

        # Clearing input field after processing
        self.reg_number_entry.delete(0, tk.END)

        # Setting focus to the entry field
        self.reg_number_entry.focus_set()

    def query_parking_record(self, ticket_number):
        # Logic for querying a parking record by ticket number
        ticket_number = ''.join(char for char in ticket_number if char.isalnum())
        if not ticket_number or ticket_number.isspace():
            self.show_message("\nPlease enter a valid Ticket Number.")
            return

        found = False
        for record in parking_records:
            if record["Ticket Number"] == ticket_number:
                self.update_output_text(f"Registration Number: {record['Vehicle Registration Number']}\n"
                                        f"Parking Space ID: {record['Parking Space ID']}\n"
                                        f"Entry Time: {record['Entry Time']}\n"
                                        f"Exit Time: {record['Exit Time']}\n"
                                        f"Parking Fee: {record['Total Parking Fee']}")
                found = True
                break

        if not found:
            self.show_message(f'\nTicket number: "{ticket_number.upper()}" is not found.')

        # Clearing input field after processing
        self.ticket_number_entry.delete(0, tk.END)

        # Setting focus to the entry field
        self.ticket_number_entry.focus_set()

    def view_available_spaces(self):
        # Logic for viewing available parking spaces
        available_spaces = self.display_available_spaces()
        self.update_output_text(f"\nRemaining Parking Spaces: {available_spaces}")
        save_records_to_csv()

    def quit_application(self):
        # Logic for quitting the application
        save_records_to_csv()
        self.master.destroy()

    def clear_output_text(self):
        # Clearing the output text widget
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)

    def show_message(self, message):
        # Displaying a message in the output text widget
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.config(state=tk.DISABLED)

    def update_output_text(self, text):
        # Updating the output text widget with the provided text
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, text)
        self.output_text.config(state=tk.DISABLED)

    def display_available_spaces(self):
        # Calculating and return the number of available parking spaces
        occupied_spaces = len([record for record in parking_records if record["Exit Time"] == "Parking....."])
        available_spaces = PARKING_CAPACITY - occupied_spaces
        return available_spaces

    def get_mode_title(self, mode):
        # Getting the title corresponding to the current mode
        if mode == "Enter Car Park":
            return "Enter The Car Park (Hourly Rate: £2)"
        elif mode == "Exit Car Park":
            return "Exit The Car Park"
        elif mode == "View Spaces":
            return "View Available Parking Spaces"
        elif mode == "Query Record":
            return "Query Parking Record by Ticket Number"
        else:
            return mode

def main():
    # Main function to create and run the GUI
    root = tk.Tk()
    app = CarParkGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

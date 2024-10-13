import tkinter as tk
from tkinter import ttk
import obd

class OBDApp:
    def __init__(self, master):
        self.master = master
        master.title("RIH4KRC-OBD")
        master.geometry("800x600")  # Set the window size
        master.resizable(True, True)  # Allow resizing

        # Center the window
        self.center_window(master)

        # Style configuration
        style = ttk.Style()
        style.configure("TLabel", font=("Poppins", 14), padding=10)
        style.configure("TButton", font=("Poppins", 12), padding=5)
        style.configure("TFrame", padding=15)

        # Create a frame for dashboard
        self.dashboard_frame = ttk.Frame(master)
        self.dashboard_frame.pack(expand=True)

        # Create cards for different OBD-II parameters
        self.create_param_card("Speed", "N/A", 0, 0)
        self.create_param_card("RPM", "N/A", 0, 1)
        self.create_param_card("Fuel Level", "N/A", 0, 2)
        self.create_param_card("Coolant Temp", "N/A", 1, 0)
        self.create_param_card("Engine Load", "N/A", 1, 1)
        self.create_param_card("Throttle Position", "N/A", 1, 2)
        self.create_param_card("Intake Temp", "N/A", 2, 0)
        self.create_param_card("Vehicle Speed", "N/A", 2, 1)
        self.create_param_card("Mileage", "N/A", 2, 2)
        self.create_param_card("Engine Runtime", "N/A", 3, 0)

        # Start and Stop Buttons
        self.start_button = ttk.Button(master, text="Start", command=self.start_reading)
        self.start_button.pack(pady=20)

        self.stop_button = ttk.Button(master, text="Stop", command=self.stop_reading, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.connection = None
        self.running = False

    def create_param_card(self, title, value, row, col):
        """Create a card for each parameter."""
        card = ttk.Frame(self.dashboard_frame, relief="groove", borderwidth=2)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        title_label = ttk.Label(card, text=title, font=("Helvetica", 16))
        title_label.pack()

        value_label = ttk.Label(card, text=value, font=("Helvetica", 14))
        value_label.pack()

        # Store the value label for later updates
        setattr(self, f"{title.lower().replace(' ', '_')}_label", value_label)

        # Configure grid weights for responsiveness
        self.dashboard_frame.grid_rowconfigure(row, weight=1)
        self.dashboard_frame.grid_columnconfigure(col, weight=1)

    def center_window(self, window):
        """Center the window on the screen."""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')

    def start_reading(self):
        self.connection = obd.OBD()
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.read_data()

    def stop_reading(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def read_data(self):
        if self.running:
            # Define commands to query
            commands = {
                "speed": obd.commands.SPEED,
                "rpm": obd.commands.RPM,
                "fuel_level": obd.commands.FUEL_LEVEL,
                "coolant_temp": obd.commands.COOLANT_TEMP,
                "engine_load": obd.commands.ENGINE_LOAD,
                "throttle_pos": obd.commands.THROTTLE_POS,
                "intake_temp": obd.commands.INTAKE_TEMP,
                "vehicle_speed": obd.commands.SPEED,
                "mileage": obd.commands.DISTANCE_SINCE_DTC_CLEAR,
                "engine_runtime": obd.commands.RUN_TIME
            }

            # Get responses
            responses = {cmd: self.connection.query(command) for cmd, command in commands.items()}

            # Update labels with values
            self.speed_label.config(text=f"{responses['speed'].value.mph if responses['speed'].value else 'N/A'} mph")
            self.rpm_label.config(text=f"{responses['rpm'].value.rpm if responses['rpm'].value else 'N/A'} RPM")
            self.fuel_level_label.config(text=f"{responses['fuel_level'].value.percent if responses['fuel_level'].value else 'N/A'}%")
            self.coolant_temp_label.config(text=f"{responses['coolant_temp'].value.celsius if responses['coolant_temp'].value else 'N/A'}°C")
            self.engine_load_label.config(text=f"{responses['engine_load'].value.percent if responses['engine_load'].value else 'N/A'}%")
            self.throttle_position_label.config(text=f"{responses['throttle_pos'].value.percent if responses['throttle_pos'].value else 'N/A'}%")
            self.intake_temp_label.config(text=f"{responses['intake_temp'].value.celsius if responses['intake_temp'].value else 'N/A'}°C")
            self.vehicle_speed_label.config(text=f"{responses['vehicle_speed'].value.mph if responses['vehicle_speed'].value else 'N/A'} mph")
            self.mileage_label.config(text=f"{responses['mileage'].value.miles if responses['mileage'].value else 'N/A'} miles")
            self.engine_runtime_label.config(text=f"{responses['engine_runtime'].value.minutes if responses['engine_runtime'].value else 'N/A'} min")

            self.master.after(1000, self.read_data)  # read every second

if __name__ == "__main__":
    root = tk.Tk()
    app = OBDApp(root)
    root.mainloop()
# --- CONFIGURATION ---
SECONDS_PER_HOUR = 2.2  # Speed of the simulation (seconds per simulated hour)
TURN_ON_HOUR = 45       # Simulated hour that triggers the pulse signal
FARING_HOUR = 48
PULSE_START_PIN = 18          # GPIO pin sending the pulse (Physical Pin 11)
PULSE_STOP_PIN = 23         # GPIO pin sending the pulse (Physical Pin 11)
INPUT_START_PIN = 24          # GPIO pin for physical start button (Physical Pin 13)
INPUT_RESET_PIN = 25          # GPIO pin for physical reset button (Physical Pin 15)

# --- ARRAY (53 ELEMENTS) ---
HOURLY_TARGETS = [
    0.9, 1.1, 0.8, 0.9, 0.6, 0.65, 0.45, 0.4, 0.7, 0.85, 0.8, 1.0, 1.1, 1.0, 
    1.4, 1.7, 1.6, 1.7, 1.9, 1.4, 1.5, 1.6, 1.4, 1.2, 1.0, 1.1, 0.8, 0.9, 
    0.85, 0.85, 0.8, 1.1, 1.25, 1.55, 2.2, 2.15, 2.1, 2.2, 2.6, 2.4, 2.35, 
    2.0, 2.1, 1.4, 1.3, 0.9, 0.85, 0.45, 0.3, 0.25, 0.1, 0.2, 0.1
]

class Status:
    is_running = False
    simulated_hour = 0
    current_value = 0.0
    current_color = "Blue"
    heater_active = False
    faring_active = False
    history = []

status = Status()
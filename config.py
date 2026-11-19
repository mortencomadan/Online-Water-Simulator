# --- CONFIGURATION ---
SECONDS_PER_HOUR = 2.2   # Speed of the simulation (seconds per simulated hour)

START_HOUR = -26         # Relative hour to start at (-48 is the very beginning, e.g., -10 starts 10h before faring)
TURN_ON_HOUR = -3        # Relative hour that triggers the pulse signal (3 hours before faring)
FARING_HOUR = 0          # Relative hour where faring starts (always 0)
FARING_INDEX = 48        # Position in HOURLY_TARGETS that corresponds to Hour 0

PULSE_START_PIN = 18     # BCM 18 (Physical Pin 12)
PULSE_STOP_PIN = 23      # BCM 23 (Physical Pin 16)
INPUT_START_PIN = 24     # BCM 24 (Physical Pin 18)
INPUT_RESET_PIN = 25     # BCM 25 (Physical Pin 22)

# --- ARRAY (53 ELEMENTS) ---
HOURLY_TARGETS = [
    0.9, 1.1, 0.8, 0.9, 0.6, 0.65, 0.45, 0.4, 0.7, 0.85, 0.8, 1.0, 1.1, 1.0, 
    1.4, 1.7, 1.6, 1.7, 1.9, 1.4, 1.5, 1.6, 1.4, 1.2, 1.0, 1.1, 0.8, 0.9, 
    0.85, 0.85, 0.8, 1.1, 1.25, 1.55, 2.2, 2.15, 2.1, 2.2, 2.6, 2.4, 2.35, 
    2.0, 2.1, 1.4, 1.3, 0.9, 0.85, 0.45, 0.3, 0.25, 0.1, 0.2, 0.1, 0.2, 0.1, 0.2, 0.1,
]

class Status:
    def __init__(self):
        self.reset()

    def reset(self):
        self.is_running = False
        self.simulated_hour = START_HOUR
        self.current_value = 0.0
        self.current_color = "Blue"
        self.heater_active = False
        self.faring_active = False
        self.history = []

status = Status()
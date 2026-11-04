import time
import threading
from flask import Flask, render_template, jsonify
from gpiozero import LED, Button

# --- CONFIGURATION ---
SECONDS_PER_HOUR = 2.2  # Speed of the simulation (seconds per simulated hour)
TURN_ON_HOUR = 3       # Simulated hour that triggers the pulse signal
FARING_HOUR = 6
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

app = Flask(__name__)

# Global status tracking
status = {
    "is_running": False,
    "simulated_hour": 0,
    "current_value": 0.0,
    "current_color": "Blue",
    "pulse_active": False,  
    "faring_active": False,  
    "history": []
}

def perform_reset():
    """Shared reset logic for both physical button and web requests"""
    global status
    try:
        pulse_stop_output.on()
        time.sleep(0.1)
        pulse_stop_output.off()    
    except NameError:
        pass
    status["is_running"] = False
    status["simulated_hour"] = 0
    status["current_value"] = 0.0
    status["current_color"] = "Blue"  # FIX: Fjernet komma, så det ikke er en tuple
    status["pulse_active"] = False
    status["faring_active"] = False
    status["history"] = []
    print("--- SYSTEM RESET ACTIVATED ---")

# Physical Hardware Setup via gpiozero
try:
    pulse_start_output = LED(PULSE_START_PIN)
    pulse_stop_output = LED(PULSE_STOP_PIN)
    
    start_button = Button(INPUT_START_PIN, pull_up=True)
    def start_demo():
        if not status["is_running"]:
            print("--- INPUT ACTIVATED: STARTING DEMO NOW ---")
            status["is_running"] = True
    start_button.when_pressed = start_demo

    reset_button = Button(INPUT_RESET_PIN, pull_up=True)
    reset_button.when_pressed = perform_reset

except Exception as e:
    print(f"GPIO initialization failed (Testing on PC?): {e}")

def time_simulation():
    global status

    while True:
        if not status["is_running"]:
            time.sleep(0.2)
            continue

        start_time = time.time()
        hour_at_start = status["simulated_hour"]

        start_val = 0.0
        end_val = HOURLY_TARGETS[hour_at_start]

        while time.time() - start_time < SECONDS_PER_HOUR:
            if not status["is_running"]:
                break

            progress = (time.time() - start_time) / SECONDS_PER_HOUR
            status["current_value"] = start_val + (end_val - start_val) * progress
            time.sleep(0.01)

        if not status["is_running"]:
            continue

        # --- FIX: Tjek og opdater farver FØR timen gemmes i historikken ---
        if status["simulated_hour"] == TURN_ON_HOUR:
            print(f"--- HOUR {TURN_ON_HOUR} REACHED! SENDING PULSE ---")
            try:
                status["pulse_active"] = True  
                status["current_color"] = "Yellow"
                pulse_start_output.on()
                time.sleep(0.1)
                pulse_start_output.off()                
            except NameError:
                status["pulse_active"] = False
                status["current_color"] = "Yellow" # Sørg for farveskift selv uden GPIO hardware
                
        if status["simulated_hour"] == FARING_HOUR:
            status["current_color"] = "Red"
            status["faring_active"] = True

        # Gem i historikken med den HELT rigtige opdaterede farve
        status["history"].append({
            "hour": status["simulated_hour"],
            "value": status["current_value"],
            "color": status["current_color"]
        })

        if len(status["history"]) > 24:
            status["history"].pop(0)

        if status["simulated_hour"] == len(HOURLY_TARGETS) - 1:
            print("--- SIMULATION FINISHED: AUTOMATIC STOP ---")
            status["is_running"] = False
            status["current_value"] = 0.0
            continue

        status["simulated_hour"] += 1

# Start simulation thread
threading.Thread(target=time_simulation, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    return jsonify({
        "is_running": status["is_running"],
        "hour": status["simulated_hour"],
        "value": status["current_value"],
        "pulse_active": status["pulse_active"], 
        "faring_active": status["faring_active"], 
        "color": status["current_color"],
        "history": status["history"]
    })

@app.route('/start_via_web')
def start_via_web():
    if not status["is_running"]:
        status["is_running"] = True
    return jsonify({"status": "started"})

@app.route('/stop_via_web')
def stop_via_web():
    if status["is_running"]:
        status["is_running"] = False
    return jsonify({"status": "stopped"})

@app.route('/reset_via_web')
def reset_via_web():
    perform_reset()
    return jsonify({"status": "resetted"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

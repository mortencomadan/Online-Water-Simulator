# simulator.py
import time
import config
from pi_io import pulse_start, pulse_stop

def get_color(is_heater_active, is_faring):
    match (is_heater_active, is_faring):
        case (False, False):
            return "Blue"
        case (True, False):
            return "Yellow"
        case (_, True):
            return "Red"

def time_simulation():
    # Calculate the final relative hour in the array (52 - 48 = +4)
    final_hour = (len(config.HOURLY_TARGETS) - 1) - config.FARING_INDEX

    while True:
        if not config.status.is_running:
            time.sleep(0.2)
            continue

        if config.status.simulated_hour >= config.TURN_ON_HOUR and not config.status.heater_active:
            print(f"--- HOUR {config.status.simulated_hour} REACHED! SENDING PULSE ---")
            config.status.heater_active = True
            pulse_start()

        if config.status.simulated_hour >= config.FARING_HOUR and not config.status.faring_active:
            print(f"--- FARING STARTED (HOUR {config.status.simulated_hour}) ---")
            config.status.faring_active = True

        config.status.current_color = get_color(config.status.heater_active, config.status.faring_active)

        start_time = time.time()
        array_index = config.FARING_INDEX + config.status.simulated_hour
        start_val = 0.0
        end_val = config.HOURLY_TARGETS[array_index]

        was_interrupted = False

        while time.time() - start_time < config.SECONDS_PER_HOUR:
            if not config.status.is_running:
                was_interrupted = True
                break
            progress = (time.time() - start_time) / config.SECONDS_PER_HOUR
            config.status.current_value = start_val + (end_val - start_val) * progress
            time.sleep(0.01)

        config.status.history.append({
            "hour": config.status.simulated_hour,
            "value": config.status.current_value,
            "color": config.status.current_color
        })

        if len(config.status.history) > 24:
            config.status.history.pop(0)

        if was_interrupted:
            print("--- SIMULATION MANUALLY STOPPED ---")
            pulse_stop()
            config.status.is_running = False
            config.status.current_value = 0.0            
            continue 

        # Automatically restart at START_HOUR when the final hour (+4) finishes
        if config.status.simulated_hour >= final_hour:
            print("--- SIMULATION FINISHED: RESTARTING AUTOMATICALLY ---")
            pulse_stop()
            config.status.history.clear()
            config.status.simulated_hour = config.START_HOUR
            config.status.heater_active = False
            config.status.faring_active = False
            config.status.current_value = 0.0
            continue

        # Advance to the next hour only if the current hour finished uninterrupted
        config.status.simulated_hour += 1

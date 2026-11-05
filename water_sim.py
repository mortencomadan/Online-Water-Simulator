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
    while True:
        if not config.status.is_running:
            time.sleep(0.2)
            continue

        if config.status.simulated_hour == config.TURN_ON_HOUR:
            print(f"--- HOUR {config.TURN_ON_HOUR} REACHED! SENDING PULSE ---")
            config.status.heater_active = True
            pulse_start()

        if config.status.simulated_hour == config.FARING_HOUR:
            config.status.faring_active = True

        config.status.current_color = get_color(config.status.heater_active, config.status.faring_active)

        start_time = time.time()
        hour_at_start = config.status.simulated_hour
        start_val = 0.0
        end_val = config.HOURLY_TARGETS[hour_at_start]

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

        if config.status.simulated_hour == len(config.HOURLY_TARGETS) - 1:
            print("--- SIMULATION FINISHED: AUTOMATIC STOP ---")
            pulse_stop()
            config.status.is_running = False
            config.status.current_value = 0.0
            continue

        # 4. Gå KUN til næste time, hvis timen blev gennemført helt uden stop
        config.status.simulated_hour += 1

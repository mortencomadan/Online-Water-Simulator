# io_hardware.py
import time
from gpiozero import LED, Button
import config

pulse_start_output = None
pulse_stop_output = None

def pulse_start():    
    pulse_start_output.on()
    time.sleep(0.1)
    pulse_start_output.off()
    

def pulse_stop():
    pulse_stop_output.on()
    time.sleep(0.1)
    pulse_stop_output.off()


def start_demo():
    if not config.status.is_running:
        print("--- INPUT ACTIVATED: STARTING DEMO NOW ---")
        config.status.is_running = True

def perform_reset():
    """Shared reset logic for both physical button and web requests"""
    pulse_stop()    
    config.status.is_running = False
    config.status.simulated_hour = 0
    config.status.current_value = 0.0
    config.status.program_active = False
    config.status.faring_active = False
    config.status.history = []
    print("--- SYSTEM RESET ACTIVATED ---")

# Physical Hardware Setup via gpiozero
try:
    pulse_start_output = LED(config.PULSE_START_PIN)
    pulse_stop_output = LED(config.PULSE_STOP_PIN)
    
    start_button = Button(config.INPUT_START_PIN, pull_up=True)
    start_button.when_pressed = start_demo

    reset_button = Button(config.INPUT_RESET_PIN, pull_up=True)
    reset_button.when_pressed = perform_reset
except Exception as e:
    print(f"GPIO initialization failed (Testing on PC?): {e}")

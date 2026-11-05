# app.py
import threading
from flask import Flask, render_template, jsonify
import config
from pi_io import perform_reset
from water_sim import time_simulation

app = Flask(__name__)

# Start simulation thread immediately
threading.Thread(target=time_simulation, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    return jsonify({
        "is_running": config.status.is_running,
        "hour": config.status.simulated_hour,
        "value": config.status.current_value,
        "heater_active": config.status.heater_active, 
        "faring_active": config.status.faring_active, 
        "color": config.status.current_color,
        "history": config.status.history
    })

@app.route('/start_via_web')
def start_via_web():
    if not config.status.is_running:
        config.status.is_running = True
    return jsonify({"status": "started"})

@app.route('/stop_via_web')
def stop_via_web():
    if config.status.is_running:
        config.status.is_running = False
    return jsonify({"status": "stopped"})

@app.route('/reset_via_web')
def reset_via_web():
    perform_reset()
    return jsonify({"status": "resetted"})

if __name__ == '__main__':
    # Running debug=False eliminates multiple thread instantiation cycles
    app.run(host='0.0.0.0', port=5000, debug=False)

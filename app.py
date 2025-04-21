from flask import Flask, render_template
import os
import psutil
import time

app = Flask(__name__)

# Dummy function for anomalies
def get_anomalies():
    return ["CPU Usage High", "Memory Leak Detected"]

@app.route("/")
def home():
    anomalies = get_anomalies()
    return render_template("index.html", anomalies=anomalies)

@app.route("/logs")
def logs():
    log_file = "logs/system.log"
    if os.path.exists(log_file):
        with open(log_file, "r") as file:
            log_data = file.readlines()
    else:
        log_data = ["No logs available"]
    return render_template("logs.html", logs=log_data)


import os
import time
import psutil

recovery_status = {"last_triggered": "Never", "status": "OK"}

def run_recovery():
    print("Recovery logic triggered.")

    os.makedirs("logs", exist_ok=True)

    try:
        with open("logs/system.log", "a") as log_file:  # ✅ no space in variable name
            log_file.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Recovery was triggered manually.\n")

            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    if proc.info['cpu_percent'] is not None and proc.info['cpu_percent'] >= 20:
                        name = proc.info.get('name', 'Unknown')
                        pid = proc.info.get('pid', 'Unknown')
                        log_file.write(f"Terminated: {name} (PID {pid})\n")
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
    except Exception as e:
        print(f"❌ Error during recovery: {e}")


recovery_status = {"last_triggered": "Never", "status": "OK"}

@app.route("/status")
def status():
    return recovery_status

@app.route('/recover')
def recover():
    run_recovery()
    recovery_status["last_triggered"] = time.strftime("%Y-%m-%d %H:%M:%S")
    recovery_status["status"] = "Recovery triggered"
    return "Recovery Triggered!"

@app.route("/cpu")
def cpu_usage():
    usage = psutil.cpu_percent()
    return {"cpu": usage}

if __name__ == "__main__":
    app.run(debug=True)

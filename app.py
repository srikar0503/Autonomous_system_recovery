from flask import Flask, render_template, jsonify
import os, time, threading
import numpy as np
import psutil

# Import AI-based anomaly detector
from ai_model.anomaly_detection import detect_anomalies

app = Flask(__name__)

recovery_status = {
    "last_triggered": "Never",
    "status": "Monitoring"
}

# Generate system vector for AI model
def generate_system_vector():
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    # Simulate more system features (random for now)
    extra_metrics = list(np.random.rand(7) * 100)
    vector = [cpu, mem, disk] + extra_metrics
    return np.array(vector[:10])  # Ensure 10-element vector

# Recovery logic
def run_recovery():
    print("🔧 Recovery triggered.")
    os.makedirs("logs", exist_ok=True)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    with open("logs/system.log", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] 🚨 Recovery was triggered automatically.\n")


    recovery_status["last_triggered"] = timestamp
    recovery_status["status"] = "Auto Recovery Triggered"

# Dashboard route
@app.route("/")
def home():
    anomalies = get_anomalies()
    return render_template("index.html", anomalies=anomalies)

# Manual trigger
@app.route("/recover")
def manual_recover():
    run_recovery()
    return "Recovery Triggered!"

# Live recovery status
@app.route("/status")
def status():
    return jsonify(recovery_status)

# Show logs
@app.route("/logs")
def logs():
    log_file = "logs/system.log"
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            lines = f.readlines()
    else:
        lines = ["No logs yet."]
    return render_template("logs.html", logs=lines)

# Clear logs
@app.route("/clear_logs")
def clear_logs():
    os.makedirs("logs", exist_ok=True)
    open("logs/system.log", "w").close()
    return "✅ Logs have been cleared!"

# CPU for live chart
@app.route("/cpu")
def cpu():
    return jsonify({"cpu": psutil.cpu_percent()})

@app.route("/memory")
def memory():
    return jsonify({"memory": psutil.virtual_memory().percent})


# Human-readable anomaly info for UI
def get_anomalies():
    anomalies = []
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    if cpu > 80:
        anomalies.append(f"⚠️ High CPU Usage: {cpu}%")
    if mem > 75:
        anomalies.append(f"⚠️ High Memory Usage: {mem}%")
    return anomalies if anomalies else ["✅ All systems normal"]

def clear_memory():
    print("🧹 Attempting to free memory...")
    os.makedirs("logs", exist_ok=True)

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    WHITELIST = [
        "python", "python3", "flask", "idea64.exe", "pycharm", "code", "explorer.exe",
        "System", "systemd", "init", "chrome", "cmd.exe"
    ]

    with open("logs/system.log", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] 🧹 Memory cleanup started...\n")

        # Kill high memory-consuming processes
        for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
            try:
                if proc.info['memory_percent'] > 30:
                    f.write(f"Terminating {proc.info['name']} (PID {proc.info['pid']}) — Memory: {proc.info['memory_percent']:.2f}%\n")
                    psutil.Process(proc.info['pid']).terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        f.write(f"[{timestamp}] ✅ Memory cleanup complete.\n")

def auto_monitor():
    while True:
        system_vector = generate_system_vector()
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent

        # AI-based or threshold anomaly
        if detect_anomalies(system_vector) or cpu > 80:
            print("🚨 AI/CPU anomaly detected! Triggering recovery.")
            run_recovery()

        # Memory cleanup trigger
        if mem > 85:
            print(f"🚨 High Memory Usage: {mem:.1f}%. Triggering memory cleaner...")
            clear_memory()

        time.sleep(5)


if __name__ == "__main__":
    threading.Thread(target=auto_monitor, daemon=True).start()
    app.run(debug=True)

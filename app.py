from flask import Flask, render_template
import os

app = Flask(__name__)

# Dummy function for anomalies (Replace with real AI model output)
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

if __name__ == "__main__":
    app.run(debug=True)

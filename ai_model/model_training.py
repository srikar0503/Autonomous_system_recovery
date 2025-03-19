import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
import os

# Define model file path
MODEL_PATH = "ai_model/anomaly_model.pkl"

def generate_training_data(samples=1000):
    """
    Generate synthetic training data for anomaly detection.
    Normal values: CPU/MEM usage between 10-60%.
    Anomalous values: CPU/MEM usage above 80%.
    """
    normal_data = np.random.uniform(10, 60, (samples, 2))  # Normal system metrics
    anomaly_data = np.random.uniform(80, 100, (samples // 10, 2))  # Anomalous cases
    data = np.vstack((normal_data, anomaly_data))
    return data

def train_anomaly_model():
    """
    Train an Isolation Forest model for anomaly detection.
    """
    print("[INFO] Generating training data...")
    training_data = generate_training_data()

    print("[INFO] Training Isolation Forest model...")
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(training_data)

    print(f"[INFO] Saving trained model to {MODEL_PATH}")
    joblib.dump(model, MODEL_PATH)

def load_anomaly_model():
    """
    Load the trained anomaly detection model.
    If the model file does not exist, train a new one.
    """
    if not os.path.exists(MODEL_PATH):
        print("[WARNING] Model not found! Training a new model...")
        train_anomaly_model()

    print("[INFO] Loading anomaly detection model...")
    return joblib.load(MODEL_PATH)

if __name__ == "__main__":
    train_anomaly_model()  # Train the model when script is run

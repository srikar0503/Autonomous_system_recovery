import numpy as np
import tensorflow as tf

# Load a pre-trained model (or create one)
def load_model():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(64, activation="relu", input_shape=(10,)),
        tf.keras.layers.Dense(32, activation="relu"),
        tf.keras.layers.Dense(1, activation="sigmoid")
    ])
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    return model

# Dummy function to detect anomalies
def detect_anomalies(data):
    model = load_model()
    predictions = model.predict(np.array([data]))  # Simulating anomaly detection
    return predictions[0][0] > 0.5  # Returns True if anomaly detected
def simulate_anomaly_trigger():
    print("Simulating CPU-intensive task...")
    for _ in range(5):  # Reduced from infinite
        _ = np.random.rand(1000, 1000)  # 8MB approx
    print("Simulation done.")

# Run test if file is executed directly
if __name__ == "__main__":
    simulate_anomaly_trigger()
    test_input = np.random.rand(10)  # Dummy input vector
    is_anomaly = detect_anomalies(test_input)
    if is_anomaly:
        print("🚨 Anomaly detected!")
    else:
        print("✅ System normal.")
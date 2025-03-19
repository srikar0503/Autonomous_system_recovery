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

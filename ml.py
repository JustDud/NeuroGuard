import os
import json
import sqlite3
from time import sleep
MODEL_PATH = os.path.join(os.path.dirname(__file__), "trained_model.pkl")

FEATURE_COLUMNS = [
    "sunlight_hours",
    "safety",
    "sleep_duration_hours",
    "screen_time_minutes",
    "physical_activity_minutes",
    "daily_goal_progression",
    "hour",
    "weekday"
]

import pandas as pd
with open("generated_sample_data.json", "r") as f:
    sample_data = json.load(f)
from sklearn.ensemble import RandomForestRegressor
import joblib
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
# Load sample data
df = pd.DataFrame(sample_data)

# Map labels to numeric for training
# Converts the list of dictionaries into a DataFrame,
# a table-like structure used by pandas for easy data handling.
df["emotion_label"] = df["mental_state"]

def prepare_data(df):
    X = df[FEATURE_COLUMNS]
    y = df["emotion_label"]
    return X, y


# random_state - responsible for picking random subsets of data or
# features when building each tree in the forest
# (42 is common but can be changed)
def train_model(X, y):
    model = RandomForestRegressor(random_state=42)
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
    return model


def predict_emotion(model, input_dict):
    input_df = pd.DataFrame([input_dict])
    input_df = input_df[FEATURE_COLUMNS]  # Ensure correct column order
    prediction = model.predict(input_df)[0]
    return int(round(prediction))

# X, y = prepare_data(df)

# model = train_model(X, y)

# new_input_data = {
#     "sunlight_hours": 10,
#     "safety": 75,
#     "sleep_duration_hours": 7.5,
#     "screen_time_minutes": 320,
#     "physical_activity_minutes": 45,
#     "daily_goal_progression": 70,
#     "hour": 14,
#     "weekday": 2
# }

# print("Sample of training features:\n", X.head())
# print("\nSample of target labels:\n", y.head())

# predicted_label = predict_emotion(model, new_input_data)
# emotion_label_map = {0: "stressed", 1: "tired", 2: "neutral", 3: "happy"}
# print(f"\nPredicted emotion label: {predicted_label}")
# print(f"Predicted emotion: {emotion_label_map.get(predicted_label, 'Unknown')}")


def retrain_model():
    X, y = prepare_data(df)
    model = train_model(X, y)
    joblib.dump(model, MODEL_PATH)
    print("Model retrained and saved.")
    return model


def load_model():
    return joblib.load(MODEL_PATH)


try:
    model = load_model()
except FileNotFoundError:
    X, y = prepare_data(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = train_model(X_train, y_train)
    joblib.dump(model, MODEL_PATH)

    # Evaluate on test set
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Validation accuracy: {accuracy:.2f}")


def get_mental_state(input_data):
    model = load_model()

    label = predict_emotion(model, input_data)
    return label


# y_pred = model.predict(X)
# accuracy = accuracy_score(y, y_pred)

print("NeuroGuard is now monitoring new user input. Type Ctrl+C to stop.\n")
last_seen_id = None


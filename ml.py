import pandas as pd
from sample_data import sample_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
# Load sample data
df = pd.DataFrame(sample_data)

# Map labels to numeric for training
# Converts the list of dictionaries into a DataFrame,
# a table-like structure used by pandas for easy data handling.
df["emotion_label"] = [
    2, 2, 3, 1, 3, 0, 3, 1, 2, 3,
    0, 3, 1, 3, 0, 3, 0, 3, 0, 3,
    3, 2, 3, 1, 3, 0, 3, 1, 2, 3,
    1, 3, 1, 3, 0, 3, 0, 3, 0, 3,
    3, 2, 3, 1, 3, 0, 3, 1, 2, 3,
    1, 3, 1, 3, 0, 3, 0, 3, 0, 3
]

def prepare_data(df):
    features = [
        "sunlight_hours",
        "safety",
        "sleep_duration_hours",
        "screen_time_minutes",
        "physical_activity_minutes",
        "daily_goal_progression",
        "hour",
        "weekday",
    ]
    X = df[features]
    y = df["emotion_label"]
    return X, y


# random_state - responsible for picking random subsets of data or
# features when building each tree in the forest
# (42 is common but can be changed)
def train_model(X, y):
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)
    return model


def predict_emotion(model, input_dict):
    input_df = pd.DataFrame([input_dict])
    prediction = model.predict(input_df)[0]
    return prediction

X, y = prepare_data(df)
model = train_model(X, y)

new_input_data = {
    "sunlight_hours": 10,
    "safety": 75,
    "sleep_duration_hours": 7.5,
    "screen_time_minutes": 320,
    "physical_activity_minutes": 45,
    "daily_goal_progression": 70,
    "hour": 14,
    "weekday": 2
}


print("Sample of training features:\n", X.head())
print("\nSample of target labels:\n", y.head())

predicted_label = predict_emotion(model, new_input_data)
emotion_label_map = {-1: "stressed", 0: "tired", 1: "neutral", 2: "happy"}
print(f"\nPredicted emotion label: {predicted_label}")
print(f"Predicted emotion: {emotion_label_map.get(predicted_label, 'Unknown')}")

y_pred = model.predict(X)
accuracy = accuracy_score(y, y_pred)

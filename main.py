from dotenv import load_dotenv
import os
import requests
from ml import get_mental_state, retrain_model, MODEL_PATH
import sqlite3
import subprocess
from time import sleep

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={GEMINI_API_KEY}"


def get_latest_user_data():
    with sqlite3.connect("User_Data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM data ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        if not row:
            return None
        # Map row to expected dictionary keys for get_mental_state
        return {
            "sleep_duration_hours": float(row[3]) if row[3] is not None else 0,
            "screen_time_minutes": int(row[4]) if row[4] is not None else 0,
            "physical_activity_minutes": int(row[5]) if row[5] is not None else 0,
            "hour": int(row[6]) if row[6] is not None else 0,
            "weekday": int(row[7]) if row[7] is not None else 0,
            "sunlight_hours": int(row[8]) if row[8] is not None else 0,
            "safety": int(row[9]) if row[9] is not None else 0,
            "daily_goal_progression": int(row[10]) if row[10] is not None else 0
        }



def generate_suggestions(user_message, mental_state, user_data):
    prompt = (
        f"You are NeuroGuard, an AI wellness companion from the year 2080.\n"
        f"The user has just submitted their lifestyle data.\n\n"
        f"Your task is to offer helpful mental health guidance based on this data:\n"
        f"- Estimated mental state score: {mental_state}/100\n"
        f"- Self-described feeling: \"{user_message}\"\n"
        f"- Weekday: {user_data.get('weekday')}\n"
        f"- Hours of sleep: {user_data.get('sleep_duration_hours')}h\n"
        f"- Screen time: {user_data.get('screen_time_minutes')} minutes\n"
        f"- Physical activity: {user_data.get('physical_activity_minutes')} minutes\n"
        f"- Goal progress: {user_data.get('daily_goal_progression')}%\n"
        f"- Safety perception: {user_data.get('safety')}/100\n"
        f"- Sunlight exposure: {user_data.get('sunlight_hours')} hours\n\n"
        "Based on this mental state and the context, suggest exactly **three personalised tips** to help the user improve or stabilise their mental well-being.\n"
        "Each suggestion should be:\n"
        "- Calm, empathetic, and psychologically sound\n"
        "- Backed by behavioural science, mindfulness, or neuroscience\n"
        "- Focused on small, actionable steps the user can take immediately\n\n"
        "Format your response as a friendly, numbered list. Do not say hi, just give the suggestions"
    )

    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    response = requests.post(GEMINI_API_URL, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Error {response.status_code}: {response.text}"


def main():
    if not os.path.exists(MODEL_PATH):
        print("No trained model found. Training now...")
        retrain_model()
    else:
        retrain = input("Type 'train' to retrain the model or press Enter to continue: ").strip().lower()
        if retrain == "train":
            retrain_model()


    # Launch the Flask app in a separate process
    print("Starting web interface...")
    subprocess.Popen(["/usr/bin/python3", "Combination.py"])
    sleep(2)  # wait briefly for Flask to start

    print("NeuroGuard is now monitoring new user input. Type Ctrl+C to stop.\n")
    with sqlite3.connect("User_Data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM data ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        last_seen_id = result[0] if result else None

    while True:
        latest_data = get_latest_user_data()
        if latest_data:
            with sqlite3.connect("User_Data.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM data ORDER BY id DESC LIMIT 1")
                current_id = cursor.fetchone()[0]
            if current_id != last_seen_id:
                print("New input detected.")
                print("Latest user data from DB:", latest_data)
                predicted_state = get_mental_state(latest_data)
                print("Predicted mental_state:", predicted_state)
                suggestion_text = generate_suggestions("No message provided", predicted_state, latest_data)
                print("AI Suggestions:\n", suggestion_text)
                last_seen_id = current_id
            sleep(2)


if __name__ == "__main__":
    main()

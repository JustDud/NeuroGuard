from dotenv import load_dotenv
import os
import requests
from ml_model import get_mental_state, retrain_model, MODEL_PATH
import sqlite3
import subprocess
from time import sleep
import time
from flask import Flask, render_template, url_for, request, session, redirect

load_dotenv()
app = Flask(__name__)
app.secret_key = "supersecretkey"

# Global state (top-level, just below load_dotenv())
latest_predicted_state = 0
latest_suggestion_text = "Loading your personalised analysis..."

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={GEMINI_API_KEY}"


@app.route('/')
def home():
    return render_template("1_mainPage.html")

@app.route('/input')
def input_page():
    return render_template("2_InputPage.html")

@app.route('/results')
def results_page():
    return render_template("3_ResultPage.html", value1=latest_predicted_state, value2=latest_suggestion_text)




@app.route('/submit', methods=['POST'])
def handle_submission():
    global latest_predicted_state, latest_suggestion_text
    data = request.get_json()

    print("Received submission:", data)

    with sqlite3.connect("User_Data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO data (
                user, emotional_state, sunlight_hours, safety, sleep_duration_hours,
                screen_time_minutes, physical_activity_minutes, hour, weekday
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "default_user",
            None,
            data.get("sunlight"),
            data.get("safety"),
            data.get("sleep_duration"),
            data.get("screen"),
            data.get("activity"),
            data.get("hour"),
            data.get("weekday")
        ))
        conn.commit()

    latest_data = {
        "sleep_duration_hours": float(data.get("sleep_duration", 0)),
        "screen_time_minutes": int(data.get("screen", 0)),
        "physical_activity_minutes": int(data.get("activity", 0)),
        "hour": int(data.get("hours", 0)),
        "weekday": int(data.get("weekday", 0)),
        "sunlight_hours": int(data.get("sunlight", 0)),
        "safety": int(data.get("safety", 0)),
        "daily_goal_progression": int(data.get("goals", 0))
    }

    if latest_data:
        predicted_state = get_mental_state(latest_data)
        suggestion_text = generate_suggestions("No message provided", predicted_state, latest_data)

        # Store for result page
        latest_predicted_state = predicted_state
        latest_suggestion_text = suggestion_text

        # Generate summary
        summary_prompt = (
            f"As NeuroGuard, summarise the following AI mental wellness advice into one short paragraph "
            f"that can be stored as historical context for future use:\n\n{suggestion_text}\n"
            "Only return the summary without any intro or title."
        )

        summary_response = requests.post(
            GEMINI_API_URL,
            headers={"Content-Type": "application/json"},
            json={"contents": [{"parts": [{"text": summary_prompt}]}]}
        )

        if summary_response.status_code == 200:
            summary_result = summary_response.json()
            summary_text = summary_result['candidates'][0]['content']['parts'][0]['text']
        else:
            summary_text = "Summary generation failed."

        update_latest_row(predicted_state, summary_text)

    print("Passing to results page:", latest_predicted_state, latest_suggestion_text)
    # time.sleep(4)
    return redirect(url_for('results_page', predicted=latest_predicted_state, suggestion=latest_suggestion_text))

def get_full_history():
    with sqlite3.connect("User_Data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT previous_suggestion FROM data WHERE previous_suggestion IS NOT NULL")
        rows = cursor.fetchall()
        return "\n- ".join([row[0] for row in rows if row[0]])


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
            "daily_goal_progression": 50  # Placeholder to satisfy expected columns
        }


def update_latest_row(mental_state, summary_text):
    with sqlite3.connect("User_Data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM data ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        if row:
            latest_id = row[0]
            cursor.execute(
                "UPDATE data SET emotional_state = ?, previous_suggestion = ? WHERE id = ?",
                (mental_state, summary_text.strip(), latest_id)
            )
            conn.commit()


def generate_suggestions(user_message, mental_state, user_data, history_text=""):
    prompt = (
        f"You are NeuroGuard, an advanced mental wellness AI from the year 2080.\n"
        f"Your top priority is to respond meaningfully to the user's emotional input.\n\n"
        f"User's message (primary focus): \"{user_message}\"\n\n"
        f"Contextual lifestyle data:\n"
        f"- Estimated mental state score: {mental_state}/100\n"
        f"- Weekday: {user_data.get('weekday')}\n"
        f"- Hours of sleep: {user_data.get('sleep_duration_hours')}h\n"
        f"- Screen time: {user_data.get('screen_time_minutes')} minutes\n"
        f"- Physical activity: {user_data.get('physical_activity_minutes')} minutes\n"
        f"- Safety perception: {user_data.get('safety')}/100\n"
        f"- Sunlight exposure: {user_data.get('sunlight_hours')} hours\n"
    )

    history_section = f"\n\nHere is the user's historical wellness advice:\n- {history_text}" if history_text else ""
    prompt += history_section + "\n\n" \
              "Based on the emotional input and context, offer exactly **three personalised tips** to help the user improve or stabilise their mental well-being.\n" \
              "Each suggestion must be:\n" \
              "- Psychologically sound and empathetic\n" \
              "- Inspired by mindfulness, behavioural science, or neuroscience\n" \
              "- Practical, concise, and immediately useful\n\n" \
              "Respond with a numbered list. Avoid greetings, introductions, or summaries. Use British spelling."

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
    # subprocess.Popen(["/usr/bin/python3", "web_data_receiver.py"])
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
                history_text = get_full_history()
                suggestion_text = generate_suggestions("No message provided", predicted_state, latest_data, history_text)
                print("AI Suggestions:\n", suggestion_text)


                # Generate a concise summary of today's suggestion
                summary_prompt = (
                    f"As NeuroGuard, summarise the following AI mental wellness advice into one short paragraph "
                    f"that can be stored as historical context for future use:\n\n{suggestion_text}\n"
                    "Only return the summary without any intro or title."
                )

                summary_response = requests.post(
                    GEMINI_API_URL,
                    headers={"Content-Type": "application/json"},
                    json={"contents": [{"parts": [{"text": summary_prompt}]}]}
                )

                if summary_response.status_code == 200:
                    summary_result = summary_response.json()
                    summary_text = summary_result['candidates'][0]['content']['parts'][0]['text']
                else:
                    summary_text = "Summary generation failed."

                # Update the row
                update_latest_row(predicted_state, summary_text)

                # Print the summary
                print("Summary stored in history:")
                print(summary_text)

                # Display full table
                print("\nCurrent data table:")
                with sqlite3.connect("User_Data.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM data")
                    for row in cursor.fetchall():
                        print(row)

                last_seen_id = current_id
            sleep(2)

def run_flask():
    app.run(debug=True, port=4000, use_reloader=False)

if __name__ == "__main__":
    from multiprocessing import Process
    flask_process = Process(target=run_flask)
    flask_process.start()
    main()

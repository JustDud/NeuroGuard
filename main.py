from dotenv import load_dotenv
import os
import requests
from ml import get_mental_state, retrain_model, MODEL_PATH

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={GEMINI_API_KEY}"


def generate_suggestions(user_message, mental_state, user_data):
    prompt = (
        f"The user's current mental state is: '{mental_state}'.\n"
        f"They have reported feeling: \"{user_message}\"\n\n"
        f"Additional context:\n"
        f"- Day of the week: {user_data.get('weekday')}\n"
        f"- Hours of sleep: {user_data.get('sleep_duration_hours')}h\n"
        f"- Screen time: {user_data.get('screen_time_minutes')} minutes\n"
        f"- Physical activity: {user_data.get('physical_activity_minutes')} minutes\n"
        f"- Goal progress: {user_data.get('daily_goal_progression')}%\n"
        f"- Safety level: {user_data.get('safety')}/100\n"
        f"- Sunlight exposure: {user_data.get('sunlight_hours')} hours\n\n"
        "As an intelligent and empathetic wellness assistant from the year 2080, use this information to offer guidance.\n"
        "Your task is to generate exactly **three personalised suggestions** that are:\n"
        "- Calm, practical, and emotionally supportive\n"
        "- Inspired by modern neuroscience, mindfulness, or behavioural psychology\n"
        "- Focused on small steps the user can take right now to improve their mental well-being\n\n"
        "Format your response as a concise, friendly list."
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

    user_data = {
        "sunlight_hours": 12,
        "safety": 75,
        "sleep_duration_hours": 7.5,
        "screen_time_minutes": 320,
        "physical_activity_minutes": 45,
        "daily_goal_progression": 80,
        "hour": 14,
        "weekday": 2
    }
    user_message = "I'm feeling like I can't focus on anything today."

    mental_state = get_mental_state(user_data)

    suggestions = generate_suggestions(user_message, mental_state, user_data)
    print("\nHere are some suggestions for you:\n")
    print(mental_state)
    print(suggestions)


if __name__ == "__main__":
    main()

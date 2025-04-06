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

    # user_data = {"sunlight_hours": 6, "safety": 31, "sleep_duration_hours": 4.3, "screen_time_minutes": 447, "physical_activity_minutes": 35, "daily_goal_progression": 58, "hour": 8, "weekday": 1}
    #
    # user_message = "I'm feeling like I can't focus on anything today."
    #
    # mental_state = get_mental_state(user_data)

    test_inputs = [
        {"sunlight_hours": 6, "safety": 31, "sleep_duration_hours": 4.3, "screen_time_minutes": 447,
         "physical_activity_minutes": 35, "daily_goal_progression": 58, "hour": 8, "weekday": 1},
        {"sunlight_hours": 10, "safety": 99, "sleep_duration_hours": 3.2, "screen_time_minutes": 443,
         "physical_activity_minutes": 111, "daily_goal_progression": 89, "hour": 7, "weekday": 3},
        {"sunlight_hours": 5, "safety": 47, "sleep_duration_hours": 9.1, "screen_time_minutes": 624,
         "physical_activity_minutes": 97, "daily_goal_progression": 77, "hour": 8, "weekday": 4},
        {"sunlight_hours": 7, "safety": 25, "sleep_duration_hours": 8.7, "screen_time_minutes": 608,
         "physical_activity_minutes": 109, "daily_goal_progression": 67, "hour": 19, "weekday": 4},
        {"sunlight_hours": 7, "safety": 78, "sleep_duration_hours": 8.9, "screen_time_minutes": 211,
         "physical_activity_minutes": 89, "daily_goal_progression": 77, "hour": 12, "weekday": 5},
        {"sunlight_hours": 5, "safety": 78, "sleep_duration_hours": 4.1, "screen_time_minutes": 782,
         "physical_activity_minutes": 3, "daily_goal_progression": 83, "hour": 18, "weekday": 0},
        {"sunlight_hours": 5, "safety": 58, "sleep_duration_hours": 8.4, "screen_time_minutes": 801,
         "physical_activity_minutes": 69, "daily_goal_progression": 35, "hour": 4, "weekday": 1},
        {"sunlight_hours": 2, "safety": 91, "sleep_duration_hours": 6.8, "screen_time_minutes": 841,
         "physical_activity_minutes": 67, "daily_goal_progression": 63, "hour": 1, "weekday": 1},
        {"sunlight_hours": 5, "safety": 51, "sleep_duration_hours": 9.0, "screen_time_minutes": 725,
         "physical_activity_minutes": 93, "daily_goal_progression": 10, "hour": 17, "weekday": 4},
        {"sunlight_hours": 5, "safety": 56, "sleep_duration_hours": 5.5, "screen_time_minutes": 354,
         "physical_activity_minutes": 43, "daily_goal_progression": 70, "hour": 10, "weekday": 5}
    ]


    for i, input_data in enumerate(test_inputs, 1):
        result = get_mental_state(input_data)
        print(f"{i}. Predicted mental_state: {result}")

    # suggestions = generate_suggestions(user_message, mental_state, user_data)
    # print("\nHere are some suggestions for you:\n")
    # print(mental_state)
    # print(suggestions)


if __name__ == "__main__":
    main()

from dotenv import load_dotenv
import os
import requests

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={GEMINI_API_KEY}"

def generate_suggestions(user_message):
    prompt = (
        f'The user has expressed that they are feeling: "{user_message}".\n\n'
        'As an intelligent mental wellness assistant in the year 2080, your role is to provide calm, practical, and emotionally intelligent suggestions that help the user restore balance, feel supported, and take small steps forward.\n\n'
        'Please suggest exactly **three helpful actions** they can take right now to improve their mental well-being. These should be:\n'
        '- Simple and realistic\n'
        '- Supportive in tone (not robotic or generic)\n'
        '- Based on modern neuroscience, mindfulness, or behavioural science (but in plain language)\n\n'
        'Format the answer as a short list.'
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
    user_message = input("How are you feeling today? ")
    suggestions = generate_suggestions(user_message)
    print("\nHere are some suggestions for you:\n")
    print(suggestions)


if __name__ == "__main__":
    main()

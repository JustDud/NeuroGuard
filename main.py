from dotenv import load_dotenv
import os
import requests

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={GEMINI_API_KEY}"

def generate_suggestions(user_message):
    prompt = f'Suggest 3 helpful actions for someone feeling: "{user_message}"'

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






import vertexai

# from google.cloud import language_v1
from vertexai.preview.generative_models import GenerativeModel
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
# project_id = os.getenv("PROJECT_ID")

# vertexai.init(project=project_id, location="us-central1")



# def analyse_sentiment(text):
#     client = language_v1.LanguageServiceClient()
#     document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
#     response = client.analyze_sentiment(document=document)
#     sentiment = response.document_sentiment
#     return {"score": sentiment.score, "magnitude": sentiment.magnitude}

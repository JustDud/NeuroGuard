# import google.generativeai as genai
# import os
# from dotenv import load_dotenv
#
# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")
#
# genai.configure(api_key=api_key)
#
# model = genai.GenerativeModel("gemini-pro")  # or "gemini-pro-vision" if multimodal
#
# response = model.generate_content("Explain how AI works")
#
# print(response.text)

import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

response = requests.get(url)

if response.status_code == 200:
    models = response.json().get("models", [])
    print("Available models for your API key:\n")
    for m in models:
        print(f"- {m['name']}")
else:
    print(f"❌ Error {response.status_code}:\n{response.text}")
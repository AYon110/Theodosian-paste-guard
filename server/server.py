import os
import json
from dotenv import load_dotenv
from google import genai
from flask import Flask, request, jsonify
from flask_cors import CORS

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)
CORS(app)

PROMPT = """

You are a data leak detector, an expert in cyber security.
Your role is to detect sensitive information
this includes:
names of private individuals, email addresses, phone numbers
confidential work info e.g salaries, internal projects, internal documents, internal code, internal tools
Passwords, API keys, secret keys, private keys, access tokens, session tokens
Financial information, credit card numbers, bank account numbers, routing numbers
THIS IS NOT AN EXHAUSTIVE LIST, if you detect any sensitive information that is not listed above, you should still flag it as sensitive information.

Non sensitive information includes: publicly available information, information that is not private or confidential, information that is not sensitive in nature.
general knowledge

ALWAYS reply with ONLY this JSON, even if nothing is found:
{"is_sensitive": true or false, "items": ["..."], "reason": "..."}

Copy each item EXACTLY as it appears in the text.
If nothing is sensitive, use "is_sensitive": false and "items": [].


"""


gemini_test = "Bill Gates is attending harvard university, his email address is billgates@gmail.com"

actual_msg = PROMPT + "\nTExt to check:\n " + gemini_test

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents = actual_msg,
    config = {"response_mime_type": "application/json"}
)

result = json.loads(response.text)

print("Sensitive?", result["is_sensitive"])
print("Items:", result["items"])
print("reasoning:", result["reason"])


import os
import json
from dotenv import load_dotenv
from google import genai
from flask import Flask, request, jsonify
from flask_cors import CORS

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)
CORS(app)   # lets the extension talk to this server

PROMPT = """
You are a data leak detector, an expert in cyber security.
Your role is to detect sensitive information in pasted text.
This includes:
- names of private individuals, email addresses, phone numbers
- confidential work info e.g. salaries, layoffs, internal projects, internal documents, internal code, internal tools
- passwords, API keys, secret keys, private keys, access tokens, session tokens
- financial information, credit card numbers, bank account numbers
- private health information
THIS IS NOT AN EXHAUSTIVE LIST. If you detect any other sensitive information, flag it too.

Non-sensitive information includes: publicly available information, public figures, general knowledge, normal questions.

ALWAYS reply with ONLY this JSON, even if nothing is found:
{"is_sensitive": true or false, "items": ["..."], "reason": "..."}

Each item must be a plain string copied EXACTLY as it appears in the text.
If nothing is sensitive, use "is_sensitive": false and "items": [].
"""

def check_text(text):
    full_message = PROMPT + "\n\nText to check:\n" + text
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=full_message,
        config={"response_mime_type": "application/json"},
    )
    result = json.loads(response.text)
    return result


   

@app.route("/check", methods=["POST"])
def check():
    text = request.get_json().get("text", "")
    try:
        result = check_text(text)
    except Exception as e:
        # case: gemini servers r overloaded
        result = {"is_sensitive": False, "items": [], "reason": "AI check unavailable: " + str(e)}
    return jsonify(result)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
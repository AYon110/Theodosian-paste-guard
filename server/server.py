

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
...paste your prompt here...
"""

def check_text(text):
    full_message = PROMPT + "\n\nText to check:\n" + text
    response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents = full_message,
    config = {"response_mime_type": "application/json"}
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
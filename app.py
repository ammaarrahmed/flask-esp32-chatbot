from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Load your API keys from environment variables
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
ESP32_SECRET_KEY = os.environ.get("ESP32_SECRET_KEY")  # ✅ Add this in Render

@app.route('/')
def home():
    return "ESP32 chatbot is alive!"

@app.route('/chat', methods=['POST'])
def chat():
    # 🔐 Require API key
    client_key = request.headers.get("X-API-KEY")
    if client_key != ESP32_SECRET_KEY:
        abort(401, description="Unauthorized: Invalid API Key")

    # 📥 Get user message
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # 📡 Prepare OpenRouter API call
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "yourdomain.com",
        "X-Title": "ESP32 Bot"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "You are a sassy assistant."},
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions",
                             headers=headers, json=data)

    try:
        bot_reply = response.json()['choices'][0]['message']['content']
    except Exception as e:
        return jsonify({
            "error": "API error",
            "details": response.text,
            "exception": str(e)
        }), 500

    return jsonify({"reply": bot_reply})

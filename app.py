from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace with your OpenRouter API key
OPENROUTER_API_KEY = "your-api-key-here"

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

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

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    try:
        bot_reply = response.json()['choices'][0]['message']['content']
    except:
        return jsonify({"error": "API error", "details": response.text}), 500

    return jsonify({"reply": bot_reply})

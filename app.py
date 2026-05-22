from flask import Flask, render_template, request, jsonify
from google import genai
import os

app = Flask(__name__)

# This connects your app to Google's Gemini AI brain
api_key = os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY")
client = genai.Client(api_key=api_key)

@app.route('/')
def home():
    # This tells the server to load your dashboard webpage
    return render_template('index.html')

@app.route('/ask_ai', methods=['POST'])
def ask_ai():
    data = request.json
    user_message = data.get('message', '')
    mode = data.get('mode', 'chat')
    
    student_class = data.get('student_class', 'General')
    board = data.get('board', 'CBSE')
    stream = data.get('stream', 'General')

    # This sets the rules for Gemini based on what the student chooses
    if mode == 'chat':
        system_prompt = f"You are an expert AI Tutor helping a {student_class} student ({board} board, {stream} stream)."
    elif mode == 'calculator':
        system_prompt = f"You are a step-by-step math solver for a {student_class} student."
    elif mode == 'translator':
        target_lang = data.get('target_lang', 'Hindi')
        system_prompt = f"Translate this text into {target_lang} for a student."
    else:
        system_prompt = "You are a helpful AI study assistant."

    try:
        # Sending the student's question to Gemini
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
            config={'system_instruction': system_prompt}
        )
        return jsonify({'reply': response.text})
    except Exception as e:
        return jsonify({'reply': "API Key error. We will fix this next!"})

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, jsonify
from google import genai
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask_ai', methods=['POST'])
def ask_ai():
    data = request.json or {}
    user_message = data.get('message', '').strip()
    mode = data.get('mode', 'chat')
    user_api_key = data.get('api_key', '').strip()
    
    # 1. Answer Identity Question First
    if any(phrase in user_message.lower() for phrase in ["who made you", "who created you", "who is your developer"]):
        return jsonify({'reply': "I was created by Mr. Aman Sardare."})

    # 2. API Key Security Check
    if not user_api_key:
        return jsonify({'reply': "❌ API Error: Please enter your Gemini API Key in the top box."})

    # 3. Centralized Prompt Map for all 20 modes
    prompts = {
        'chat': "You are an expert AI Tutor.",
        'calculator': "You are a step-by-step math/science solver.",
        'translator': f"Translate the text into {data.get('target_lang', 'Hindi')}.",
        'test': "Generate a mock exam or past-year question.",
        'notes': "Convert the text into structured, clean bullet-point notes.",
        'visuals': "Create conceptual ASCII flowcharts or diagrams.",
        'flashcards': "Generate study flashcards in FRONT/BACK format.",
        'planner': "Create an optimized, actionable study timetable.",
        'eli5': "Explain the topic like I am 5 years old using fun analogies.",
        'debate': "Act as a critical thinking debate partner and challenge the student's views.",
        'memory': "Create a vivid 'Memory Palace' narrative to help memorize these facts.",
        'simulator': "Act as a strict, high-stakes exam invigilator and ask a challenge question.",
        'career': "Act as a professional career counselor and provide roadmap advice.",
        'grader': "Grade the student's answer out of 10 and provide specific technical corrections.",
        'cheatsheet': "Extract all critical formulas and core laws into a dense cheat sheet.",
        'popculture': "Explain the academic topic using fun analogies from movies, anime, or games.",
        'break': "Provide a 1-minute mindfulness activity, fun riddle, or brain teaser.",
        'voice': "Provide a friendly, conversational educational response.",
        'scanner': "Analyze the provided text and solve the problem step-by-step."
    }

    system_prompt = prompts.get(mode, "You are a helpful study assistant.")

    # 4. Generate AI Response
    try:
        client = genai.Client(api_key=user_api_key)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
            config={'system_instruction': system_prompt}
        )
        return jsonify({'reply': response.text})
    except Exception as e:
        return jsonify({'reply': f"❌ API Error: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

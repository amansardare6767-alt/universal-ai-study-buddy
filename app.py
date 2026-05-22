from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask_ai', methods=['POST'])
def ask_ai():
    try:
        data = request.get_json()
        message = data.get('message', '')
        mode = data.get('mode', 'chat')
        api_key = data.get('api_key', '')
        target_lang = data.get('target_lang', 'Hindi')

        # CREATOR CHECK
        lower_msg = message.lower().strip()
        creator_questions = ["who made you", "who created you", "who developed you", "who is your creator", "who owns you"]
        
        if any(q in lower_msg for q in creator_questions):
            return jsonify({"reply": "🌸 I was created and developed by Mr. Aman Sardare. He built this AI Study Hub for students."})

        if not api_key:
            return jsonify({"reply": "❌ Please enter your Gemini API Key in the top bar."})

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        prompts = {
            "chat": "You are a humble and helpful AI tutor.",
            "calculator": "Solve maths step-by-step.",
            "translator": f"Translate into {target_lang}.",
            "test": "Create mock exam with answers.",
            "notes": "Create structured notes.",
            "visuals": "Create ASCII visuals.",
            "flashcards": "Create flashcards.",
            "planner": "Create study timetable.",
            "eli5": "Explain very simply.",
            "debate": "Act as debate partner.",
            "memory": "Create memory tricks.",
            "simulator": "Act as exam simulator.",
            "career": "Give career guidance.",
            "grader": "Grade answer out of 10.",
            "cheatsheet": "Create cheat sheet.",
            "popculture": "Explain with pop culture.",
            "break": "Give mindfulness exercise.",
            "voice": "Talk conversationally.",
            "scanner": "Analyze and solve carefully."
        }

        system_prompt = prompts.get(mode, "You are a helpful AI assistant.")
        final_prompt = f"SYSTEM: {system_prompt}\n\nUSER: {message}"

        response = model.generate_content(final_prompt)
        return jsonify({"reply": response.text})

    except Exception as e:
        return jsonify({"reply": f"❌ Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)

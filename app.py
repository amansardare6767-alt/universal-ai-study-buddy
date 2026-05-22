from flask import Flask, render_template, request, jsonify
from google import genai

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

        if not api_key:
            return jsonify({
                "reply":"❌ Please Enter Gemini API Key"
            })

        prompts = {

            "chat":"You are an advanced AI tutor for students.",

            "calculator":"Solve maths step-by-step with explanations.",

            "translator":f"Translate into {target_lang}.",

            "test":"Create a professional mock test with answers.",

            "notes":"Convert into structured notes with headings.",

            "visuals":"Create ASCII diagrams and charts.",

            "flashcards":"Create study flashcards.",

            "planner":"Create a study timetable.",

            "eli5":"Explain very simply for kids.",

            "debate":"Act like a debate partner.",

            "memory":"Create memory palace tricks.",

            "simulator":"Act as exam simulator.",

            "career":"Give professional career guidance.",

            "grader":"Grade answers out of 10 with feedback.",

            "cheatsheet":"Create a compact cheat sheet.",

            "popculture":"Explain using movies and pop culture.",

            "break":"Give mindfulness and focus exercise.",

            "voice":"Talk conversationally.",

            "scanner":"Analyze and solve the problem."
        }

        system_prompt = prompts.get(mode)

        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(

            model="gemini-2.5-flash",

            contents=f"""
            SYSTEM:
            {system_prompt}

            USER:
            {message}
            """
        )

        return jsonify({
            "reply":response.text
        })

    except Exception as e:

        return jsonify({
            "reply":f"❌ Error: {str(e)}"
        })

if __name__ == "__main__":
    app.run(debug=True)

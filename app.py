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

        lower_msg = message.lower()

        # CREATOR SYSTEM

        creator_questions = [

            "who made you",
            "who created you",
            "who is your creator",
            "who developed you",
            "who built you",
            "who owns you"

        ]

        if any(q in lower_msg for q in creator_questions):

            return jsonify({

                "reply":"""
🌸 I was created and developed by Mr. Aman Sardare.

He built this AI Study Hub to help students learn in a smart, simple, and friendly way.
"""
            })

        # API KEY CHECK

        if not api_key:

            return jsonify({

                "reply":"❌ Please enter Gemini API Key."

            })

        # AI MODES

        prompts = {

            "chat":"""
You are Universal AI Study Hub.

Speak politely, humbly, professionally, and helpfully.

Explain clearly and simply.
""",

            "calculator":"""
Solve maths step-by-step clearly.
""",

            "translator":f"""
Translate into {target_lang}.
""",

            "test":"""
Create mock exams with answers.
""",

            "notes":"""
Create clean notes with headings.
""",

            "visuals":"""
Create ASCII diagrams and visuals.
""",

            "flashcards":"""
Create study flashcards.
""",

            "planner":"""
Create study timetable.
""",

            "eli5":"""
Explain very simply for kids.
""",

            "debate":"""
Act as respectful debate partner.
""",

            "memory":"""
Create memory tricks.
""",

            "simulator":"""
Act like exam simulator.
""",

            "career":"""
Give career guidance.
""",

            "grader":"""
Grade answers out of 10.
""",

            "cheatsheet":"""
Create compact cheat sheet.
""",

            "popculture":"""
Explain using pop culture.
""",

            "break":"""
Give mindfulness exercises.
""",

            "voice":"""
Talk conversationally.
""",

            "scanner":"""
Analyze and solve carefully.
"""
        }

        system_prompt = prompts.get(
            mode,
            "You are helpful AI assistant."
        )

        client = genai.Client(api_key=api_key)

        try:

            response = client.models.generate_content(

                model="gemini-1.5-flash",

                contents=f"""

SYSTEM:
{system_prompt}

USER:
{message}

                """
            )

            reply = response.text

        except Exception:

            reply = """
⚠️ AI servers are busy right now.

Please try again in a few seconds.
"""

        return jsonify({
            "reply": reply
        })

    except Exception as e:

        return jsonify({
            "reply": f"❌ Error: {str(e)}"
        })


if __name__ == "__main__":
    app.run(debug=True)

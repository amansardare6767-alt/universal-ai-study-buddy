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

        # CREATOR QUESTIONS

        lower_msg = message.lower()

        creator_questions = [

            "who made you",
            "who created you",
            "who developed you",
            "who is your creator",
            "who owns you"

        ]

        if any(q in lower_msg for q in creator_questions):

            return jsonify({

                "reply":"""
🌸 I was created and developed by Mr. Aman Sardare.

He built this AI Study Hub for students.
"""
            })

        # CHECK API KEY

        if not api_key:

            return jsonify({

                "reply":"❌ Please enter Gemini API Key."

            })

        # CONFIGURE GEMINI

        genai.configure(api_key=api_key)

        model = genai.GenerativeModel('gemini-1.5-flash')

        # AI MODES

        prompts = {

            "chat":"You are a humble and helpful AI tutor.",

            "calculator":"Solve maths step-by-step.",

            "translator":f"Translate into {target_lang}.",

            "test":"Create mock exam with answers.",

            "notes":"Create structured notes.",

            "visuals":"Create ASCII visuals.",

            "flashcards":"Create flashcards.",

            "planner":"Create study timetable.",

            "eli5":"Explain very simply.",

            "debate":"Act as debate partner.",

            "memory":"Create memory tricks.",

            "simulator":"Act as exam simulator.",

            "career":"Give career guidance.",

            "grader":"Grade answer out of 10.",

            "cheatsheet":"Create cheat sheet.",

            "popculture":"Explain with pop culture.",

            "break":"Give mindfulness exercise.",

            "voice":"Talk conversationally.",

            "scanner":"Analyze and solve carefully."
        }

        system_prompt = prompts.get(
            mode,
            "You are helpful AI assistant."
        )

        final_prompt = f"""

SYSTEM:
{system_prompt}

USER:
{message}

"""

        try:

            response = model.generate_content(final_prompt)

            reply = response.text

        except Exception:

            reply = """
⚠️ AI servers are busy right now.

Please try again later.
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

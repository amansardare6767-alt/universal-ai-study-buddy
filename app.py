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
    
    # 🔑 Read the API key sent dynamically from the user's browser input
    user_api_key = data.get('api_key', '').strip()
    
    # Fallback to backend environment variable if user didn't provide one
    final_api_key = user_api_key if user_api_key else os.environ.get("GEMINI_API_KEY", "")

    if not final_api_key:
        return jsonify({'reply': "⚠️ No API Key found! Please follow the instruction guide at the top of the page to generate your free Gemini API Key, paste it in, and start learning."})

    student_class = data.get('student_class', 'General')
    board = data.get('board', 'CBSE')
    stream = data.get('stream', 'General')

    # 🍀 SECRET EASTER EGG: Lucky Number 46
    if user_message == "46":
        return jsonify({'reply': "🌟 46 Detected! You've unlocked the Developer's Lucky Streak! Your learning journey is blessed with maximum focus and cosmic success today. 🚀"})

    # Instruction sets for all 20 distinct modes
    if mode == 'chat':
        system_prompt = f"You are an expert AI Tutor helping a {student_class} student ({board} board, {stream} stream). Answer clearly with relevant academic depth."
    elif mode == 'calculator':
        system_prompt = f"You are a step-by-step math and science equation solver for a {student_class} student. Break down formulas beautifully."
    elif mode == 'translator':
        target_lang = data.get('target_lang', 'Hindi')
        system_prompt = f"Translate this text into clear, easy-to-understand {target_lang} for educational purposes."
    elif mode == 'test':
        system_prompt = f"Generate a mock exam question or past-year question (PYQ) appropriate for a {student_class} ({board} board, {stream} stream) student. Include options and a hidden explanation."
    elif mode == 'notes':
        system_prompt = f"Convert the textbook chapter or concept provided into neat bullet points, core definitions, and quick summaries for a {student_class} student."
    elif mode == 'visuals':
        system_prompt = "Create a conceptual layout or flowchart map using clear ASCII text arrows (-->) or tiered bullet structures to show how a process works."
    elif mode == 'flashcards':
        system_prompt = f"Generate 3-5 study flashcards for a {student_class} student based on the topic. Format each clearly as: FRONT: (Question) | BACK: (Answer)."
    elif mode == 'planner':
        system_prompt = f"You are an expert academic counselor. Create a highly optimized study timetable or strategy planner for a {student_class} student based on their input goal."
    elif mode == 'eli5':
        system_prompt = f"Explain the topic provided like I am 5 years old. Use highly creative, fun analogies, stories, and simple concepts that even a preschooler or young child could grasp."
    elif mode == 'debate':
        system_prompt = f"Take an opposing, argumentative academic view on the student's topic to challenge a {student_class} student's critical reasoning skills. Keep it balanced and pedagogical."
    elif mode == 'memory':
        system_prompt = f"Convert the raw list of elements or facts provided into a creative, descriptive 'Memory Palace' room journey narrative to help a {student_class} student memorize them effortlessly."
    elif mode == 'simulator':
        system_prompt = f"Act as a strict exam invigilator. Give a high-stakes, quick, single test question matching the {student_class} level. Grade inputs strictly out of 100%."
    elif mode == 'career':
        system_prompt = f"Act as an elite career mentor. Analyze the student's preferences and provide strategic career pathways and subject choices suited for a {student_class} context."
    elif mode == 'grader':
        system_prompt = f"Act as an official board examiner. Grade the student's answer out of 10, list technical errors, and write an improved model answer for a {student_class} standard."
    elif mode == 'cheatsheet':
        system_prompt = f"Extract all critical formulas, core laws, definitions, and key reactions into an ultra-dense, clean cheat sheet text layout for a {student_class} student."
    elif mode == 'popculture':
        system_prompt = f"Explain this academic concept entirely using analogies from popular movies, cartoons, superheroes, video games, or anime to keep a {student_class} student completely engaged."
    elif mode == 'break':
        system_prompt = "Act as a mental health and study mindfulness coach. Provide a fun 1-minute brain teaser riddle, a quick logic game, or a grounding deep breathing layout routine."
    else:
        system_prompt = "You are a helpful AI study assistant."

    try:
        client = genai.Client(api_key=final_api_key)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
            config={'system_instruction': system_prompt}
        )
        return jsonify({'reply': response.text})
    except Exception as e:
        return jsonify({'reply': "❌ API Connection Error. Please verify that the Gemini API key you provided is valid and active!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

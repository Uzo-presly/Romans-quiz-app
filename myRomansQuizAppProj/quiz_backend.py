# quiz_backend.py
from flask import Flask, render_template, request, redirect, url_for
from send_result_email import send_email
from log_to_sheet import log_to_sheet
from dotenv import load_dotenv
from datetime import datetime
import os
import re

try:
    # ✅ For Render or gunicorn deployment
    from myRomansQuizAppProj.models import Session, Question, UserAttempt
except ModuleNotFoundError:
    # ✅ For local testing
    from models import Session, Question, UserAttempt

load_dotenv()
app = Flask(__name__)

@app.route("/")
def home():
    return redirect(url_for("quiz"))  # Redirect to quiz page

@app.route("/quiz", methods=["GET"])
def quiz():
    session = Session()
    questions = session.query(Question).all()
    return render_template("quiz.html", questions=questions)

@app.route("/submit", methods=["POST"])
def submit_quiz():
    session = Session()

    # 🛡️ Step 1: Validate and sanitize email input
    email = request.form.get("email")
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return "❌ Invalid email format", 400

    questions = session.query(Question).all()
    score = 0
    total = 0

    # ✅ Extract contextual info
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip_address = request.remote_addr or "Unknown IP"
    browser_info = request.user_agent.string or request.headers.get('User-Agent', "Unknown browser")

    feedback = f"Hello dear,\n\nYou took the Romans Chapter 2 Quiz.\n📅 Date/Time: {timestamp}\n"
    result_details = ""

    for index, q in enumerate(questions, start=1):
        user_answer = request.form.get(f"question_{q.id}")
        if user_answer is not None:
            total += 1
            user_answer_int = int(user_answer)
            user_answer_text = getattr(q, f"option_{user_answer_int}")
            correct_answer_text = getattr(q, f"option_{q.correct}")

            result_details += f"Q{index}. {q.prompt}\n"
            result_details += f"Your answer: {user_answer_text} "
            if user_answer_int == q.correct:
                score += 1
                result_details += "✅\n\n"
            else:
                result_details += f"❌\nCorrect answer: {correct_answer_text}\n\n"

    # Save attempt to DB
    attempt = UserAttempt(email=email, score=score)
    session.add(attempt)
    session.commit()

    # ✅ Correct: Call log_to_sheet with all arguments in correct order
    try:
        log_to_sheet(timestamp, ip_address, email, score, total, browser_info)
        print("✅ Logged to Google Sheets.")
    except Exception as e:
        print("❌ Failed to log to Sheets:", e)

    # 📩 Final feedback message
    feedback += f"\n📊 You scored {score} out of {total}.\n\n📝 Results:\n{result_details}"
    feedback += "\n📖 Let reading God's Word—the holy Bible—be your daily experience.\n(Psalm 1:1–3)\n\n🙏 Thanks for taking the quiz!"

    try:
        send_email(email, "Your Romans chapter 2 Quiz Result", feedback)
        print("✅ Email sent successfully.")
    except Exception as e:
        print("❌ Failed to send email:", e)

    return f"<pre>{feedback}</pre>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

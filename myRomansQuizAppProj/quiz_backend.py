from flask import Flask, render_template, request
from models import Session, Question, UserAttempt
from send_result_email import send_email
from dotenv import load_dotenv
from markupsafe import escape
import re
import os

load_dotenv()
app = Flask(__name__)

@app.route("/")
def quiz_form():
    session = Session()
    questions = session.query(Question).all()
    return render_template("quiz.html", questions=questions)


#@app.route("/submit", methods=["POST"])
#def submit_quiz():
 #   session = Session()
  #  email = request.form.get("email")

    # 🚫 Check if this email has already submitted
   # if session.query(UserAttempt).filter_by(email=email).first():
    #    return f"<h2>{email}, you have already submitted the quiz. Only one attempt is allowed.</h2>"

    # ✅ Proceed with submission
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
    # 📩 This will hold the full feedback for email and browser
    feedback = f"Hello dear,\n\nYou took the Romans Chapter 2 Quiz.\n\n"
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

    # Save to DB
    attempt = UserAttempt(email=email, score=score)
    session.add(attempt)
    session.commit()

    # Final message
    feedback += f"You scored {score} out of {total}.\n\nResults:\n{result_details}"
    feedback += "Oh let reading God's word-the holy Bible, be your daily experience\n\n"
    feedback += "(Psalms 1:1-3) Thanks for taking the quiz!"


    # Send email
    try:
        send_email(email, "Your Romans chapter 2 Quiz Result", feedback)
        print("✅ Email sent successfully.")
    except Exception as e:
        print("❌ Failed to send email:", e)

    # Return message in browser too (for user to see immediately)
    return f"<pre>{feedback}</pre>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

# 📖 Bible Quiz App (Romans 2)

A simple interactive Bible quiz built with Flask, SQLite, and Bootstrap. Focuses on Romans Chapter 2.

## 🌟 Features

- Dynamic quiz questions from database
- Email results to users using SMTP
- Stores attempts in SQLite DB
- Timer countdown (4 mins)
- Bootstrap styled layout

## 🚀 Run Locally

```bash
git clone https://github.com/yourusername/bible-quiz-app.git
cd bible-quiz-app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python quiz_backend.py


As much as possible, Uzo you want to avoid putting comments in html page to avoid reading error from flask.
This is a major step into full-stack web development! Let’s take it one solid piece at a time.
🔍 First: What Does "Modularize" Mean?

Modularizing means splitting your project into separate files (modules) based on responsibility.
✅ Benefits:

    Easy to maintain or replace one part (e.g., email logic) without affecting others.

    Cleaner, readable, and scalable structure.

    Encourages reuse (e.g., same email logic in other projects).

📦 In Our Case:
File	Responsibility
quiz_backend.py	Flask app (web server, routes)
send_result_email.py	Handles all email sending logic
templates/	Contains HTML files (frontend)
models.py (new)	Handles database and quiz logic
🔍 Now: What Does "Integrating Into a Database" Mean?

Instead of hardcoding one question in Python like:

correct_answer = "Python"

We now store multiple quiz questions and answers in a real database — e.g., SQLite.

Flask + SQLAlchemy lets us:

    Save questions

    Retrieve them

    Save each user's score & email

    Later even show a leaderboard!
first make sure to install sqlalchemy with pip install sqlalchemy before freezing requirement.txt

🧱 Tech Stack We're Using
Tool	Purpose
Flask	Web server
SQLite	Lightweight database (already in Python)
SQLAlchemy	Python ORM (Object Relational Mapper)
Jinja2	HTML rendering engine
python-dotenv	To keep passwords out of code
smtplib	Send emails
Bootstrap (optional)	For prettier frontend (later)
🛠️ What We’ll Build (Next Steps)

    ✅ Use SQLite database to store questions and track results.

    ✅ Display multiple quiz questions dynamically.

    ✅ Evaluate and score quiz submissions.

    ✅ Store user submissions in database.

    ✅ Email result to the user.


    👣 One step at a time

    ⚡ Full project right now

✅ What Is Full-Stack Development?

Full-stack development means working on both the frontend and the backend of a web application — everything the user sees and interacts with, and everything that happens behind the scenes.
🔁 The “Stack” Breakdown
🧑‍💻 Frontend (Client-Side)

This is the user interface — what the user sees and interacts with in their browser.

Includes:

    HTML (structure)

    CSS (styling)

    JavaScript (interaction, animations)

    Frameworks: React, Vue, Bootstrap (optional)

📍 Example: The quiz form where the user types their answer.
🛠️ Backend (Server-Side)

This is where your app processes logic, stores data, and talks to services (like sending emails or fetching quiz questions from a database).

Includes:

    Python (Flask, Django)

    Node.js

    Java

    Ruby

    PHP

📍 Example: Your quiz_backend.py handles routes, checks answers, and sends emails.
🗃️ Database (Data Layer)

Where persistent information is stored and retrieved.

Examples:

    SQLite (what we’ll use)

    PostgreSQL

    MySQL

    MongoDB (NoSQL)

📍 Example: Instead of hardcoding a quiz answer, we store questions & answers in a database table.
📦 Example of a Full-Stack Quiz App (like Yours)
1. User visits http://localhost:5000

➡️ Flask serves quiz.html (HTML page)
2. User answers: “What is Flask?”

➡️ HTML form submits answer to Flask
3. Flask backend receives the answer

➡️ Checks against correct answer from SQLite
➡️ Saves result to database
➡️ Sends result via email
4. User sees: “Thanks, your score has been emailed”

➡️ Frontend shows confirmation
➡️ Email is delivered from backend
🔍 Diagram of Full-Stack Flow

[Browser (HTML, CSS, JS)]
        ⇅  form POST/GET
[Flask App (Python)]
        ⇅  SQLAlchemy
[SQLite Database]
        ⇅  SMTP
[Gmail - Email Delivery]

You now see why your project is more than just a script — it is a real full-stack application because you're managing:

    Frontend (HTML form)

    Backend (Flask routes + logic)

    External service (SMTP email)

    Data layer (optional but coming: SQLite)

🧠 Summary: What Full-Stack Dev Really Means
Area	You’ve Already Done It
Frontend (HTML)	✅ quiz.html
Backend (Flask/Python)	✅ quiz_backend.py
External API/Service	✅ Gmail SMTP
Database	🛠️ Next step: SQLite
✅ Real-World Analogy

    Imagine building an online school exam portal:

        Frontend shows exam pages, options, submit buttons.

        Backend calculates score, stores result, sends emails.

        Database stores questions, answers, user scores.

You’re already building this piece by piece.

    ✅ quiz.html for frontend

    ✅ quiz_backend.py for Flask routing

    ✅ send_result_email.py for sending email

👉 The Next Logical Step: Introduce a Database

Specifically, we’ll:

    🔹 Create a SQLite database
    🔹 Store quiz questions and answers in it
    🔹 Load questions dynamically from the DB into your HTML form

🧱 Step 1: Create the Database with SQLAlchemy

We'll start by creating a models.py file that:

    Sets up a SQLite database (quiz.db)

    Defines a Question table

    Inserts a few sample questions
please for modularizong the questions into a seperate script like we have done in models.py, 
then do the following before running backend
Do This Now:

    Replace questions in models.py

    Delete existing quiz.db (if needed, to repopulate fresh questions)

    Run:

python models.py

Then:

python quiz_backend.py

Visit: http://127.0.0.1:5000/

That new error tells us exactly what’s wrong:

    ❌ send_email() got an unexpected keyword argument 'to'`

✅ Root Cause:

In your quiz_backend.py, you likely called send_email() like this:

send_email(to=email, subject="Your Score", body=email_body)

But the actual send_email() function (probably in send_result_email.py) was defined with positional parameters, like:

def send_email(recipient, subject, body):

So Python doesn’t recognize to= as a valid keyword.
✅ Fix It In One of Two Ways:
✅ Option 1: Change the call to use positional arguments

Update your call in quiz_backend.py:

send_email(email, "Your Score", email_body)

This matches the function signature send_email(recipient, subject, body).
✅ Option 2: Update the function to accept to= as a keyword

Change the send_email() definition in send_result_email.py to:

def send_email(to, subject, body):
    ...
    message["To"] = to

    Where does feedback_html come from and how do we use it?
    And you'd like your script to send a detailed email like:

Hello,

You scored 7 out of 10.

Results:
Q1. Why is the person...?
Your answer: Because they pray too little ❌
Correct answer: Because they pass judgment while doing the same things

...

Thanks for taking the quiz!

Let’s walk through it properly, using your quiz_backend.py and email module.
✅ Step-by-Step Integration Plan:

We will:

    Build a detailed result message in Python.

    Use it both in the email body and browser return.

🧩 Modify your submit_quiz() route like this:

@app.route("/submit", methods=["POST"])
def submit_quiz():
    session = Session()
    email = request.form.get("email")
    score = 0
    total = 0

    questions = session.query(Question).all()

    # 📩 This will hold the full feedback for email and browser
    feedback = f"Hello,\n\nYou took the Romans 2 Quiz.\n\n"
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
    feedback += "Thanks for taking the quiz!"

    # Send email
    try:
        send_email(email, "Your Romans 2 Quiz Result", feedback)
        print("✅ Email sent successfully.")
    except Exception as e:
        print("❌ Failed to send email:", e)

    # Return message in browser too (for user to see immediately)
    return f"<pre>{feedback}</pre>"

✅ Explanation of New Parts:
Code Segment	Purpose
result_details = ""	Accumulates Q&A breakdown
getattr(q, f"option_{...}")	Dynamically fetches the right option text
feedback += ...	Builds the full message for both email and browser
return f"<pre>{feedback}</pre>"	Displays clean message in browser using <pre> formatting


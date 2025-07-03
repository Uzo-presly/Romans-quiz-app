# send_result_email.py

import smtplib
import os
from email.message import EmailMessage

def send_email(to_email, subject, body):
    # Load from environment variables
    from_email = os.environ.get("SENDER_EMAIL")
    password = os.environ.get("APP_PASSWORD")

    if not from_email or not password:
        raise ValueError("Missing EMAIL_USER or EMAIL_PASS in environment")

    # Compose email
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    msg.set_content(body)

    # Send email using Gmail SMTP
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(from_email, password)
        smtp.send_message(msg)

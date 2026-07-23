import os
import smtplib
from datetime import date
from email.message import EmailMessage

import requests

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
EMAIL_ADDRESS = os.environ["EMAIL_ADDRESS"]
EMAIL_APP_PASSWORD = os.environ["EMAIL_APP_PASSWORD"]
TO_EMAIL = os.environ["TO_EMAIL"]

MODEL = "claude-sonnet-4-6"


def build_prompt() -> str:
    today = date.today().strftime("%A, %B %d, %Y")
    return (
        f"Today is {today}. Write a short, thoughtful daily briefing for me: "
        "include a motivational thought, a fun fact, and a suggestion for "
        "something productive to focus on today."
    )


def call_claude(prompt: str) -> str:
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": MODEL,
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}],
        },
    )
    response.raise_for_status()
    data = response.json()
    return "".join(block["text"] for block in data["content"] if block["type"] == "text")


def send_email(body: str) -> None:
    msg = EmailMessage()
    msg["Subject"] = f"Daily Claude Briefing - {date.today().strftime('%B %d, %Y')}"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
        smtp.send_message(msg)


def main() -> None:
    prompt = build_prompt()
    reply = call_claude(prompt)
    send_email(reply)
    print("Email sent successfully.")


if __name__ == "__main__":
    main()

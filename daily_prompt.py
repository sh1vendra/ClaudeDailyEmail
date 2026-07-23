import os
import smtplib
from datetime import date
from email.message import EmailMessage
from urllib.parse import quote

EMAIL_ADDRESS = os.environ["EMAIL_ADDRESS"]
EMAIL_APP_PASSWORD = os.environ["EMAIL_APP_PASSWORD"]
TO_EMAIL = os.environ["TO_EMAIL"]

SUGGESTED_PROMPT = (
    "Search the web for today's weather forecast for San Marcos, Texas, "
    "including whether it will rain, and the high and low temperatures. "
    "Then check my Google Calendar for any events, meetings, or reminders "
    "scheduled for today. Give me a short summary of both."
)


def build_email_body(today: str) -> str:
    claude_link = f"claude://claude.ai/new?q={quote(SUGGESTED_PROMPT)}"
    return (
        "Good morning Boss. Ready to conquer today?\n\n"
        f"Today is {today}.\n\n"
        "Tap to start your Claude session with today's prompt already loaded:\n"
        f"{claude_link}\n\n"
        "If the link doesn't open the app, you can also copy this prompt manually:\n"
        "---\n"
        f"{SUGGESTED_PROMPT}\n"
        "---\n"
    )


def send_email(body: str) -> None:
    msg = EmailMessage()
    msg["Subject"] = "Time for your daily Claude session"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
        smtp.send_message(msg)


def main() -> None:
    today = date.today().strftime("%A, %B %d, %Y")
    body = build_email_body(today)
    send_email(body)
    print("Email sent successfully.")


if __name__ == "__main__":
    main()

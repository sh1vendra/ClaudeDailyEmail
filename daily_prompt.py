import os
import smtplib
from datetime import date
from email.message import EmailMessage

EMAIL_ADDRESS = os.environ["EMAIL_ADDRESS"]
EMAIL_APP_PASSWORD = os.environ["EMAIL_APP_PASSWORD"]
TO_EMAIL = os.environ["TO_EMAIL"]

CLAUDE_URL = "https://claude.ai/new"

SUGGESTED_PROMPT = (
    "Search the web for today's weather forecast for San Marcos, Texas, "
    "including whether it will rain, and the high and low temperatures. "
    "Then check my Google Calendar for any events, meetings, or reminders "
    "scheduled for today. Give me a short summary of both."
)


def build_email_body(today: str) -> str:
    return (
        f"Today is {today}.\n\n"
        f"Start your daily Claude session here: {CLAUDE_URL}\n\n"
        "Suggested prompt to copy and paste:\n"
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

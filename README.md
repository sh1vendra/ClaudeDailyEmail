# Claude Daily Email

A GitHub Actions workflow that emails you a daily reminder with a pre-built Claude prompt and a tap-to-open link, so you never have to manually open Claude and type a prompt to start your day.

## Table of Contents

- [What This Does](#what-this-does)
- [Why](#why)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Daylight Saving Time Drift](#daylight-saving-time-drift)
- [Customization Ideas](#customization-ideas)
- [License](#license)
- [Contributing](#contributing)

## What This Does

A GitHub Actions workflow runs on a schedule (`.github/workflows/daily-claude.yml`). Each run:

1. Executes `daily_prompt.py`, which builds an email containing today's date, a suggested Claude prompt, and a `claude://` link with that prompt URL-encoded into it.
2. Sends the email via Gmail SMTP to whatever address you configure.

On mobile, tapping the `claude://` link in the email opens the Claude app with the prompt already typed into the input box, ready for you to review and send. No API calls are made — this project only builds and sends an email; you interact with Claude directly through the app.

## Why

Claude's usage limits don't reset at midnight — they reset on a rolling 5-hour window that starts from your *first message* in that window. Whenever you send that first message, the clock starts. Everything after that counts against the same window until it expires 5 hours later, at which point a fresh window opens on your next message.

That mechanic has a hidden cost: if you don't message Claude until 11am, your first window of the day doesn't start until 11am. The hours before that — the ones you spent making coffee, commuting, or getting through email — are hours your usage window could already have been running, but wasn't. You're not saving anything by waiting; you're just delaying when your day's usage cycle begins, which pushes every window after it later too.

This project closes that gap. An automated email lands at 7am (or whatever time you set) with a prompt already loaded behind a tap-to-open `claude://` link. The moment you wake up and tap it, your first window of the day starts — before you've even had coffee, let alone opened your laptop. Concretely, that means:

- Your rolling window resets early, so you have a full block of usage already running by the time you actually sit down to work
- You stop losing hours to a window you simply forgot to start
- Your usage cycle is front-loaded, so the windows that matter most — your actual working hours later in the day — aren't cut short by a start you delayed by accident

If you use Claude seriously throughout the day, this is a few seconds of setup that removes a completely avoidable inefficiency from every single day.

## Prerequisites

- A Gmail account with **2-Step Verification** enabled (required to generate an app password)
- A **Gmail app password** for that account
- A GitHub repository (this one, forked or cloned)
- The **Claude mobile app** installed, if you want the tap-to-open link to work — `claude://` links only work inside the Claude app itself, not in a mobile or desktop browser

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/sh1vendra/ClaudeDailyEmail.git
cd ClaudeDailyEmail
```

### 2. Add repo secrets

In GitHub, go to **Settings > Secrets and variables > Actions** and add the following repository secrets:

| Secret name         | Value                                              |
| -------------------- | --------------------------------------------------- |
| `EMAIL_ADDRESS`      | The Gmail address the email will be sent **from**  |
| `EMAIL_APP_PASSWORD` | The Gmail app password (see below)                 |
| `TO_EMAIL`           | The address the reminder should be sent **to**     |

### 3. Generate a Gmail app password

1. Make sure 2-Step Verification is turned on for your Google account.
2. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords).
3. Create a new app password (name it something like "Claude Daily Email").
4. Copy the generated 16-character password and use it as the `EMAIL_APP_PASSWORD` secret. This is not your regular Gmail password.

### 4. Customize the prompt

Open `daily_prompt.py` and edit the `SUGGESTED_PROMPT` variable to whatever prompt you want sent to you each day:

```python
SUGGESTED_PROMPT = (
    "Search the web for today's weather forecast for San Marcos, Texas, "
    "including whether it will rain, and the high and low temperatures. "
    "Then check my Google Calendar for any events, meetings, or reminders "
    "scheduled for today. Give me a short summary of both."
)
```

### 5. Set the schedule

Open `.github/workflows/daily-claude.yml` and edit the `cron` expression under `schedule`:

```yaml
on:
  schedule:
    - cron: "0 13 * * *"
```

Cron format is `minute hour day-of-month month day-of-week`, and **GitHub Actions schedules always run in UTC** — not your local time zone. To pick a time, convert your desired local time to UTC first.

Example: if you want the email to arrive at 8am CDT (UTC-5), that's `13:00` UTC, giving `0 13 * * *`. If you want 8am CST (UTC-6) instead, that's `14:00` UTC, giving `0 14 * * *`.

### 6. Test it manually

Before waiting for the scheduled run, trigger the workflow by hand:

1. Go to the **Actions** tab on GitHub.
2. Select the **Daily Claude Email** workflow.
3. Click **Run workflow** (this uses the `workflow_dispatch` trigger already defined in the workflow file).
4. Check your inbox and confirm the email arrives with the correct date, link, and prompt.

## Daylight Saving Time Drift

Cron schedules are fixed to a specific UTC time and do **not** automatically adjust for daylight saving time. If your target is a specific local time (e.g., "always 8am wherever I am"), you'll need to manually update the `cron` expression by one hour when DST starts or ends. If exact local timing doesn't matter to you, you can leave the schedule as-is and accept the hour shift twice a year.

## Customization Ideas

The prompt and schedule are just two variables — this same pattern works for other daily nudges:

- **Nightly journal prompt** — send it in the evening with a prompt like "Help me reflect on today: what went well, what didn't, and one thing to improve tomorrow."
- **Workout reminder** — a morning prompt suggesting a quick workout plan based on the day of the week.
- **Reading prompt** — a prompt that asks Claude to summarize or discuss whatever book or article you're currently working through.
- **Study prompt** — a prompt that quizzes you or reviews material for something you're studying, sent before your usual study time.

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

## Contributing

PRs are welcome, especially for:

- Support for other email providers beyond Gmail (Outlook, iCloud, etc.)
- Alternative notification methods (Slack, Discord, SMS)

Open an issue or PR with your proposed change.

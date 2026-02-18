# Still Alive Bot

A Telegram dead man's switch. Check in regularly - if you miss your deadline, your designated watchers are notified.

[![Still Alive Bot](bot.png)](https://t.me/salive_bot)

## How it works

1. Add a watcher via `/invite` — share the link with someone you trust
2. Check in daily with `/checkin`
3. If you miss your deadline, your watchers receive your custom alert message

Reminders are sent at a configurable daily time and again when the deadline is approaching.

## Commands

| Command     | Description                                                     |
| ----------- | --------------------------------------------------------------- |
| `/checkin`  | Record a check-in                                               |
| `/settings` | Configure interval, deadline, reminders, alert message, and PIN |
| `/invite`   | Generate a one-time invite link for a watcher                   |
| `/watchers` | View and manage your watchers                                   |
| `/watching` | View people you are watching                                    |
| `/lang`     | Switch language                                                 |

## Settings

- **Interval** — how often you intend to check in (12 / 24 / 48 / 72 h)
- **Deadline** — how long after a missed check-in before watchers are alerted (24-96 h)
- **Daily reminder** — UTC hour to receive a daily nudge
- **Before deadline** — reminder X hours before the deadline is reached
- **Alert message** — what your watchers see if you go silent
- **PIN** — optional 4-digit PIN required to complete a check-in

## Running

**Requirements:** Python 3.12+, [uv](https://github.com/astral-sh/uv)

```bash
BOT_TOKEN=your_token uv run python main.py
```

**Docker:**

```bash
docker build -t stillalive-bot .
docker run -e BOT_TOKEN=your_token -v $(pwd)/data:/app/data stillalive-bot
```

The SQLite database is stored at `stillalive.db` by default (set `DB_PATH` to override).

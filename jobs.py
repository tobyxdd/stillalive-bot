from datetime import datetime

from telegram.ext import ContextTypes

import db
from i18n import t


def get_name(user: dict) -> str:
    return user.get("username") or f"User {user['user_id']}"


async def check_deadlines(context: ContextTypes.DEFAULT_TYPE):
    """Hourly job to check for users past deadline and send alerts."""
    users = db.get_users_past_deadline()
    for user in users:
        watchers = db.get_watchers(user["user_id"])
        if not watchers:
            continue
        name = get_name(user)
        message = user.get("message")
        for watcher_id in watchers:
            watcher = db.get_user(watcher_id)
            ln = watcher["language"] if watcher else "en"
            if message:
                text = t(ln, "alert_message", name=name, message=message)
            else:
                text = t(ln, "alert_no_message", name=name)
            try:
                await context.bot.send_message(watcher_id, text)
            except Exception:
                pass
        db.mark_alerted(user["user_id"])


async def send_daily_reminders(context: ContextTypes.DEFAULT_TYPE):
    """Send daily reminders to users at their configured hour."""
    now = datetime.utcnow()
    current_hour = now.hour
    users = db.get_all_users()
    for user in users:
        if user.get("reminder_hour") == current_hour:
            if not db.has_watchers(user["user_id"]):
                continue
            ln = user.get("language", "en")
            try:
                await context.bot.send_message(user["user_id"], t(ln, "reminder_daily"))
            except Exception:
                pass


async def send_deadline_reminders(context: ContextTypes.DEFAULT_TYPE):
    """Send reminders to users approaching their deadline."""
    users = db.get_users_needing_deadline_reminder()
    for user in users:
        if not db.has_watchers(user["user_id"]):
            continue
        ln = user.get("language", "en")
        # Calculate hours remaining
        last = user.get("last_checkin")
        if isinstance(last, str):
            last = datetime.fromisoformat(last)
        if last:
            deadline_ts = last.timestamp() + user["deadline_hours"] * 3600
            hours_left = max(
                0, int((deadline_ts - datetime.utcnow().timestamp()) / 3600)
            )
            try:
                await context.bot.send_message(
                    user["user_id"],
                    t(ln, "reminder_deadline", hours=hours_left),
                )
            except Exception:
                pass

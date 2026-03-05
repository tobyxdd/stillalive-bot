import os
import secrets
from datetime import datetime, timezone
from html import escape as html_escape

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

import db
from config import ADMIN_ID, DB_PATH
from i18n import LANGUAGE_NAMES, t

# Conversation states
SET_MESSAGE = 1


def _pin_dots(entered: int) -> str:
    return "● " * entered + "○ " * (4 - entered)


def _pin_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(str(d), callback_data=f"pin_{d}") for d in [1, 2, 3]],
            [InlineKeyboardButton(str(d), callback_data=f"pin_{d}") for d in [4, 5, 6]],
            [InlineKeyboardButton(str(d), callback_data=f"pin_{d}") for d in [7, 8, 9]],
            [
                InlineKeyboardButton("✕", callback_data="pin_cancel"),
                InlineKeyboardButton("0", callback_data="pin_0"),
                InlineKeyboardButton("⌫", callback_data="pin_back"),
            ],
        ]
    )


def lang(user_id: int) -> str:
    user = db.get_user(user_id)
    return user["language"] if user else "en"


def get_name(user: dict | None, fallback: str = "User") -> str:
    if not user:
        return fallback
    return user.get("username") or f"User {user['user_id']}"


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or update.effective_user.first_name
    db.upsert_user(user_id, username)
    ln = lang(user_id)

    # Check for invite code
    if context.args and context.args[0].startswith("inv_"):
        code = context.args[0]
        invite = db.get_invite(code)
        if not invite:
            await update.message.reply_text(t(ln, "invite_invalid"))
            return
        inviter = db.get_user(invite["user_id"])
        inviter_name = get_name(inviter)
        keyboard = [
            [
                InlineKeyboardButton(
                    t(ln, "invite_accept"), callback_data=f"accept_{code}"
                ),
                InlineKeyboardButton(
                    t(ln, "invite_decline"), callback_data=f"decline_{code}"
                ),
            ]
        ]
        await update.message.reply_text(
            t(ln, "invite_received", name=inviter_name),
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return

    await update.message.reply_text(t(ln, "welcome"))


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ln = lang(update.effective_user.id)
    await update.message.reply_text(t(ln, "help"))


async def cmd_checkin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    ln = lang(user_id)
    if not db.has_watchers(user_id):
        db.log_checkin(user_id, False, "direct", "no_watchers")
        await update.message.reply_text(t(ln, "setup_needed"))
        return
    if db.get_pin_hash(user_id):
        context.user_data["pin_purpose"] = "checkin"
        context.user_data["pin_digits"] = ""
        await update.message.reply_text(
            t(ln, "pin_enter", dots=_pin_dots(0)),
            reply_markup=_pin_keyboard(),
        )
        return
    db.checkin(user_id)
    db.log_checkin(user_id, True, "direct")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    await update.message.reply_text(t(ln, "checkin_done", time=now))


async def cmd_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    ln = lang(user_id)
    user = db.get_user(user_id)
    if not user:
        db.upsert_user(user_id)
        user = db.get_user(user_id)

    msg = html_escape(user.get("message") or t(ln, "not_set"))
    text = t(
        ln,
        "settings_menu",
        interval=user["interval_hours"],
        deadline=user["deadline_hours"],
        reminder_hour=user["reminder_hour"],
        reminder_before=user["reminder_before"],
        message=msg,
    )

    has_pin = bool(db.get_pin_hash(user_id))
    keyboard = [
        [
            InlineKeyboardButton(t(ln, "btn_interval"), callback_data="set_interval"),
            InlineKeyboardButton(t(ln, "btn_deadline"), callback_data="set_deadline"),
        ],
        [
            InlineKeyboardButton(
                t(ln, "btn_reminder_time"), callback_data="set_reminder_hour"
            ),
            InlineKeyboardButton(
                t(ln, "btn_before_deadline"), callback_data="set_reminder_before"
            ),
        ],
        [
            InlineKeyboardButton(
                t(ln, "btn_edit_message"), callback_data="set_message"
            ),
            InlineKeyboardButton(
                t(ln, "btn_clear_pin" if has_pin else "btn_set_pin"),
                callback_data="clear_pin" if has_pin else "set_pin",
            ),
        ],
    ]
    if has_pin:
        duress_on = db.get_duress_mode(user_id)
        keyboard.append(
            [
                InlineKeyboardButton(
                    t(ln, "btn_disable_duress" if duress_on else "btn_enable_duress"),
                    callback_data="disable_duress" if duress_on else "enable_duress",
                )
            ]
        )
    await update.message.reply_text(
        text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML"
    )


async def cb_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    ln = lang(user_id)
    data = query.data

    if data == "set_interval":
        keyboard = [
            [
                InlineKeyboardButton(f"{h}h", callback_data=f"interval_{h}")
                for h in [12, 24, 48, 72]
            ]
        ]
        await query.edit_message_text(
            t(ln, "set_interval"), reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif data == "set_deadline":
        keyboard = [
            [
                InlineKeyboardButton(f"{h}h", callback_data=f"deadline_{h}")
                for h in [24, 48, 72, 96]
            ]
        ]
        await query.edit_message_text(
            t(ln, "set_deadline"), reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif data == "set_reminder_hour":
        rows = [
            [
                InlineKeyboardButton(f"{h}:00", callback_data=f"rhour_{h}")
                for h in range(r, r + 6)
            ]
            for r in range(0, 24, 6)
        ]
        await query.edit_message_text(
            t(ln, "set_reminder_hour"), reply_markup=InlineKeyboardMarkup(rows)
        )
    elif data == "set_reminder_before":
        keyboard = [
            [
                InlineKeyboardButton(f"{h}h", callback_data=f"rbefore_{h}")
                for h in [2, 4, 6, 12]
            ]
        ]
        await query.edit_message_text(
            t(ln, "set_reminder_before"), reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif data == "set_message":
        await query.edit_message_text(t(ln, "set_message"))
        context.user_data["awaiting_message"] = True
    elif data == "set_pin":
        if db.get_pin_hash(user_id):
            # PIN already exists — verify current one before allowing change
            context.user_data["pin_purpose"] = "change_pin"
            context.user_data["pin_digits"] = ""
            await query.edit_message_text(
                t(ln, "pin_confirm_change", dots=_pin_dots(0)),
                reply_markup=_pin_keyboard(),
            )
        else:
            context.user_data["pin_purpose"] = "setup"
            context.user_data["pin_digits"] = ""
            await query.edit_message_text(
                t(ln, "pin_setup_enter", dots=_pin_dots(0)),
                reply_markup=_pin_keyboard(),
            )
    elif data == "clear_pin":
        context.user_data["pin_purpose"] = "clear_pin"
        context.user_data["pin_digits"] = ""
        await query.edit_message_text(
            t(ln, "pin_confirm_clear", dots=_pin_dots(0)),
            reply_markup=_pin_keyboard(),
        )
    elif data == "enable_duress":
        context.user_data["pin_purpose"] = "enable_duress"
        context.user_data["pin_digits"] = ""
        await query.edit_message_text(
            t(ln, "pin_confirm_duress_enable", dots=_pin_dots(0)),
            reply_markup=_pin_keyboard(),
        )
    elif data == "disable_duress":
        context.user_data["pin_purpose"] = "disable_duress"
        context.user_data["pin_digits"] = ""
        await query.edit_message_text(
            t(ln, "pin_confirm_duress_disable", dots=_pin_dots(0)),
            reply_markup=_pin_keyboard(),
        )
    elif data.startswith("interval_"):
        val = int(data.split("_")[1])
        db.upsert_user(user_id, interval_hours=val)
        await query.edit_message_text(t(ln, "setting_saved"))
    elif data.startswith("deadline_"):
        val = int(data.split("_")[1])
        db.upsert_user(user_id, deadline_hours=val)
        await query.edit_message_text(t(ln, "setting_saved"))
    elif data.startswith("rhour_"):
        val = int(data.split("_")[1])
        db.upsert_user(user_id, reminder_hour=val)
        await query.edit_message_text(t(ln, "setting_saved"))
    elif data.startswith("rbefore_"):
        val = int(data.split("_")[1])
        db.upsert_user(user_id, reminder_before=val)
        await query.edit_message_text(t(ln, "setting_saved"))


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text input for setting message."""
    if not context.user_data.get("awaiting_message"):
        return
    user_id = update.effective_user.id
    ln = lang(user_id)
    db.upsert_user(user_id, message=update.message.text)
    context.user_data["awaiting_message"] = False
    await update.message.reply_text(t(ln, "message_saved"))


async def cb_pin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    ln = lang(user_id)
    action = query.data  # e.g. "pin_3", "pin_back", "pin_cancel"

    if action == "pin_cancel":
        if context.user_data.get("pin_purpose") == "checkin":
            db.log_checkin(user_id, False, "pin", "cancelled")
        context.user_data.pop("pin_purpose", None)
        context.user_data.pop("pin_digits", None)
        await query.delete_message()
        return

    digits: str = context.user_data.get("pin_digits", "")
    purpose: str = context.user_data.get("pin_purpose", "checkin")

    if action == "pin_back":
        digits = digits[:-1]
    else:
        digit = action.split("_")[1]
        if len(digits) < 4:
            digits += digit

    context.user_data["pin_digits"] = digits

    if len(digits) < 4:
        prompt_key = {
            "setup": "pin_setup_enter",
            "clear_pin": "pin_confirm_clear",
            "change_pin": "pin_confirm_change",
            "enable_duress": "pin_confirm_duress_enable",
            "disable_duress": "pin_confirm_duress_disable",
        }.get(purpose, "pin_enter")
        await query.edit_message_text(
            t(ln, prompt_key, dots=_pin_dots(len(digits))),
            reply_markup=_pin_keyboard(),
        )
        return

    # 4 digits entered — act on purpose
    if purpose == "setup":
        db.set_pin(user_id, digits)
        context.user_data.pop("pin_purpose", None)
        context.user_data.pop("pin_digits", None)
        await query.edit_message_text(t(ln, "pin_set"))
    elif purpose == "checkin":
        correct = db.verify_pin(user_id, digits)
        if correct:
            db.checkin(user_id)
            db.log_checkin(user_id, True, "pin")
        if correct or db.get_duress_mode(user_id):
            if not correct:
                db.log_checkin(user_id, False, "pin", "duress")
            context.user_data.pop("pin_purpose", None)
            context.user_data.pop("pin_digits", None)
            now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
            await query.edit_message_text(t(ln, "checkin_done", time=now))
        else:
            db.log_checkin(user_id, False, "pin", "wrong_pin")
            context.user_data["pin_digits"] = ""
            await query.edit_message_text(
                t(ln, "pin_wrong", dots=_pin_dots(0)),
                reply_markup=_pin_keyboard(),
            )
    elif purpose == "clear_pin":
        if db.verify_pin(user_id, digits):
            db.clear_pin(user_id)
            context.user_data.pop("pin_purpose", None)
            context.user_data.pop("pin_digits", None)
            await query.edit_message_text(t(ln, "pin_cleared"))
        else:
            context.user_data["pin_digits"] = ""
            await query.edit_message_text(
                t(ln, "pin_wrong", dots=_pin_dots(0)),
                reply_markup=_pin_keyboard(),
            )
    elif purpose == "change_pin":
        if db.verify_pin(user_id, digits):
            # Old PIN verified — now collect the new one
            context.user_data["pin_purpose"] = "setup"
            context.user_data["pin_digits"] = ""
            await query.edit_message_text(
                t(ln, "pin_setup_enter", dots=_pin_dots(0)),
                reply_markup=_pin_keyboard(),
            )
        else:
            context.user_data["pin_digits"] = ""
            await query.edit_message_text(
                t(ln, "pin_wrong", dots=_pin_dots(0)),
                reply_markup=_pin_keyboard(),
            )
    elif purpose in ("enable_duress", "disable_duress"):
        if db.verify_pin(user_id, digits):
            enabling = purpose == "enable_duress"
            db.set_duress_mode(user_id, enabling)
            context.user_data.pop("pin_purpose", None)
            context.user_data.pop("pin_digits", None)
            await query.edit_message_text(
                t(ln, "duress_enabled" if enabling else "duress_disabled")
            )
        else:
            context.user_data["pin_digits"] = ""
            await query.edit_message_text(
                t(ln, "pin_wrong", dots=_pin_dots(0)),
                reply_markup=_pin_keyboard(),
            )


async def cmd_invite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    ln = lang(user_id)
    code = f"inv_{secrets.token_urlsafe(8)}"
    db.create_invite(user_id, code)
    bot_username = (await context.bot.get_me()).username
    link = f"https://t.me/{bot_username}?start={code}"
    await update.message.reply_text(t(ln, "invite_link", link=link))


async def cb_invite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    ln = lang(user_id)
    data = query.data

    if data.startswith("accept_"):
        code = data[7:]
        invite = db.get_invite(code)
        if not invite:
            await query.edit_message_text(t(ln, "invite_invalid"))
            return
        inviter_id = invite["user_id"]
        db.upsert_user(user_id, update.effective_user.username)  # Ensure watcher exists
        db.add_watcher(inviter_id, user_id)
        db.suppress_stale_alert(inviter_id)
        db.delete_invite(code)
        inviter = db.get_user(inviter_id)
        await query.edit_message_text(t(ln, "invite_accepted", name=get_name(inviter)))
        # Notify inviter
        watcher_name = (
            update.effective_user.username or update.effective_user.first_name
        )
        try:
            inviter_ln = lang(inviter_id)
            await context.bot.send_message(
                inviter_id,
                t(inviter_ln, "invite_accepted_notify", name=watcher_name),
            )
        except Exception:
            pass
    elif data.startswith("decline_"):
        code = data[8:]
        db.delete_invite(code)
        await query.edit_message_text(t(ln, "invite_declined"))


async def cmd_watchers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    ln = lang(user_id)
    watchers = db.get_watchers(user_id)
    if not watchers:
        await update.message.reply_text(t(ln, "watchers_empty"))
        return
    lines = []
    buttons = []
    for wid in watchers:
        watcher = db.get_user(wid)
        name = get_name(watcher, f"User {wid}")
        lines.append(f"• {name}")
        buttons.append(
            [
                InlineKeyboardButton(
                    t(ln, "btn_remove", name=name), callback_data=f"rmwatch_{wid}"
                )
            ]
        )
    await update.message.reply_text(
        t(ln, "watchers_list", list="\n".join(lines)),
        reply_markup=InlineKeyboardMarkup(buttons) if buttons else None,
    )


async def cb_remove_watcher(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    ln = lang(user_id)
    watcher_id = int(query.data.split("_")[1])
    watcher = db.get_user(watcher_id)
    db.remove_watcher(user_id, watcher_id)
    await query.edit_message_text(t(ln, "watcher_removed", name=get_name(watcher)))


async def cmd_watching(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    ln = lang(user_id)
    watching = db.get_watching(user_id)
    if not watching:
        await update.message.reply_text(t(ln, "watching_empty"))
        return
    lines = []
    buttons = []
    now = datetime.now(timezone.utc)
    for u in watching:
        name = get_name(u)
        last = u.get("last_checkin")
        if not last:
            lines.append(t(ln, "watching_status_never", name=name))
        else:
            if isinstance(last, str):
                last = datetime.fromisoformat(last)
            deadline = last.timestamp() + u["deadline_hours"] * 3600
            time_str = last.strftime("%Y-%m-%d %H:%M UTC")
            if now.timestamp() > deadline:
                lines.append(t(ln, "watching_status_late", name=name, time=time_str))
            else:
                lines.append(t(ln, "watching_status_ok", name=name, time=time_str))
        buttons.append(
            [
                InlineKeyboardButton(
                    t(ln, "btn_stop_watching", name=name),
                    callback_data=f"stopwatch_{u['user_id']}",
                )
            ]
        )
    await update.message.reply_text(
        t(ln, "watching_list", list="\n".join(lines)),
        reply_markup=InlineKeyboardMarkup(buttons) if buttons else None,
    )


async def cb_stop_watching(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    watcher_id = update.effective_user.id
    ln = lang(watcher_id)
    user_id = int(query.data.split("_")[1])
    user = db.get_user(user_id)
    db.remove_watcher(user_id, watcher_id)
    await query.edit_message_text(t(ln, "stopped_watching", name=get_name(user)))
    # Notify the user being watched
    watcher_name = update.effective_user.username or update.effective_user.first_name
    try:
        user_ln = lang(user_id)
        await context.bot.send_message(
            user_id,
            t(user_ln, "watcher_left", name=watcher_name),
        )
    except Exception:
        pass


async def cmd_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    ln = lang(user_id)
    langs = list(LANGUAGE_NAMES.items())
    keyboard = [
        [
            InlineKeyboardButton(name, callback_data=f"lang_{code}")
            for code, name in langs[i : i + 2]
        ]
        for i in range(0, len(langs), 2)
    ]
    await update.message.reply_text(
        t(ln, "lang_select"), reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def cb_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    new_lang = query.data.split("_")[1]
    db.upsert_user(user_id, language=new_lang)
    await query.edit_message_text(t(new_lang, "lang_changed"))


async def cmd_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not ADMIN_ID or update.effective_user.id != ADMIN_ID:
        return

    args = context.args or []
    subcommand = args[0].lower() if args else "status"

    if subcommand == "status":
        await _admin_status(update)
    elif subcommand == "user" and len(args) >= 2:
        await _admin_user(update, args[1])
    elif subcommand == "broadcast" and len(args) >= 2:
        message = " ".join(args[1:])
        await _admin_broadcast(update, context, message)
    else:
        await update.message.reply_text(
            "Admin commands:\n"
            "/admin — Bot status dashboard\n"
            "/admin user <id> — Inspect a user\n"
            "/admin broadcast <msg> — Message all users"
        )


async def _admin_status(update: Update):
    stats = db.get_stats()
    checkins = db.get_checkin_stats(24)

    db_size_kb = os.path.getsize(DB_PATH) / 1024

    lines = [
        "Bot Status",
        "",
        f"Users: {stats['total_users']}",
        f"  With watchers: {stats['users_with_watchers']}",
        f"  Without watchers: {stats['total_users'] - stats['users_with_watchers']}",
        f"Watcher links: {stats['total_watchers']}",
        f"Pending invites: {stats['pending_invites']}",
        "",
        f"Past deadline: {stats['past_deadline']}",
        f"Alerted: {stats['alerted']}",
        "",
        "Check-ins (24h):",
        f"  Total: {checkins['total']}",
        f"  Successful: {checkins['successful']}",
        f"  Failed: {checkins['failed']}",
        f"  Wrong PIN: {checkins['wrong_pin']}",
        f"  Duress: {checkins['duress']}",
        "",
        f"DB size: {db_size_kb:.1f} KB",
    ]
    await update.message.reply_text("\n".join(lines))


async def _admin_user(update: Update, user_id_str: str):
    try:
        uid = int(user_id_str)
    except ValueError:
        await update.message.reply_text("Invalid user ID.")
        return

    user = db.get_user(uid)
    if not user:
        await update.message.reply_text(f"User {uid} not found.")
        return

    watchers = db.get_watchers(uid)
    watcher_names = []
    for wid in watchers:
        w = db.get_user(wid)
        watcher_names.append(get_name(w, f"User {wid}"))

    last = user.get("last_checkin") or "never"
    has_pin = "yes" if user.get("pin_hash") else "no"
    duress = "yes" if user.get("duress_mode") else "no"

    lines = [
        f"User: {get_name(user)} ({uid})",
        f"Language: {user.get('language', 'en')}",
        f"Created: {user.get('created_at', '?')}",
        "",
        f"Interval: {user['interval_hours']}h",
        f"Deadline: {user['deadline_hours']}h",
        f"Reminder: {user['reminder_hour']}:00 UTC",
        f"Reminder before: {user['reminder_before']}h",
        "",
        f"Last check-in: {last}",
        f"Alerted: {'yes' if user.get('alerted') else 'no'}",
        f"PIN: {has_pin}",
        f"Duress mode: {duress}",
        "",
        f"Watchers ({len(watchers)}): {', '.join(watcher_names) or 'none'}",
    ]

    logs = db.get_user_checkin_logs(uid)
    if logs:
        lines.append("")
        lines.append("Recent check-ins:")
        for log in logs:
            status = "OK" if log["success"] else log.get("failure_reason", "failed")
            lines.append(f"  {log['timestamp']} [{log['method']}] {status}")
    else:
        lines.append("\nNo check-in logs.")

    await update.message.reply_text("\n".join(lines))


async def _admin_broadcast(
    update: Update, context: ContextTypes.DEFAULT_TYPE, message: str
):
    users = db.get_all_users()
    sent = 0
    failed = 0
    for user in users:
        try:
            await context.bot.send_message(user["user_id"], message)
            sent += 1
        except Exception:
            failed += 1
    await update.message.reply_text(
        f"Broadcast complete: {sent} sent, {failed} failed."
    )

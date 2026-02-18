import secrets
from datetime import datetime, timezone

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

import db
from i18n import t

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
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    await update.message.reply_text(t(ln, "checkin_done", time=now))


async def cmd_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    ln = lang(user_id)
    user = db.get_user(user_id)
    if not user:
        db.upsert_user(user_id)
        user = db.get_user(user_id)

    msg = user.get("message") or t(ln, "not_set")
    text = t(
        ln,
        "settings_menu",
        interval=user["interval_hours"],
        deadline=user["deadline_hours"],
        reminder_hour=user["reminder_hour"],
        reminder_before=user["reminder_before"],
        message=msg,
    )

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
                t(ln, "btn_clear_pin" if db.get_pin_hash(user_id) else "btn_set_pin"),
                callback_data="clear_pin" if db.get_pin_hash(user_id) else "set_pin",
            ),
        ],
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


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
        if db.verify_pin(user_id, digits):
            db.checkin(user_id)
            context.user_data.pop("pin_purpose", None)
            context.user_data.pop("pin_digits", None)
            now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
            await query.edit_message_text(t(ln, "checkin_done", time=now))
        else:
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
    keyboard = [
        [
            InlineKeyboardButton("English", callback_data="lang_en"),
            InlineKeyboardButton("中文", callback_data="lang_zh"),
        ]
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

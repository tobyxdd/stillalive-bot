STRINGS = {
    "en": {
        "welcome": (
            "Welcome to Still Alive Bot!\n\n"
            "This bot helps you check in daily. If you miss your deadline, your watchers will be notified.\n\n"
            "Quick Setup:\n"
            "1. /settings → Edit Message (set what watchers see if you're unresponsive)\n"
            "2. /invite → Share link with a trusted person\n"
            "3. /checkin → Do this daily!\n\n"
            "Defaults: check-in every 24h, alert after 48h.\n"
            "Use /settings to customize."
        ),
        "help": (
            "Commands:\n"
            "/checkin - Check in to confirm you're alive\n"
            "/settings - Configure your settings\n"
            "/invite - Generate invite link for a watcher\n"
            "/watchers - View your watchers\n"
            "/watching - View who you're watching\n"
            "/lang - Change language\n"
            "/help - Show this help"
        ),
        "checkin_done": "Check-in recorded at {time}. Stay safe!",
        "settings_menu": "Settings:\n\nInterval: {interval}h\nDeadline: {deadline}h\nDaily reminder: {reminder_hour}:00 UTC\nReminder before deadline: {reminder_before}h\nMessage: {message}",
        "set_interval": "Set check-in interval:",
        "set_deadline": "Set deadline (hours after last check-in):",
        "set_reminder_hour": "Set daily reminder time (UTC hour):",
        "set_reminder_before": "Remind me X hours before deadline:",
        "set_message": "Send your alert message (what watchers will see):",
        "message_saved": "Alert message saved!",
        "setting_saved": "Setting saved!",
        "invite_link": "Share this link with someone you want as a watcher:\n\n{link}\n\nThey must click it and accept to receive alerts.",
        "invite_received": "{name} wants you to be their emergency contact.\n\nIf they miss their check-in deadline, you'll be notified.\n\nAccept?",
        "invite_accept": "Accept",
        "invite_decline": "Decline",
        "invite_accepted": "You are now watching {name}.",
        "invite_accepted_notify": "{name} accepted your invite and is now watching you!",
        "invite_declined": "Invite declined.",
        "invite_invalid": "This invite is invalid or expired.",
        "watchers_list": "Your watchers:\n{list}\n\nUse buttons to remove.",
        "watchers_empty": "You have no watchers yet. Use /invite to add some.",
        "watcher_removed": "Removed {name} from your watchers.",
        "watching_list": "You are watching:\n{list}",
        "watching_empty": "You are not watching anyone.",
        "watching_status_ok": "{name}: last check-in {time} (OK)",
        "watching_status_late": "{name}: last check-in {time} (LATE!)",
        "watching_status_never": "{name}: never checked in",
        "reminder_daily": "Daily reminder: Please check in with /checkin",
        "reminder_deadline": "Warning: Your deadline is in {hours}h! Check in soon with /checkin",
        "alert_message": "ALERT from Still Alive Bot:\n\n{name} has missed their check-in deadline!\n\nTheir message:\n{message}",
        "alert_no_message": "ALERT from Still Alive Bot:\n\n{name} has missed their check-in deadline!\n\n(No custom message set)",
        "lang_changed": "Language changed to English.",
        "lang_select": "Select language:",
        "setup_needed": "Please set up first:\n1. Use /settings to set your alert message\n2. Use /invite to add watchers",
        "back": "Back",
        "cancel": "Cancel",
        "hours": "{n}h",
        "btn_interval": "Interval",
        "btn_deadline": "Deadline",
        "btn_reminder_time": "Reminder Time",
        "btn_before_deadline": "Before Deadline",
        "btn_edit_message": "Edit Message",
        "btn_remove": "Remove {name}",
        "btn_stop_watching": "Stop watching {name}",
        "stopped_watching": "You stopped watching {name}.",
        "watcher_left": "{name} is no longer watching you.",
        "not_set": "(not set)",
        "pin_enter": "Enter your PIN to check in:\n\n{dots}",
        "pin_setup_enter": "Set a new 4-digit PIN:\n\n{dots}",
        "pin_wrong": "Wrong PIN. Try again:\n\n{dots}",
        "pin_set": "PIN protection enabled.",
        "pin_cleared": "PIN protection removed.",
        "pin_confirm_clear": "Enter your current PIN to disable protection:\n\n{dots}",
        "pin_confirm_change": "Enter your current PIN to set a new one:\n\n{dots}",
        "btn_set_pin": "Set PIN",
        "btn_clear_pin": "Clear PIN",
    },
    "zh": {
        "welcome": (
            "欢迎使用 Still Alive Bot!\n\n"
            "这个机器人帮助你每日签到。如果你错过截止时间,你的守望者将收到通知。\n\n"
            "快速设置:\n"
            "1. /settings → 编辑消息(设置你无响应时守望者看到的内容)\n"
            "2. /invite → 分享链接给信任的人\n"
            "3. /checkin → 每天签到!\n\n"
            "默认:每24小时签到,48小时后发送警报。\n"
            "使用 /settings 自定义设置。"
        ),
        "help": (
            "命令:\n"
            "/checkin - 签到确认你还活着\n"
            "/settings - 配置设置\n"
            "/invite - 生成守望者邀请链接\n"
            "/watchers - 查看你的守望者\n"
            "/watching - 查看你正在守望的人\n"
            "/lang - 更改语言\n"
            "/help - 显示帮助"
        ),
        "checkin_done": "签到已记录于 {time}。保重!",
        "settings_menu": "设置:\n\n签到间隔: {interval}小时\n截止时间: {deadline}小时\n每日提醒: {reminder_hour}:00 UTC\n截止前提醒: {reminder_before}小时\n消息: {message}",
        "set_interval": "设置签到间隔:",
        "set_deadline": "设置截止时间(上次签到后小时数):",
        "set_reminder_hour": "设置每日提醒时间(UTC小时):",
        "set_reminder_before": "截止前X小时提醒我:",
        "set_message": "发送你的警报消息(守望者将看到):",
        "message_saved": "警报消息已保存!",
        "setting_saved": "设置已保存!",
        "invite_link": "将此链接分享给你想要作为守望者的人:\n\n{link}\n\n他们必须点击并接受才能收到警报。",
        "invite_received": "{name} 希望你成为他们的紧急联系人。\n\n如果他们错过签到截止时间,你将收到通知。\n\n接受吗?",
        "invite_accept": "接受",
        "invite_decline": "拒绝",
        "invite_accepted": "你现在正在守望 {name}。",
        "invite_accepted_notify": "{name} 接受了你的邀请,现在正在守望你!",
        "invite_declined": "邀请已拒绝。",
        "invite_invalid": "此邀请无效或已过期。",
        "watchers_list": "你的守望者:\n{list}\n\n使用按钮移除。",
        "watchers_empty": "你还没有守望者。使用 /invite 添加。",
        "watcher_removed": "已将 {name} 从你的守望者中移除。",
        "watching_list": "你正在守望:\n{list}",
        "watching_empty": "你没有守望任何人。",
        "watching_status_ok": "{name}: 上次签到 {time} (正常)",
        "watching_status_late": "{name}: 上次签到 {time} (迟到!)",
        "watching_status_never": "{name}: 从未签到",
        "reminder_daily": "每日提醒:请使用 /checkin 签到",
        "reminder_deadline": "警告:你的截止时间还有 {hours} 小时!请尽快使用 /checkin 签到",
        "alert_message": "Still Alive Bot 警报:\n\n{name} 错过了签到截止时间!\n\n他们的消息:\n{message}",
        "alert_no_message": "Still Alive Bot 警报:\n\n{name} 错过了签到截止时间!\n\n(未设置自定义消息)",
        "lang_changed": "语言已更改为中文。",
        "lang_select": "选择语言:",
        "setup_needed": "请先设置:\n1. 使用 /settings 设置警报消息\n2. 使用 /invite 添加守望者",
        "back": "返回",
        "cancel": "取消",
        "hours": "{n}小时",
        "btn_interval": "签到间隔",
        "btn_deadline": "截止时间",
        "btn_reminder_time": "提醒时间",
        "btn_before_deadline": "截止前提醒",
        "btn_edit_message": "编辑消息",
        "btn_remove": "移除 {name}",
        "btn_stop_watching": "停止守望 {name}",
        "stopped_watching": "你已停止守望 {name}。",
        "watcher_left": "{name} 不再守望你了。",
        "not_set": "(未设置)",
        "pin_enter": "请输入 PIN 码以签到:\n\n{dots}",
        "pin_setup_enter": "设置新的4位 PIN 码:\n\n{dots}",
        "pin_wrong": "PIN 码错误,请重试:\n\n{dots}",
        "pin_set": "PIN 码保护已启用。",
        "pin_cleared": "PIN 码保护已关闭。",
        "pin_confirm_clear": "请输入当前 PIN 码以关闭保护:\n\n{dots}",
        "pin_confirm_change": "请输入当前 PIN 码以设置新码:\n\n{dots}",
        "btn_set_pin": "设置 PIN 码",
        "btn_clear_pin": "清除 PIN 码",
    },
}


def t(lang: str, key: str, **kwargs) -> str:
    """Get translated string with optional formatting."""
    text = STRINGS.get(lang, STRINGS["en"]).get(key, STRINGS["en"].get(key, key))
    return text.format(**kwargs) if kwargs else text

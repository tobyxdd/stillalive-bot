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
        "btn_enable_duress": "Enable Duress Mode",
        "btn_disable_duress": "Disable Duress Mode",
        "duress_enabled": "Duress mode enabled. The bot will now always appear to accept any PIN.",
        "duress_disabled": "Duress mode disabled.",
        "pin_confirm_duress_enable": "Enter your PIN to enable duress mode:\n\n{dots}",
        "pin_confirm_duress_disable": "Enter your PIN to disable duress mode:\n\n{dots}",
        "cmd_checkin": "Check in to confirm you're alive",
        "cmd_settings": "Configure your settings",
        "cmd_invite": "Generate invite link for a watcher",
        "cmd_watchers": "View your watchers",
        "cmd_watching": "View who you're watching",
        "cmd_lang": "Change language",
        "cmd_help": "Show help",
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
        "btn_enable_duress": "启用胁迫模式",
        "btn_disable_duress": "禁用胁迫模式",
        "duress_enabled": "胁迫模式已启用。无论输入什么 PIN 码,机器人都会显示签到成功。",
        "duress_disabled": "胁迫模式已禁用。",
        "pin_confirm_duress_enable": "请输入 PIN 码以启用胁迫模式:\n\n{dots}",
        "pin_confirm_duress_disable": "请输入 PIN 码以禁用胁迫模式:\n\n{dots}",
        "cmd_checkin": "签到确认你还活着",
        "cmd_settings": "配置设置",
        "cmd_invite": "生成守望者邀请链接",
        "cmd_watchers": "查看你的守望者",
        "cmd_watching": "查看你正在守望的人",
        "cmd_lang": "更改语言",
        "cmd_help": "显示帮助",
    },
    "es": {
        "welcome": (
            "¡Bienvenido a Still Alive Bot!\n\n"
            "Este bot te ayuda a registrarte diariamente. Si no lo haces antes del límite, tus vigilantes serán notificados.\n\n"
            "Configuración rápida:\n"
            "1. /settings → Editar mensaje (lo que verán tus vigilantes si no respondes)\n"
            "2. /invite → Comparte el enlace con alguien de confianza\n"
            "3. /checkin → ¡Hazlo cada día!\n\n"
            "Por defecto: registro cada 24h, alerta tras 48h.\n"
            "Usa /settings para personalizar."
        ),
        "help": (
            "Comandos:\n"
            "/checkin - Registrarse para confirmar que estás bien\n"
            "/settings - Configurar ajustes\n"
            "/invite - Generar enlace de invitación para un vigilante\n"
            "/watchers - Ver tus vigilantes\n"
            "/watching - Ver a quién estás vigilando\n"
            "/lang - Cambiar idioma\n"
            "/help - Mostrar esta ayuda"
        ),
        "checkin_done": "Registro realizado a las {time}. ¡Cuídate!",
        "settings_menu": "Ajustes:\n\nIntervalo: {interval}h\nLímite: {deadline}h\nRecordatorio diario: {reminder_hour}:00 UTC\nAviso antes del límite: {reminder_before}h\nMensaje: {message}",
        "set_interval": "Establecer intervalo de registro:",
        "set_deadline": "Establecer límite (horas tras el último registro):",
        "set_reminder_hour": "Establecer hora del recordatorio diario (UTC):",
        "set_reminder_before": "Avisarme X horas antes del límite:",
        "set_message": "Envía tu mensaje de alerta (lo que verán tus vigilantes):",
        "message_saved": "¡Mensaje de alerta guardado!",
        "setting_saved": "¡Ajuste guardado!",
        "invite_link": "Comparte este enlace con quien quieras como vigilante:\n\n{link}\n\nDeben hacer clic y aceptar para recibir alertas.",
        "invite_received": "{name} quiere que seas su contacto de emergencia.\n\nSi no se registra antes del límite, serás notificado.\n\n¿Aceptas?",
        "invite_accept": "Aceptar",
        "invite_decline": "Rechazar",
        "invite_accepted": "Ahora estás vigilando a {name}.",
        "invite_accepted_notify": "¡{name} aceptó tu invitación y ahora te está vigilando!",
        "invite_declined": "Invitación rechazada.",
        "invite_invalid": "Esta invitación no es válida o ha expirado.",
        "watchers_list": "Tus vigilantes:\n{list}\n\nUsa los botones para eliminar.",
        "watchers_empty": "Aún no tienes vigilantes. Usa /invite para añadir.",
        "watcher_removed": "Se eliminó a {name} de tus vigilantes.",
        "watching_list": "Estás vigilando a:\n{list}",
        "watching_empty": "No estás vigilando a nadie.",
        "watching_status_ok": "{name}: último registro {time} (OK)",
        "watching_status_late": "{name}: último registro {time} (¡TARDE!)",
        "watching_status_never": "{name}: nunca se ha registrado",
        "reminder_daily": "Recordatorio diario: Por favor regístrate con /checkin",
        "reminder_deadline": "Aviso: ¡Tu límite es en {hours}h! Regístrate pronto con /checkin",
        "alert_message": "ALERTA de Still Alive Bot:\n\n¡{name} no se ha registrado antes del límite!\n\nSu mensaje:\n{message}",
        "alert_no_message": "ALERTA de Still Alive Bot:\n\n¡{name} no se ha registrado antes del límite!\n\n(Sin mensaje personalizado)",
        "lang_changed": "Idioma cambiado a español.",
        "lang_select": "Selecciona idioma:",
        "setup_needed": "Configura primero:\n1. Usa /settings para establecer tu mensaje de alerta\n2. Usa /invite para añadir vigilantes",
        "back": "Atrás",
        "cancel": "Cancelar",
        "hours": "{n}h",
        "btn_interval": "Intervalo",
        "btn_deadline": "Límite",
        "btn_reminder_time": "Hora de aviso",
        "btn_before_deadline": "Antes del límite",
        "btn_edit_message": "Editar mensaje",
        "btn_remove": "Eliminar {name}",
        "btn_stop_watching": "Dejar de vigilar a {name}",
        "stopped_watching": "Dejaste de vigilar a {name}.",
        "watcher_left": "{name} ya no te está vigilando.",
        "not_set": "(no establecido)",
        "pin_enter": "Introduce tu PIN para registrarte:\n\n{dots}",
        "pin_setup_enter": "Establece un nuevo PIN de 4 dígitos:\n\n{dots}",
        "pin_wrong": "PIN incorrecto. Inténtalo de nuevo:\n\n{dots}",
        "pin_set": "Protección por PIN activada.",
        "pin_cleared": "Protección por PIN eliminada.",
        "pin_confirm_clear": "Introduce tu PIN actual para desactivar la protección:\n\n{dots}",
        "pin_confirm_change": "Introduce tu PIN actual para establecer uno nuevo:\n\n{dots}",
        "btn_set_pin": "Establecer PIN",
        "btn_clear_pin": "Eliminar PIN",
        "btn_enable_duress": "Activar modo coacción",
        "btn_disable_duress": "Desactivar modo coacción",
        "duress_enabled": "Modo coacción activado. El bot siempre mostrará éxito independientemente del PIN introducido.",
        "duress_disabled": "Modo coacción desactivado.",
        "pin_confirm_duress_enable": "Introduce tu PIN para activar el modo coacción:\n\n{dots}",
        "pin_confirm_duress_disable": "Introduce tu PIN para desactivar el modo coacción:\n\n{dots}",
        "cmd_checkin": "Registrarse para confirmar que estás bien",
        "cmd_settings": "Configurar ajustes",
        "cmd_invite": "Generar enlace de invitación para un vigilante",
        "cmd_watchers": "Ver tus vigilantes",
        "cmd_watching": "Ver a quién estás vigilando",
        "cmd_lang": "Cambiar idioma",
        "cmd_help": "Mostrar ayuda",
    },
    "ru": {
        "welcome": (
            "Добро пожаловать в Still Alive Bot!\n\n"
            "Этот бот помогает вам регулярно отмечаться. Если вы пропустите дедлайн, ваши наблюдатели получат уведомление.\n\n"
            "Быстрая настройка:\n"
            "1. /settings → Редактировать сообщение (что увидят наблюдатели, если вы не отвечаете)\n"
            "2. /invite → Поделитесь ссылкой с доверенным человеком\n"
            "3. /checkin → Делайте это каждый день!\n\n"
            "По умолчанию: отметка каждые 24ч, оповещение через 48ч.\n"
            "Используйте /settings для настройки."
        ),
        "help": (
            "Команды:\n"
            "/checkin - Отметиться и подтвердить, что вы живы\n"
            "/settings - Настройки\n"
            "/invite - Создать ссылку-приглашение для наблюдателя\n"
            "/watchers - Посмотреть ваших наблюдателей\n"
            "/watching - Посмотреть, за кем вы наблюдаете\n"
            "/lang - Изменить язык\n"
            "/help - Показать эту справку"
        ),
        "checkin_done": "Отметка записана в {time}. Берегите себя!",
        "settings_menu": "Настройки:\n\nИнтервал: {interval}ч\nДедлайн: {deadline}ч\nЕжедневное напоминание: {reminder_hour}:00 UTC\nНапоминание до дедлайна: {reminder_before}ч\nСообщение: {message}",
        "set_interval": "Установить интервал отметки:",
        "set_deadline": "Установить дедлайн (часов после последней отметки):",
        "set_reminder_hour": "Установить время ежедневного напоминания (UTC):",
        "set_reminder_before": "Напомнить за X часов до дедлайна:",
        "set_message": "Отправьте ваше сообщение (его увидят наблюдатели):",
        "message_saved": "Сообщение сохранено!",
        "setting_saved": "Настройка сохранена!",
        "invite_link": "Поделитесь этой ссылкой с тем, кого хотите сделать наблюдателем:\n\n{link}\n\nОни должны нажать и принять, чтобы получать оповещения.",
        "invite_received": "{name} хочет сделать вас своим экстренным контактом.\n\nЕсли они пропустят дедлайн, вы получите уведомление.\n\nПринять?",
        "invite_accept": "Принять",
        "invite_decline": "Отклонить",
        "invite_accepted": "Теперь вы наблюдаете за {name}.",
        "invite_accepted_notify": "{name} принял(а) ваше приглашение и теперь наблюдает за вами!",
        "invite_declined": "Приглашение отклонено.",
        "invite_invalid": "Это приглашение недействительно или истекло.",
        "watchers_list": "Ваши наблюдатели:\n{list}\n\nИспользуйте кнопки для удаления.",
        "watchers_empty": "У вас ещё нет наблюдателей. Используйте /invite для добавления.",
        "watcher_removed": "{name} удалён из ваших наблюдателей.",
        "watching_list": "Вы наблюдаете за:\n{list}",
        "watching_empty": "Вы ни за кем не наблюдаете.",
        "watching_status_ok": "{name}: последняя отметка {time} (OK)",
        "watching_status_late": "{name}: последняя отметка {time} (ОПОЗДАНИЕ!)",
        "watching_status_never": "{name}: никогда не отмечался(-ась)",
        "reminder_daily": "Ежедневное напоминание: пожалуйста, отметьтесь с помощью /checkin",
        "reminder_deadline": "Внимание: до дедлайна осталось {hours}ч! Отметьтесь скорее с помощью /checkin",
        "alert_message": "ОПОВЕЩЕНИЕ от Still Alive Bot:\n\n{name} пропустил(а) дедлайн!\n\nИх сообщение:\n{message}",
        "alert_no_message": "ОПОВЕЩЕНИЕ от Still Alive Bot:\n\n{name} пропустил(а) дедлайн!\n\n(Сообщение не задано)",
        "lang_changed": "Язык изменён на русский.",
        "lang_select": "Выберите язык:",
        "setup_needed": "Сначала выполните настройку:\n1. Используйте /settings для задания сообщения\n2. Используйте /invite для добавления наблюдателей",
        "back": "Назад",
        "cancel": "Отмена",
        "hours": "{n}ч",
        "btn_interval": "Интервал",
        "btn_deadline": "Дедлайн",
        "btn_reminder_time": "Время напоминания",
        "btn_before_deadline": "До дедлайна",
        "btn_edit_message": "Изменить сообщение",
        "btn_remove": "Удалить {name}",
        "btn_stop_watching": "Перестать следить за {name}",
        "stopped_watching": "Вы перестали наблюдать за {name}.",
        "watcher_left": "{name} больше не наблюдает за вами.",
        "not_set": "(не задано)",
        "pin_enter": "Введите PIN для отметки:\n\n{dots}",
        "pin_setup_enter": "Задайте новый 4-значный PIN:\n\n{dots}",
        "pin_wrong": "Неверный PIN. Попробуйте ещё раз:\n\n{dots}",
        "pin_set": "Защита PIN включена.",
        "pin_cleared": "Защита PIN отключена.",
        "pin_confirm_clear": "Введите текущий PIN для отключения защиты:\n\n{dots}",
        "pin_confirm_change": "Введите текущий PIN для установки нового:\n\n{dots}",
        "btn_set_pin": "Установить PIN",
        "btn_clear_pin": "Удалить PIN",
        "btn_enable_duress": "Включить режим принуждения",
        "btn_disable_duress": "Выключить режим принуждения",
        "duress_enabled": "Режим принуждения включён. Бот будет принимать любой PIN как верный.",
        "duress_disabled": "Режим принуждения выключён.",
        "pin_confirm_duress_enable": "Введите PIN для включения режима принуждения:\n\n{dots}",
        "pin_confirm_duress_disable": "Введите PIN для выключения режима принуждения:\n\n{dots}",
        "cmd_checkin": "Отметиться и подтвердить, что вы живы",
        "cmd_settings": "Настройки",
        "cmd_invite": "Создать ссылку-приглашение для наблюдателя",
        "cmd_watchers": "Посмотреть ваших наблюдателей",
        "cmd_watching": "Посмотреть, за кем вы наблюдаете",
        "cmd_lang": "Изменить язык",
        "cmd_help": "Показать справку",
    },
}


LANGUAGE_NAMES = {
    "en": "English",
    "zh": "中文",
    "es": "Español",
    "ru": "Русский",
}


def t(lang: str, key: str, **kwargs) -> str:
    """Get translated string with optional formatting."""
    text = STRINGS.get(lang, STRINGS["en"]).get(key, STRINGS["en"].get(key, key))
    return text.format(**kwargs) if kwargs else text

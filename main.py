import logging

from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

import db
import handlers
import jobs
from config import BOT_TOKEN

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN environment variable not set")
        return

    db.init_db()

    app = Application.builder().token(BOT_TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", handlers.cmd_start))
    app.add_handler(CommandHandler("help", handlers.cmd_help))
    app.add_handler(CommandHandler("checkin", handlers.cmd_checkin))
    app.add_handler(CommandHandler("settings", handlers.cmd_settings))
    app.add_handler(CommandHandler("invite", handlers.cmd_invite))
    app.add_handler(CommandHandler("watchers", handlers.cmd_watchers))
    app.add_handler(CommandHandler("watching", handlers.cmd_watching))
    app.add_handler(CommandHandler("lang", handlers.cmd_lang))

    # Callback query handlers
    app.add_handler(CallbackQueryHandler(handlers.cb_pin, pattern=r"^pin_"))
    app.add_handler(
        CallbackQueryHandler(
            handlers.cb_settings,
            pattern=r"^(set_|clear_pin|interval_|deadline_|rhour_|rbefore_)",
        )
    )
    app.add_handler(
        CallbackQueryHandler(handlers.cb_invite, pattern=r"^(accept_|decline_)")
    )
    app.add_handler(
        CallbackQueryHandler(handlers.cb_remove_watcher, pattern=r"^rmwatch_")
    )
    app.add_handler(
        CallbackQueryHandler(handlers.cb_stop_watching, pattern=r"^stopwatch_")
    )
    app.add_handler(CallbackQueryHandler(handlers.cb_lang, pattern=r"^lang_"))

    # Text handler for message input
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.handle_text)
    )

    # Schedule jobs
    job_queue = app.job_queue
    job_queue.run_repeating(jobs.check_deadlines, interval=3600, first=10)
    job_queue.run_repeating(jobs.send_daily_reminders, interval=3600, first=10)
    job_queue.run_repeating(jobs.send_deadline_reminders, interval=3600, first=10)

    logger.info("Bot starting...")
    app.run_polling()


if __name__ == "__main__":
    main()

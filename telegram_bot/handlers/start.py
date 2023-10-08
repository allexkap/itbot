from telegram import Update
from telegram.ext import CallbackContext, CommandHandler


def get_handler():
    def handler(update: Update, context: CallbackContext) -> None:
        context.bot.send_message(chat_id=update.effective_chat.id, text="yeah")

    return CommandHandler('start', handler)

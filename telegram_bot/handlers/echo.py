from telegram import ParseMode, Update
from telegram.ext import CallbackContext, MessageHandler


def get_handler():
    def handler(update: Update, context: CallbackContext) -> None:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=update.message.text_html,
            parse_mode=ParseMode.HTML,
        )

    return MessageHandler(None, handler)

from telegram import ParseMode, Update
from telegram.ext import CallbackContext, Handler, MessageHandler


def get_handler() -> Handler:
    def handler(update: Update, context: CallbackContext) -> None:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=update.message.text_html,
            parse_mode=ParseMode.HTML,
        )

    return MessageHandler(None, handler)

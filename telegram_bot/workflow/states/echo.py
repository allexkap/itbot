from telegram import ParseMode

from .utils import *


def prepare(update: Update, context: CallbackContext) -> None | str:
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="$echo_message",
    )


def process(update: Update, context: CallbackContext) -> None | str:
    try:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=update.message.text_html,
            parse_mode=ParseMode.HTML,
        )
    finally:
        return 'start'

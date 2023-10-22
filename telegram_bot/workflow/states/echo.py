from telegram import ParseMode

from .utils import *

edges = {
    'cancel': 'start',
}


def prepare(update: Update, context: CallbackContext) -> None | str:
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="$echo_message",
        reply_markup=get_markup(edges),
    )


@parse_commands(edges)
def process(update: Update, context: CallbackContext) -> None | str:
    try:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=update.message.text_html,
            parse_mode=ParseMode.HTML,
        )
    finally:
        return 'start'

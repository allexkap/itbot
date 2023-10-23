from telegram import ParseMode

from .utils import *

edges = [
    Edge('start', 'cancel'),
]


def prepare(update: Update, context: CallbackContext) -> None | str:
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Напиши любое сообщение",
        reply_markup=get_markup(edges),
    )


@parse_commands(edges)
def process(update: Update, context: CallbackContext) -> None | str:
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text_html,
        parse_mode=ParseMode.HTML,
    )
    return 'start'

from telegram import ReplyKeyboardRemove

from .utils import *

edges = [
    Edge('start', 'start', ''),
]


def prepare(update: Update, context: CallbackContext) -> None | str:
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Хорошо, я тебя забыл :_(",
        reply_markup=ReplyKeyboardRemove(),
    )


@parse_commands(edges)
def process(update: Update, context: CallbackContext) -> None | str:
    pass

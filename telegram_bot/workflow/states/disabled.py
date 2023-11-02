from .utils import *

edges = [
    Edge('ready', 'start'),
]


prepare = send_message_with_reply_keyboard('Хорошо, я тебя забыл :_(')


@parse_commands(edges)
def process(update: Update, context: CallbackContext, user: User) -> str | None:
    pass

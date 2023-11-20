from .utils import *

edges = [
    Edge('ready', 'start'),
]


prepare = send_message_with_reply_keyboard('state_disabled:text')


@parse_commands(edges)
def process(update: Update, context: CallbackContext, user: User) -> str | None:
    pass

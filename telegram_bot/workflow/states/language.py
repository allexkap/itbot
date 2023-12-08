from telegram_bot.workflow.utils import *


def handler(update: Update, context: CallbackContext, user: User) -> str | None:
    user.language = edges[edges.index((update.effective_message.text, user))].cmd
    user.save()
    return 'ready'


edges = [
    Edge(handler, 'ru', 'state_language:ru'),
    Edge(handler, 'en', 'state_language:en'),
    Edge('ready', 'cancel', 'global:cancel'),
]


prepare = send_message_with_reply_keyboard('global:placeholder', edges)


@parse_commands(edges)
def process(update: Update, context: CallbackContext, user: User) -> str | None:
    pass

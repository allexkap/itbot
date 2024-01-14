from telegram_bot.workflow.utils import *


edges = [
    Edge(None, 'ru', 'state_language:ru'),
    Edge(None, 'en', 'state_language:en'),
    Edge('ready', 'cancel', 'global:cancel'),
]


prepare = send_message_with_reply_keyboard('global:placeholder', edges)


@parse_commands(edges)
def process(update: Update, context: CallbackContext, user: User) -> str | None:
    try:
        user.language = edges[edges.index((update.effective_message.text, user))].cmd
        user.save()
    except ValueError:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=get_text('state_language:unknown_language', user),
        )
    return 'ready'

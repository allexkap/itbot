from telegram_bot.workflow.utils import *

edges = [
    Edge('ready', 'start'),
]


def prepare(update: Update, context: CallbackContext, user: User) -> str | None:
    user.isu_id = None
    user.save()
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=get_text('state_disabled:text', user),
        reply_markup=get_reply_markup(edges, user),
    )


@parse_commands(edges)
def process(update: Update, context: CallbackContext, user: User) -> str | None:
    pass

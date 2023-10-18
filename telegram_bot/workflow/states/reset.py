from .utils import *

WAYS = {
    'start': 'start',
}


def prepare(update: Update, context: CallbackContext) -> None | str:
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="$reset_message",
    )


@parse_commands(WAYS)
def process(update: Update, context: CallbackContext) -> None | str:
    pass

from .utils import *

edges = {
    'stop': 'reset',
    'echo': 'echo',
}


def prepare(update: Update, context: CallbackContext) -> None | str:
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="$start_message",
        reply_markup=get_markup(edges),
    )


@parse_commands(edges)
def process(update: Update, context: CallbackContext) -> None | str:
    pass

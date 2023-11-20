from .utils import *

edges = [
    Edge('test_echo', 'echo', 'Повторить сообщение'),
    Edge('test_magic', 'magic', 'Сделать красиво'),
    Edge('disabled', 'stop', 'Выйти из аккаунта'),
]


def prepare(update: Update, context: CallbackContext, user: User) -> str | None:
    user.clear_properties()
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=get_text('state_ready:text', user),
        reply_markup=get_reply_markup(edges, user),
    )


@parse_commands(edges)
def process(update: Update, context: CallbackContext, user: User) -> str | None:
    pass

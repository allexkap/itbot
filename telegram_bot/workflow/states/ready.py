from .utils import *

edges = [
    Edge('test_echo', 'echo', 'Повторить сообщение'),
    Edge('disabled', 'stop', 'Выйти из аккаунта'),
]


def prepare(update: Update, context: CallbackContext) -> None | str:
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Что делаем?",
        reply_markup=get_markup(edges),
    )


@parse_commands(edges)
def process(update: Update, context: CallbackContext) -> None | str:
    pass

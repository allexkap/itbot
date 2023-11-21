from telegram_bot.workflow.utils import *

edges = [
    Edge('test/echo', 'echo', 'state_ready:edge_test_echo'),
    Edge('test/magic', 'magic', 'state_ready:edge_test_magic'),
    Edge('disabled', 'stop', 'state_ready:edge_disabled'),
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

from telegram_bot.workflow.utils import *

edges = [
    Edge('test/echo', 'echo', 'state_ready:edge_test_echo'),
    Edge('test/magic', 'magic', 'state_ready:edge_test_magic'),
    Edge('auth', 'auth', 'state_ready:edge_auth'),
    Edge('language', 'setlang', 'state_ready:edge_language'),
    Edge('disabled', 'stop', 'state_ready:edge_disabled'),
]


# external access for keycloak
def reset(bot, chat_id, user):
    user.clear_properties()
    bot.send_message(
        chat_id=chat_id,
        text=get_text('state_ready:text', user),
        reply_markup=get_reply_markup(edges, user),
    )


def prepare(update: Update, context: CallbackContext, user: User) -> str | None:
    reset(context.bot, update.effective_chat.id, user)


@parse_commands(edges)
def process(update: Update, context: CallbackContext, user: User) -> str | None:
    pass

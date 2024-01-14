from telegram_bot.workflow.utils import *
import requests


def qrcode(update: Update, context: CallbackContext, user: User) -> str | None:
    r = requests.get(
        'https://upload.wikimedia.org/wikipedia/commons/thumb/'
        '8/8d/QR_Code_Damaged.jpg/220px-QR_Code_Damaged.jpg'
    )
    assert r.status_code == 200
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=r.content)


edges = [
    Edge('auth', 'auth', 'state_ready:edge_auth', lambda u: not u.is_authenticated()),
    Edge(qrcode, 'qr', 'state_ready:qrcode', lambda u: u.is_authenticated()),
    Edge('language', 'setlang', 'state_ready:edge_language'),
    Edge('disabled', 'stop', 'state_ready:edge_disabled'),
    Edge('test/echo', 'echo', 'state_ready:edge_test_echo'),
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

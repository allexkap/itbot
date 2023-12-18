from django.conf import settings
from telegram import ParseMode

from telegram_bot.workflow.utils import *

edges = [
    Edge('ready', 'cancel', 'global:cancel'),
]


def prepare(update: Update, context: CallbackContext, user: User) -> str | None:
    link = (
        '{}/protocol/openid-connect/auth?scope=openid&response_type=code'
        '&client_id={}&redirect_uri={}&state={}'.format(
            settings.KEYCLOAK_REALM_URL,
            settings.KEYCLOAK_CLIENT_ID,
            settings.KEYCLOAK_REDIRECT_URL,
            update.effective_user.id,
        )
    )

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='<a href="{}">{}</a>'.format(link, get_text('state_auth:link', user)),
        reply_markup=get_reply_markup(edges, user),
        parse_mode=ParseMode.HTML,
    )


@parse_commands(edges)
def process(update: Update, context: CallbackContext, user: User) -> str | None:
    pass

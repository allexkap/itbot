from django.contrib import admin

from telegram_bot.locale import String
from telegram_bot.models import Context, User

admin.site.register(User)
admin.site.register(Context)
admin.site.register(String)

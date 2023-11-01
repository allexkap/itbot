from django.contrib import admin

from telegram_bot.models import Context, User

# Register your models here.
admin.site.register(User)
admin.site.register(Context)

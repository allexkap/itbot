from telegram import Update
from telegram.ext import Updater
from django.conf import settings
from django.http import JsonResponse
from django.utils.module_loading import import_string
from django.views.decorators.csrf import csrf_exempt
import json


updater = Updater(token=settings.TELEGRAM_BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

for name in settings.TELEGRAM_HANDLERS:
    handler = import_string(f'telegram_bot.handlers.{name}.get_handler')()
    dispatcher.add_handler(handler)


@csrf_exempt
def webhook(request):
    if request.method == "POST":
        json_string = request.body.decode('UTF-8')
        update = Update.de_json(json.loads(json_string), updater.bot)
        dispatcher.process_update(update)

    return JsonResponse({'status':'ok'})

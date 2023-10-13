import json

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update
from telegram.ext import MessageHandler, Updater

from telegram_bot.workflow.handler import workflow_handler

updater = Updater(token=settings.TELEGRAM_BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(MessageHandler(None, workflow_handler))


@csrf_exempt
def webhook(request) -> JsonResponse:
    if request.method == "POST":
        json_string = request.body.decode('UTF-8')
        update = Update.de_json(json.loads(json_string), updater.bot)
        dispatcher.process_update(update)

    return JsonResponse({'status': 'ok'})

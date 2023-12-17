import json

import requests
from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseServerError, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update
from telegram.ext import MessageHandler, Updater

from telegram_bot.workflow.handler import workflow_handler

updater = Updater(token=settings.TELEGRAM_BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(MessageHandler(None, workflow_handler))


@csrf_exempt
def webhook(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        json_string = request.body.decode('UTF-8')
        update = Update.de_json(json.loads(json_string), updater.bot)
        dispatcher.process_update(update)

    return JsonResponse({'status': 'ok'})


@csrf_exempt
def keycloak(request: HttpRequest) -> HttpResponse:
    try:
        code = request.GET['code']
        r = requests.post(
            settings.KEYCLOAK_REALM_URL + '/protocol/openid-connect/token',
            data={
                'grant_type': 'authorization_code',
                'client_id': settings.KEYCLOAK_CLIENT_ID,
                'client_secret': settings.KEYCLOAK_CLIENT_SECRET,
                'redirect_uri': settings.KEYCLOAK_REDIRECT_URL,
                'code': code,
            },
        )
        return JsonResponse({'result': json.loads(r.content)})
    except KeyError:
        return JsonResponse(
            {
                'error': 'invalid_request',
                'error_description': 'Missing form parameter: code',
            }
        )
    except Exception as e:
        print('Error', e)
        return HttpResponseServerError()
    return JsonResponse({'status': 'ok'})

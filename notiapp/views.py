from channels.layers import get_channel_layer
from django.shortcuts import render, HttpResponse
from django.template import RequestContext
import json
# Create your views here.

from asgiref.sync import async_to_sync
def test(request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notification_%s" % request.user.username,
        {
            'type': 'send_notification',
            'message': 'haiii'
        }
    )
    return HttpResponse("Done")
    
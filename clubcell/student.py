from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.template.loader import render_to_string

from clubcell.models import events, event_query
import sys


class Student:

    @staticmethod
    def ask_event_query(request):
        if request.user.is_authenticated and request.method == "POST" and request.is_ajax():
            user = request.user
            query = request.POST['query']
            event_uen = request.POST['uen']
            rinfo = request.POST['replying_info']
            event = events.objects.get(event_uen=event_uen)
            replied_model = None
            replied_user_model = None
            if rinfo != "0-0":
                replied = int(rinfo.split('-')[0])
                replied_user = int(rinfo.split('-')[1])
                replied_model = event_query.objects.get(pk=replied, event=event)
                replied_user_model = User.objects.get(pk=replied_user)
                ask = event_query(user=user, query=query, event=event, replied=replied_model,
                                  replied_user=replied_user_model)
                ask.save()
                html = render_to_string('ajax/reply_query.html', {'user': user,
                                                                'event': event,
                                                                'reply': ask,
                                                                'query': replied_model
                                                                },
                                        request=request)
            else:
                ask = event_query(user=user, query=query, event=event, replied=replied_model,
                                  replied_user=replied_user_model)
                ask.save()
                html = render_to_string('ajax/ask_query.html', {'user': user,
                                                                'event': event,
                                                                'query': ask
                                                                },
                                        request=request)

            return HttpResponse(html)

    @staticmethod
    def dlt_event_query(request):
        if request.user.is_authenticated and request.method == "POST" and request.is_ajax():
            user = request.user
            query = int(request.POST['qdata'])
            event_uen = request.POST['uen']
            event = events.objects.get(event_uen=event_uen)
            target_query = event_query.objects.get(user=user, pk=query, event=event)
            target_query.delete()
            return HttpResponse({})
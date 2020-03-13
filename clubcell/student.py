from django.shortcuts import render
from clubcell.models import eventstodo
import sys


class Student:
    @staticmethod
    def render_dict(request):
        if request.user.is_authenticated:
            user = request.user
            events = reversed(eventstodo.objects.filter(show_public=True))
            path = sys.path[0] + "\\media\\user\\" + user.details.PAN + "\\" + "event_registered.csv"
            with open(path, 'r') as fb:
                event_register = fb.read().splitlines()
            return {'signup_path': 'signup', 'l_b_active': 'btn btn-light action-button',
                       's_b_active': 'text-white-50 login',
                       'events': events, "user": user, 'event_register': event_register}

    @staticmethod
    def home(request):
        return render(request, 'studentcell/shome.html', Student.render_dict(request))

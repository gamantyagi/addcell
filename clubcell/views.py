import json

from django.http import HttpResponse

from clubcell.models import events, clubcell, events, messages, typing_message, event_participants, posts
from .General import General, GoTo
from django.contrib.auth.models import User
from .Constants import Paths, Pages, Alerts
from .Common import Rendering, GetData, InCSV
import os


class Entry:

    @staticmethod
    def login(request):
        # Return True if login succeed
        if General.login_by_request(request):
            return GoTo.redirect_to(Paths.HOMEPAGE)
        else:
            # alert will send to the user if submitted username or password is incorrect
            General.message_response(request, if_method='POST', alert=Alerts.LOGIN_FAILED_MESSAGE)
            return GoTo.render_page(request, Pages.LOGIN)

    @staticmethod
    def homepage(request):
        if request.user.is_authenticated:
            if GetData.is_user_having_club(request):
                return GoTo.redirect_to(Paths.CLUB_HOME)
            else:
                return GoTo.redirect_to(Paths.STUDENT_HOME)
        else:
            return GoTo.redirect_to(Paths.LOGIN)

    @staticmethod
    def signup(request):
        # Return True if registration succeed
        if not request.user.is_authenticated:
            if General.signup(request):
                return GoTo.landing_page()
            else:
                return GoTo.render_page(request, Pages.SIGNUP)
        else:
            # Landing page is root url of site
            return GoTo.landing_page()

    @staticmethod
    def logout(request):
        General.logout_user(request)
        return GoTo.landing_page()


class Club:

    @staticmethod
    def having_permission(request):
        if request.user.is_authenticated and request.user.details.having_club:
            return True
        return False

    @staticmethod
    def home(request):
        # This function is used for club dashboard
        if Club.having_permission(request):
            user = request.user
            GetData.distinct_messages(request)
            return GoTo.render_page(request, Pages.CLUB_HOME, {'user': request.user,
                                                               'alert_unseen': user.alerts.filter(seen=False).count,
                                                               'events_done': user.clubcell.events.filter(
                                                                   event_complete='D'),
                                                               'events_todo': user.clubcell.events.filter(
                                                                   event_complete='P'),
                                                               'messages': GetData.distinct_messages(
                                                                   request)})
        return GoTo.landing_page()

    @staticmethod
    def profile_view(request):
        if Club.having_permission(request):
            return GoTo.render_page(request, Pages.CLUB_PROFILE_VIEW,
                                    {'user': request.user,
                                     'events_done': request.user.clubcell.events.filter(event_complete='D')})
        return GoTo.landing_page()

    @staticmethod
    def my_cell(request):
        if Club.having_permission(request):
            user = request.user
            return GoTo.render_page(request, Pages.CLUB_MY_CELL, {'user': request.user,
                                                                  'alert_unseen': user.alerts.filter(seen=False).count,
                                                                  'messages': GetData.distinct_messages(request)})
        return GoTo.landing_page()

    @staticmethod
    def add_event(request):
        return GoTo.render_page(request, Pages.ClUB_ADD_EVENT, Rendering.render_data(request, "Club: Add Event"))

    @staticmethod
    def event_todo_main(request, event_uen):
        # this method is use to manipulate only any one event todo's
        if Club.having_permission(request):
            user = request.user
            event = events.objects.get(club=user.clubcell, event_uen=event_uen)
            return GoTo.render_page(request, Pages.EVENT_TODO_MAIN, {'event': event,
                                                                     'alert_unseen': user.alerts.filter(
                                                                         seen=False).count,
                                                                     'messages': GetData.distinct_messages(request)})
        # return Club.events_todo(request)

    @staticmethod
    def events_todo(request):
        if Club.having_permission(request):
            user = request.user
            return GoTo.render_page(request, Pages.EVENTS_TODO,
                                    {'events_todo': reversed(user.clubcell.events.filter(event_complete='P'))})
        return GoTo.landing_page()

    @staticmethod
    def event_done(request):
        if Club.having_permission(request):
            user = request.user
            return GoTo.render_page(request, Pages.EVENTS_DONE, {'user': request.user,
                                                                 'alert_unseen': user.alerts.filter(seen=False).count,
                                                                 'events_done': user.clubcell.events.filter(
                                                                     event_complete='D'),
                                                                 'messages': GetData.distinct_messages(
                                                                     request)})
        return GoTo.landing_page()

    @staticmethod
    def update_profile(request):
        if Club.having_permission(request) and request.method == "POST":
            user = request.user

            username = request.POST['username'].lower().lstrip()
            first_name = (request.POST['first_name']).lower().lstrip()
            last_name = (request.POST['last_name']).lower().lstrip()
            email = request.POST['email'].lstrip()
            if username != '' and first_name != '' and last_name != '' and email != '':
                user.email, user.last_name, user.first_name, user.username = email, last_name, first_name, username
                user.save()
        return GoTo.redirect_to(Paths.CLUB_PROFILE_VIEW)

    @staticmethod
    def update_cell(request):
        if Club.having_permission(request) and request.method == "POST":
            user = request.user
            cell = clubcell.objects.get(PAN=user.details.PAN)
            cellname = request.POST['cellname'].lower().lstrip()
            offemail = (request.POST['offemail']).lower().lstrip()
            about = (request.POST['about']).lower().lstrip()
            tel = request.POST['tel'].lstrip()
            cell.off_email, cell.clubname, cell.tel, cell.about = offemail, cellname, tel, about
            cell.save()
        return GoTo.redirect_to(Paths.CLUB_PROFILE_VIEW)

    @staticmethod
    def members(request):
        if Club.having_permission(request):
            user = request.user
            return GoTo.render_page(request, Pages.CLUB_MEMBERS, {'user': request.user,
                                                                  'alert_unseen': user.alerts.filter(seen=False).count,
                                                                  'messages': GetData.distinct_messages(request),
                                                                  'teams': user.clubcell.team.all()})

    @staticmethod
    def posts(request):
        if Club.having_permission(request):
            user = request.user
            return GoTo.render_page(request, Pages.CLUB_POSTS, {'user': request.user,
                                                                'alert_unseen': user.alerts.filter(seen=False).count,
                                                                'messages': GetData.distinct_messages(request),
                                                                'posts': posts.objects.filter(user=user)})

    @staticmethod
    def addcells(request):
        if Club.having_permission(request):
            user = request.user
            return GoTo.render_page(request, Pages.CLUB_ADDCELLS, {'user': request.user,
                                                                   'alert_unseen': user.alerts.filter(seen=False).count,
                                                                   'messages': GetData.distinct_messages(request)})

    @staticmethod
    def trending(request):
        if Club.having_permission(request):
            user = request.user
            return GoTo.render_page(request, Pages.CLUB_TRENDING, {'user': request.user,
                                                                   'alert_unseen': user.alerts.filter(seen=False).count,
                                                                   'messages': GetData.distinct_messages(request)})


class Student:

    @staticmethod
    def home(request):
        if request.user.is_authenticated:
            user = request.user
            return GoTo.render_page(request, Pages.STUDENT_HOME, {'user': user,
                                                                  'events_todo': events.objects.filter(
                                                                      event_complete='P')})

    @staticmethod
    def profile(request):
        if request.user.is_authenticated:
            user = request.user
            return GoTo.render_page(request, Pages.STUDENT_PROFILE, {'user': user,
                                                                     'events_participants': event_participants.objects.filter(
                                                                         user=user)})

    @staticmethod
    def posts(request):
        if request.user.is_authenticated:
            user = request.user
            return GoTo.render_page(request, Pages.STUDENT_POSTS, {'user': user,
                                                                     'posts': posts.objects.all()})


class CommonMethod:

    @staticmethod
    def view_event_detail(request, event_uen):
        user = request.user
        return GoTo.render_page(request, Pages.CLUB_EVENT_DETAIL, {'user': user,
                                                                   'event': events.objects.get(event_uen=event_uen)
                                                                   })


class Message:

    @staticmethod
    def chat(request, chat_to):
        if request.user.is_authenticated:
            user = request.user
            chat_to_user = User.objects.get(username=chat_to)
            if request.method == "POST":
                message_sent = request.POST['message']
                new_msg = messages(user=user, second_user=chat_to_user, message_in=message_sent)
                new_msg.save()
                return GoTo.redirect_to('/messages/chat/{}/'.format(chat_to))

            chats = (messages.objects.filter(user=chat_to_user, second_user=user).union(
                messages.objects.filter(user=user, second_user=chat_to_user))).order_by('date_and_time')
            return GoTo.render_page(request, Pages.CHAT_PANEL, {'chat_to': chat_to_user,
                                                                'user': user,
                                                                'chats': chats
                                                                })

    @staticmethod
    def get_new_message(request, chat_to):
        if request.user.is_authenticated and request.is_ajax():
            user = request.user
            gpk = request.POST['element']
            txt_len = int(request.POST['text'])
            chat_to_user = User.objects.get(username=chat_to)
            # now we will get if second user is typing or not and set if we are also typing
            second_typing = GetData.typing_message(txt_len, user, chat_to_user)
            chats = (messages.objects.filter(user=chat_to_user, second_user=user).union(
                messages.objects.filter(user=user, second_user=chat_to_user))).order_by('date_and_time')
            last = chats.latest('date_and_time')
            if last.user == chat_to_user and last.seen == False:
                last.seen = True
                last.save()
            if last.pk == int(gpk):
                return HttpResponse(json.dumps("%dt" % (second_typing)), content_type="application/json")
            elif last.pk != int(gpk) and int(gpk) < last.pk and last.user != user:
                dict_data = {'result': 1, 'msg': last.message_in, 'user': last.user.username,
                             'time': str(last.get_time()[0]), 'date': str(last.get_time()[1]), 'id': last.pk}
                return HttpResponse(json.dumps(dict_data), content_type="application/json")
            else:
                return HttpResponse(json.dumps("-1"), content_type="application/json")
        else:
            return HttpResponse(json.dumps("unknown"), content_type="application/json")

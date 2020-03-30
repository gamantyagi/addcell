from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.utils import timezone

from clubcell.models import events, event_participants, details, team, members, event_query, messages, event_wishlist, \
    group_event
from django.http import HttpResponse
import sys
import csv
import json
from clubcell.ML import Logs
from .Common import GetData
from .Constants import Paths
import os


class Ajax:

    @staticmethod
    def validate_username(request):
        if request.method == "GET":
            username = request.GET.get('username', None)
            if not User.objects.filter(username=username).exists():
                return HttpResponse(json.dumps('not_taken'), content_type="application/json")
            else:
                return None

    ''' It shows only those event publicly which are allowed '''

    @staticmethod
    def show_event(request):
        if request.method == "GET" and request.user.is_authenticated:  # os request.GET()
            user = request.user
            event_id = request.GET.get('element', None)
            show = request.GET.get('show', None)
            try:
                update = user.clubcell.events.get(event_id=event_id)
                if not update.registration:
                    update.registration = True
                    update.save()
                    result = "{} is now publicly available for registration".format(update.eventname)
                    return HttpResponse(json.dumps(result), content_type="application/json")
                elif update.registration:
                    update.registration = False
                    update.save()
                    result = "{} is now not publicly available for registration".format(update.eventname)
                    return HttpResponse(json.dumps(result), content_type="application/json")
            except:
                return HttpResponse(json.dumps("Suspecious Activity by user"), content_type="application/json")
        else:
            return HttpResponse(json.dumps("Suspecious Activity by user in auth"), content_type="application/json")

    '''register for event by student '''

    @staticmethod
    def event_register(request):
        if request.method == "POST" and request.user.is_authenticated and request.is_ajax():  # os request.GET()
            event_id = request.POST.get('element', None)
            try:
                user = request.user
                event = events.objects.get(event_id=event_id)
                if event.registration and not event_participants.objects.filter(events=event, user=user).exists():
                    register_member = event_participants(user=user, club=event.club, events=event)
                    register_member.save()
                    result = event.event_uen  # it it used to change html of desire button, ID of that element
                    return HttpResponse(json.dumps(result), content_type="application/json")
                elif event.registration and event_participants.objects.filter(events=event, user=user).exists():
                    result = "Already registered"
                    return HttpResponse(json.dumps(result), content_type="application/json")
                elif not event.registration:
                    result = "closed"
                    return HttpResponse(json.dumps(result), content_type="application/json")
                else:
                    print("not expected")
                    return HttpResponse(json.dumps("specious"), content_type="application/json")
            except Exception as e:
                print(e)
                return HttpResponse(json.dumps("wrong"), content_type="application/json")
        else:
            return HttpResponse(json.dumps("Suspicious Activity by user"), content_type="application/json")

    @staticmethod
    def event_wishlist(request):
        if request.method == "POST" and request.user.is_authenticated and request.is_ajax():  # os request.GET()
            event_id = request.POST.get('element', None)
            try:
                user = request.user
                event = events.objects.get(event_id=event_id)
                if event_wishlist.objects.filter(events=event, user=user).exists():
                    result = "already wishlist"
                    return HttpResponse(json.dumps(result), content_type="application/json")
                elif event.registration and not event_participants.objects.filter(events=event, user=user).exists():
                    wishlist_member = event_wishlist(user=user, events=event)
                    wishlist_member.save()
                    result = event.event_uen  # it it used to change html of desire button, ID of that element
                    return HttpResponse(json.dumps(result), content_type="application/json")
                elif event.registration and event_participants.objects.filter(events=event, user=user).exists():
                    result = "Already registered"
                    return HttpResponse(json.dumps(result), content_type="application/json")
                elif not event.registration:
                    result = "closed"
                    return HttpResponse(json.dumps(result), content_type="application/json")
                else:
                    print("not expected")
                    return HttpResponse(json.dumps("specious"), content_type="application/json")
            except Exception as e:
                print(e)
                return HttpResponse(json.dumps("wrong"), content_type="application/json")
        else:
            return HttpResponse(json.dumps("Suspicious Activity by user"), content_type="application/json")

    @staticmethod
    def return_message(request, message_to):
        if request.user.is_authenticated:
            user = request.user
            message_to = User.objects.get(username=message_to)
            path = sys.path[0] + "\\media\\user\\" + user.details.PAN + "\\" + "event_registered.csv"
            return {"message_to_username": message_to.username,
                    "message_to_first_name": message_to.first_name,
                    "message_to_last_name": message_to.last_name
                    }

    def message_chat(request, message_to):
        if request.user.is_authenticated:
            user = request.user
            return render(request, 'common/message_chat.html', Ajax.return_message(request, message_to))


class Club:

    @staticmethod
    def add_member(request):
        if request.user.is_authenticated and request.is_ajax() and request.method == "POST":
            user = request.user
            member_reg_no = int(request.POST['member'])
            try:
                member = details.objects.get(reg_no=member_reg_no)
            except:
                if details.objects.filter(reg_no=member_reg_no).all().count() > 1:
                    return HttpResponse(json.dumps({'result': '-1',
                                                    'message': 'Error, registration number {} is associated with multiple account'.format(
                                                        member_reg_no)}), content_type="application/json")
                return HttpResponse(json.dumps(
                    {'result': '-1', 'message': 'No account found by registration number {}'.format(member_reg_no)}),
                    content_type="application/json")
            team_name = request.POST['team']
            teams = user.clubcell.team.get(team_name=team_name)
            already_member = member.user.members.filter(team=teams)
            if teams.team_name == team_name and already_member.all().count() == 0:
                new_member = members(user=member.user, club=user.clubcell, team=teams, post="CN")
                new_member.save()
                return HttpResponse(json.dumps(
                    {'result': '1', 'name': member.user.first_name + ' ' + member.user.last_name, 'reg': member.reg_no,
                     'team': teams.team_name, 'dp': member.profile_pic.url}), content_type="application/json")
            elif already_member.all().count() > 0:

                return HttpResponse(json.dumps({'result': '-1',
                                                'message': 'member {} {} already in team'.format(member.user.first_name,
                                                                                                 member.user.last_name)}),
                                    content_type="application/json")
            return HttpResponse(json.dumps({'result': '-1', 'message': 'team is not available or something other'}),
                                content_type="application/json")

    @staticmethod
    def edit_team(request):
        if request.user.is_authenticated and request.is_ajax() and request.method == "POST":
            user = request.user
            team_name = int(request.POST['team'])
            new_team_name = request.POST['new_name']
            try:
                teams = user.clubcell.team.get(pk=team_name)
            except:
                return HttpResponse(json.dumps({'result': '-1',
                                                'message': "can't change team name twice at a time, please refresh the page first"}),
                                    content_type="application/json")
            team_name = teams.team_name
            try:
                teams.team_name = new_team_name
                teams.save()
            except:
                return HttpResponse(json.dumps({'result': '-1', 'message': "Error in given name, may be too long."}),
                                    content_type="application/json")
            if user.clubcell.team.get(team_name=new_team_name):
                return HttpResponse(
                    json.dumps({'result': '1', 'oldName': team_name, 'newName': new_team_name, 'team_pk': teams.pk}),
                    content_type="application/json")
            return HttpResponse(json.dumps({'result': '-1', 'message': 'team name failed to initialize'}),
                                content_type="application/json")

    @staticmethod
    def delete_team(request):
        if request.user.is_authenticated and request.is_ajax() and request.method == "POST":
            user = request.user
            team_name = int(request.POST['team'])
            confirm_team = request.POST['confirm_team']
            try:
                teams = user.clubcell.team.get(pk=team_name)
            except:
                return HttpResponse(json.dumps({'result': '-1',
                                                'message': "No team found, unusual thing happened.".format(team_name)}),
                                    content_type="application/json")
            if teams.team_name == confirm_team:
                name = teams.team_name
                teams.delete()
                return HttpResponse(json.dumps({'result': '1',
                                                'team_name': name, 'pk': teams.pk}),
                                    content_type="application/json")
            else:
                return HttpResponse(json.dumps({'result': '-1',
                                                'message': "team didn't delete, {} and {} are different names".format(
                                                    confirm_team, teams.team_name)}),
                                    content_type="application/json")

    @staticmethod
    def add_team(request):
        if request.user.is_authenticated and request.is_ajax() and request.method == "POST":
            user = request.user
            team_name = (request.POST['team']).upper()
            team_name = team_name.lstrip().rstrip()
            team_filter = user.clubcell.team.filter(team_name=team_name)
            if team_filter.all().count() == 0:
                new_team = team(club=user.clubcell, team_name=team_name)
                new_team.save()
                if new_team.team_name == team_name:
                    return HttpResponse(json.dumps({'result': '1',
                                                    'team_name': new_team.team_name, 'pk': new_team.pk}),
                                        content_type="application/json")
            else:

                return HttpResponse(json.dumps({'result': '-1',
                                                'message': "Team {} already present".format(team_name)}),
                                    content_type="application/json")
            return HttpResponse(json.dumps({'result': '-1',
                                            'message': "Unable to create new team '{}'.".format(team_name)}),
                                content_type="application/json")

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
            if event.club.user == user:
                target_query = event_query.objects.get(pk=query, event=event)
                target_query.delete()
            return HttpResponse({})


class ClubLoadHtml:

    @staticmethod
    def queries_and_alerts(request):
        if request.user.is_authenticated and request.is_ajax() and request.method == "POST":
            user = request.user
            event_uen = request.POST['uen']
            event = events.objects.get(event_uen=event_uen)
            html = render_to_string('ajax/queries_and_alerts.html', {'user': user,
                                                                     'event': event,
                                                                     'event_query': event.event_query.filter(
                                                                         replied=None)
                                                                     },
                                    request=request)
            return HttpResponse(html)

    @staticmethod
    def messages_and_queries(request):
        if request.user.is_authenticated and request.is_ajax() and request.method == "POST":
            user = request.user
            uen = request.POST['uen']
            try:
                even_to = events.objects.get(event_uen=uen)
            except:
                even_to = None
            html = render_to_string('ajax/club_event_messages.html', {'user': user,
                                                                      'messages': GetData.distinct_messages(request,
                                                                                                            even_to),
                                                                      'uen': uen
                                                                      },
                                    request=request)
            return HttpResponse(html)

    @staticmethod
    def one_to_one_chat(request):  # for events message handling
        if request.user.is_authenticated and request.is_ajax() and request.method == "POST":
            user = request.user
            chat_to = request.POST['second_user']
            uen = request.POST['uen']
            try:
                event_to = events.objects.get(event_uen=uen)
                uen = event_to.eventname
            except:
                event_to = None
                uen = 'all'
            mstart = int(request.POST['mstart'])  # mstart and mend are the message slice range that we want to load
            mend = int(request.POST['mend'])
            chat_to_user = User.objects.get(username=chat_to)
            if uen == 'all':
                chats = (messages.objects.filter(user=chat_to_user, second_user=user).union(
                    messages.objects.filter(user=user, second_user=chat_to_user))).order_by(
                    'date_and_time')[::-1][
                        mstart:mend][::-1]
            else:
                chats = (messages.objects.filter(user=chat_to_user, second_user=user, event=event_to).union(
                    messages.objects.filter(user=user, second_user=chat_to_user, event=event_to))).order_by(
                    'date_and_time')[::-1][
                        mstart:mend][::-1]
            if len(chats) == 0:
                mend = -12
            html = render_to_string('ajax/msg_text_box.html', {'user': user,
                                                               'chats': chats,
                                                               'chat_to': chat_to_user,
                                                               'mstart': mstart + 12,
                                                               'mend': mend + 12,
                                                               'script_load': 'true'
                                                               },
                                    request=request)
            return HttpResponse(html)

    @staticmethod
    def receive_chat(request):
        if request.user.is_authenticated and request.is_ajax() and request.method == "POST":
            user = request.user
            uen = request.POST['event_to']
            chat_to = request.POST['second_user']
            chat_to_user = User.objects.get(username=chat_to)
            message_sent = request.POST['message']
            message_sent = message_sent.lstrip()
            if message_sent != '':
                try:
                    event = events.objects.get(event_uen=uen)
                except:
                    event = None
                now = timezone.now()
                new_msg = messages(user=user, second_user=chat_to_user, message_in=message_sent, date_and_time=now,
                                   event=event)
                new_msg.save()
                new_msg = messages.objects.filter(user=user, second_user=chat_to_user, message_in=message_sent,
                                                  date_and_time=now)

                html = render_to_string('ajax/msg_text_box.html', {'user': user,
                                                                   'chat_to': chat_to_user,
                                                                   'chats': new_msg,
                                                                   'mend': 0,
                                                                   'show_span': 0
                                                                   },
                                        request=request)
                return HttpResponse(html)
            return HttpResponse('')

    @staticmethod
    def get_new_message(request):
        if request.user.is_authenticated and request.is_ajax() and request.method == "POST":
            user = request.user
            chat_to = request.POST['second_user']
            gpk = request.POST['element'][2::]
            txt_len = int(request.POST['text'])
            chat_to_user = User.objects.get(username=chat_to)

            uen = request.POST['uen']
            try:
                event_to = events.objects.get(event_uen=uen)
                uen = event_to.eventname
            except:
                event_to = None
                uen = 'all'

            # now we will get if second user is typing or not and set if we are also typing
            second_typing = GetData.typing_message(txt_len, user, chat_to_user)
            if uen == 'all':
                chats = (messages.objects.filter(user=chat_to_user, second_user=user).union(
                    messages.objects.filter(user=user, second_user=chat_to_user))).order_by('date_and_time')
            else:
                chats = (messages.objects.filter(user=chat_to_user, second_user=user, event=event_to).union(
                    messages.objects.filter(user=user, second_user=chat_to_user, event=event_to))).order_by(
                    'date_and_time')
            last = chats.latest('date_and_time')
            if last.user == chat_to_user and last.seen == False:
                last.seen = True
                last.save()
            if last.pk == int(gpk):
                return HttpResponse(json.dumps("%dt" % second_typing), content_type="application/json")
            elif last.pk != int(gpk) and int(gpk) < last.pk and last.user != user:
                html = render_to_string('ajax/msg_text_box.html', {'user': user,
                                                                   'chat_to': chat_to_user,
                                                                   'chats': [last, ],
                                                                   'mend': 0,
                                                                   'show_span': 0
                                                                   },
                                        request=request)
                dict_data = {'result': 1, 'html': html, 'id': last.pk}
                return HttpResponse(json.dumps(dict_data), content_type="application/json")
            else:
                # return HttpResponse(json.dumps("-1"), content_type="application/json")
                return HttpResponse(json.dumps("-1"), content_type="application/json")
        else:
            return HttpResponse(json.dumps("unknown"), content_type="application/json")

    @staticmethod
    def load_event_group(request):
        if request.user.is_authenticated and request.is_ajax() and request.method == "POST":
            user = request.user
            group_id = request.POST['group_id']
            group_name = request.POST['group_name']
            if group_id == '0' and group_name == '0':
                groups = group_event.objects.filter(club=user.clubcell, parent_group=None)
                group = None
                path_directory = "/"
                pk = pname = ''
            else:
                group = group_event.objects.get(club=user.clubcell, pk=int(group_id), group_name=group_name)
                pk, pname = group.pk, group_name
                groups = group_event.objects.filter(club=user.clubcell, parent_group=group)
                temp_group = group
                path_directory = ("<a href='#' onclick=\"load_event_group('%s','%s')\">/%s</a>" % (
                temp_group.pk, temp_group.group_name, temp_group.group_name))
                while 1:
                    if temp_group.parent_group is None:
                        break
                    else:
                        temp_group = temp_group.parent_group
                        path_directory = ("<a href='#' onclick=\"load_event_group('%s','%s')\">/%s</a>" % (
                        temp_group.pk, temp_group.group_name, temp_group.group_name)) + path_directory

            html = render_to_string('ajax/groupevent.html', {'user': user,
                                                             'path_directory': path_directory,
                                                             'groups': groups,
                                                             'pk': pk,
                                                             'pname': pname,
                                                             'events_done': reversed(
                                                                 user.clubcell.events.filter(group_event=group))
                                                             },
                                    request=request)
            return HttpResponse(html)

    @staticmethod
    def create_event_group(request):
        if request.user.is_authenticated and request.is_ajax() and request.method == "POST":
            user = request.user
            parent_group = request.POST['parent_group']
            group_name = request.POST['group_name']
            if parent_group == '':
                pevent = None
            else:
                pk = request.POST['pk']
                pevent = group_event.objects.get(club=user.clubcell, pk=pk, group_name=parent_group)
            new_group = group_event(club=user.clubcell, group_name=group_name, parent_group=pevent)
            new_group.save()
            html = render_to_string('ajax/single_group.html', {'user': user,
                                                               'group': new_group,
                                                               },
                                    request=request)
            return HttpResponse(html)


class StudentLoadHtml:

    @staticmethod
    def profile_load_event(request):
        if request.user.is_authenticated and request.method == "POST" and request.is_ajax():
            user = request.user
            to_load = request.POST['to_load']
            if to_load == "wishlist":
                html = render_to_string('ajax/event_box.html', {'user': user,
                                                                'events': event_wishlist.objects.filter(user=user),
                                                                },
                                        request=request)
            elif to_load == "registered":
                html = render_to_string('ajax/event_box.html', {'user': user,
                                                                'events': event_participants.objects.filter(
                                                                    user=user),
                                                                },
                                        request=request)
            return HttpResponse(html)

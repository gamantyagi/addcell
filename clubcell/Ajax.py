from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from clubcell.models import events, event_participants, details, team, members, event_query
from django.http import HttpResponse
import sys
import csv
import json
from clubcell.ML import Logs
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
        if request.method == "GET" and request.user.is_authenticated:  # os request.GET()
            event_id = request.GET.get('element', None)
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

            html = render_to_string('ajax/club_event_messages.html', {'user': user,
                                                                     },
                                    request=request)
            return HttpResponse(html)

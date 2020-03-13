from django.shortcuts import render, redirect
from clubcell.models import clubcell, eventstodo
import sys
import csv
from clubcell.ML import Logs


class ClubCell:

    @staticmethod
    def render_dict(request):
        if request.user.is_authenticated:
            user = request.user
            user_message, msg_unseen = ClubCell.opendata("message", user)
            user_alert, alert_unseen = ClubCell.opendata("alert", user)
            cell = clubcell.objects.get(PAN=user.details.PAN)
            events = eventstodo.objects.filter(PAN=user.details.PAN)
            try:
                logs = Logs.get_logs(request)[-7:-1]
            except:
                logs = Logs.get_logs(request)
            return {'name': str(user.first_name + ' ' + user.last_name),
                    'main_class': 'ml-auto',
                    'cell': cell,
                    'events': reversed(events),
                    'messages': user_message,
                    'msg_unseen': str(msg_unseen),
                    'alerts': user_alert,
                    'alert_unseen': str(alert_unseen),
                    'logs': logs
                    }

    @staticmethod
    def open_dash(request):
        if request.user.is_authenticated:
            ren_dict = ClubCell.render_dict(request)

            return render(request, 'clubcell/dash.html', ren_dict)
        else:
            return render(request, 'clubcell/login.html', login_a)

    @staticmethod
    def profileview(request):
        if request.user.is_authenticated:
            return render(request, 'clubcell/profile.html', ClubCell.render_dict(request))
        else:
            return render(request, 'clubcell/login.html', login_a)

    @staticmethod
    def update(request):
        if request.user.is_authenticated:
            if request.method == 'POST':
                if request.POST['type'] == 'userupdate':
                    user=request.user
                    username = request.POST['username'].lower().lstrip()
                    first_name = (request.POST['first_name']).lower().lstrip()
                    last_name = (request.POST['last_name']).lower().lstrip()
                    email = request.POST['email'].lstrip()
                    if username!='' and first_name != '' and last_name != '' and email != '':
                        user.email, user.last_name, user.first_name, user.username = email, last_name, first_name, username
                        user.save()
                    return redirect('/Dashboard/profile')

                elif request.POST['type'] == 'cellupdate':
                    user = request.user
                    cell = clubcell.objects.get(PAN=user.details.PAN)
                    cellname = request.POST['cellname'].lower().lstrip()
                    offemail = (request.POST['offemail']).lower().lstrip()
                    about = (request.POST['about']).lower().lstrip()
                    tel = request.POST['tel'].lstrip()
                    cell.off_email, cell.clubname, cell.tel, cell.about = offemail, cellname, tel, about
                    cell.save();
                    return redirect('/Dashboard/profile')

            else:
                return redirect('Dashboard/profile')

        else:
            return redirect('/Dashboard/profile')

    @staticmethod
    def addevent(request):
        if request.user.is_authenticated:
            if request.method == 'POST':
                user = request.user
                eventname = request.POST['eventname']
                eventtype = request.POST['cat']
                season = request.POST['season']
                heldon = request.POST['heldon']
                event_UAP = str(request.POST['event_UAP']).upper()

                tags = request.POST['tags_info']

                breif_about = request.POST['breif_info']
                try:
                    paid = request.POST['paid']
                    fee = request.POST['fee']
                    paid = 'True'
                except:
                    paid = 'False'
                    fee = 0
                try:
                    certificate = request.POST['certificate']
                    certificate = 'True'
                    c_about = request.POST['certificate_about']
                except:
                    certificate = 'False'
                try:
                    duty_leave = request.POST['dl']
                    duty_leave = 'True'
                    dl_about = request.POST['dl_about']
                except:
                    duty_leave = 'False'

                event_id = generate('event@')
                event = eventstodo(PAN=user.details.PAN,event_id=event_id, eventname=eventname, eventtype=eventtype,
                                   season=season, heldon=heldon, breif_about=breif_about, tags=tags,
                                   paid=paid, fee=fee, certificate=certificate, dl=duty_leave, event_UAP=event_UAP)
                path = sys.path[0] + "\\media\\user\\" + user.details.PAN
                f1 = open((path + r"\{}.csv".format(event_id)), "w+")
                f1.write("is_registered,user_id,first_name,last_name,reg_no,email_id,phone_no,branch,course,highlight,"
                         "reason,gender,attended\n")
                f1.close()
                event.save();
                log_title = "added an event '{}'".format(eventname)
                Logs.put_in(request, log_title)
                return redirect('/')
            else:
                return render(request,'clubcell/addevent.html',ClubCell.render_dict(request))
        else:
            return render(request, 'clubcell/login.html')

    @staticmethod
    def mycell(request):
        if request.user.is_authenticated:
            return render(request, 'clubcell/mycell2.html', ClubCell.render_dict(request))
        else:
            return render(request, 'clubcell/login.html', login_a)

    '''this function is used to return the data like message, alert and many more.'''
    @staticmethod
    def opendata(datatype, user):
        path = sys.path[0]+"\\media\\user\\"+user.details.PAN+"\\"
        if datatype == 'message':
            fn = "message.csv"
        if datatype == 'alert':
            fn = "alert.csv"
        with open(path+fn, "r") as f:
            r = csv.reader(f)
            message_list = list(r)
        count = 0
        for row in message_list:
            if row[3] == 'no':
                count += 1
        return message_list[1::], count

    '''this method is used to give information of to do event and manuplate it.'''
    @staticmethod
    def event_todo_manuplate(request):
        if request.method == "GET" and request.user.is_authenticated:
            event_id = request.GET["i"]
            user = request.user
            try:
                event_detail = eventstodo.objects.get(event_id=event_id, PAN=user.details.PAN)
                path = sys.path[0] + "\\media\\user\\" + user.details.PAN + "\\" + event_id + ".csv"
                with open(path, 'r') as fb:
                    c = list(csv.reader(fb))
                members = list(filter(None, c))
                print(members)
                ren_dict = {"members": members[1::], "this_event": event_detail}
                ren_dict.update(ClubCell.render_dict(request))
                return render(request, 'clubcell/event_todo_table.html', ren_dict)
            except Exception as e:
                print(e)
                return redirect('/')

        return redirect('/')
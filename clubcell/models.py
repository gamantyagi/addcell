from django.contrib.auth.models import User
from versatileimagefield.fields import VersatileImageField
from django.shortcuts import redirect
from django.db import models
from .Constants import Paths
import sys
import os
import random
import string
import django
from django.utils import timezone
from PIL import Image


def get_upload_path(instance, filename):
    return os.path.join("media/user", instance.user.details.PAN)


def pan_generate():
    random_id = str()
    ch = list(string.ascii_letters + string.digits + '_')
    for i in range(100):
        random_id += random.choice(ch)
    return random_id


class details(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    PAN = models.CharField(max_length=100, unique=True, default=pan_generate)
    profile_pic = VersatileImageField(upload_to='profile_images', default='profile.jpg')
    gender = models.CharField(max_length=6, default="male")
    having_club = models.BooleanField(default=False)
    phone_no = models.CharField(max_length=13, default='+91')
    branch = models.CharField(max_length=20)
    course = models.CharField(max_length=20)
    reg_no = models.CharField(max_length=10)
    objects = models.Manager()

    def dp_small(self):
        img = Image.open(self.profile_pic)
        img.convert('RGB')
        img.thumbnail((10, 15))
        return img


class messages(models.Model):
    TEXT = 'T'
    IMAGE = 'I'
    AUDIO = 'A'
    VIDEO = 'V'
    MESSAGE_TYPE = [
        (TEXT, 'Text'),
        (IMAGE, 'Image'),
        (AUDIO, 'Audio'),
        (VIDEO, 'Video')
    ]
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    second_user = models.ForeignKey(User, related_name='second_user', on_delete=models.CASCADE, default=None)
    date_and_time = models.DateTimeField(default=django.utils.timezone.now)
    message_type = models.CharField(max_length=1, choices=MESSAGE_TYPE, default=TEXT)
    message_in = models.CharField(max_length=500)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return str(self.date_and_time) + str(self.message_in)

    def time_old(self):
        deadline = timezone.now() - self.date_and_time
        """seconds_t = deadline.total_seconds()
        minutes = (seconds_t % 3600) // 60
        seconds = seconds_t % 60"""
        days, seconds, = deadline.days, deadline.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        if days != 0:
            if days >= 7:
                show = '{} weeks'.format(int(days / 7))
            elif days == 1:
                show = '{} day'.format(days)
            else:
                show = '{} days'.format(days)
        elif hours != 0:
            show = '{} h'.format(hours)
        elif minutes != 0:
            show = '{} m'.format(minutes)
        else:
            show = '{} s'.format(seconds)
        return [show, days, hours, int(minutes), int(seconds)]

    def get_time(self):
        send_time = self.date_and_time
        date = send_time.date()
        date_now = timezone.now().date()
        if date == date_now:
            date = 'Today'
        time = send_time.time()
        return [time, date]


class typing_message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='typing_message')
    second_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='typing_message_2')
    typing = models.BooleanField(default=False)
    last_type = models.DateTimeField(default=django.utils.timezone.now)

    def last_type_time(self):
        deadline = timezone.now() - self.last_type
        return deadline.seconds / 1000


class alerts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alerts')
    second_user = models.ForeignKey(User, related_name='alert_second_user', on_delete=models.CASCADE, default=None)
    subject = models.CharField(max_length=120)
    date_and_time = models.DateTimeField(default=django.utils.timezone.now)
    alerts_in = models.CharField(max_length=1000)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return str(self.date_and_time) + str(self.subject)


class following(models.Model):
    user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    follower = models.ManyToManyField(User, related_name='follower')


class interest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interest = models.CharField(max_length=100)
    value = models.IntegerField(default=1)
    related_tags = models.CharField(max_length=1000)


class clubcell(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, related_name='clubcell')
    account_id = models.AutoField
    PAN = models.CharField(max_length=100, unique=True)
    clubname = models.CharField(max_length=30)
    off_email = models.CharField(max_length=100, default='')
    tel = models.CharField(max_length=12, default=91)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    verified = models.BooleanField(default=False)
    reputation = models.IntegerField(default=0)
    rating = models.DecimalField(default=0, max_digits=3, decimal_places=1)
    about = models.CharField(max_length=500)
    objects = models.Manager()

    def __str__(self):
        return self.clubname


class team(models.Model):
    club = models.ForeignKey(clubcell, on_delete=models.CASCADE, related_name='team')
    team_name = models.CharField(max_length=50)
    date = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return self.team_name

    def name_length(self):
        return len(self.team_name) * 29.9


class members(models.Model):
    HEAD = 'H'
    LEADER = 'L'
    CO_LEADER = 'CL'
    COORDINATOR = 'CN'
    CLUB_POST_LIST = [
        (HEAD, 'Head'),
        (LEADER, 'Leader'),
        (CO_LEADER, 'Co-Leader'),
        (COORDINATOR, 'Coordinator'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="members")
    club = models.ForeignKey(clubcell, on_delete=models.CASCADE)
    team = models.ForeignKey(team, on_delete=models.CASCADE, related_name='members')
    post = models.CharField(max_length=5, choices=CLUB_POST_LIST, default=COORDINATOR)


class group_event(models.Model):
    club = models.ForeignKey(clubcell, on_delete=models.CASCADE)
    group_name = models.CharField(max_length=100)

    def __str__(self):
        return self.group_name


class events(models.Model):
    DONE = 'D'
    PENDING = 'P'
    CANCELED = 'C'
    EVENT_SITUATION_CHOICE = [
        (DONE, 'Done'),
        (PENDING, 'Pending'),
        (CANCELED, 'Canceled'),
    ]
    WORKSHOP = 'WS'
    COMPETITION = 'CP'
    CONCERT = 'CC'
    EVENT_TYPE_CHOICE = [
        (WORKSHOP, 'Workshop'),
        (COMPETITION, 'Competition'),
        (CONCERT, 'Concert')
    ]
    ONLY_ME = 'OM'
    MEMBERS = 'MB'
    PUBLIC = 'PB'
    PRIVACY = [
        (ONLY_ME, 'Only Me'),
        (MEMBERS, 'Members of this club'),
        (PUBLIC, 'Public')
    ]
    club = models.ForeignKey(clubcell, on_delete=models.CASCADE, related_name='events')
    parent_event = models.ForeignKey(group_event, on_delete=models.CASCADE, blank=True)
    PAN = models.CharField(max_length=100)
    event_id = models.CharField(max_length=100, unique=True, default=pan_generate)
    event_uen = models.CharField(max_length=30, unique=True)
    eventname = models.CharField(max_length=100)
    session = models.IntegerField(default=1)
    members = models.IntegerField(default=0)
    attended = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    reviews = models.IntegerField(default=0)
    breif_about = models.CharField(max_length=90)
    event_detail = models.CharField(max_length=2000,
                                    default='<font size="12px" color="RED">detail of this event is not given</font>')
    eventtype = models.CharField(max_length=2, choices=EVENT_TYPE_CHOICE, default=WORKSHOP)
    tags = models.CharField(max_length=100)
    season = models.IntegerField(default=1)
    heldon = models.DateTimeField(max_length=20)
    paid = models.BooleanField(default=False)
    fee = models.IntegerField(default=0)
    certificate = models.BooleanField(default=False)
    privacy = models.CharField(max_length=2, choices=PRIVACY, default=PUBLIC)
    registration = models.BooleanField(default=True)
    dl = models.BooleanField(default=False)
    event_complete = models.CharField(max_length=1, choices=EVENT_SITUATION_CHOICE, default=PENDING)
    objects = models.Manager()

    def __str__(self):
        d = {'P': 'Pending...', 'C': 'Canceled!', 'D': 'Done'}
        return str(self.event_uen) + ' ' + str(d[self.event_complete])

    def time_old(self):
        deadline = self.heldon - timezone.now()
        days, seconds, = deadline.days, deadline.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        if days != 0:
            if days == 1:
                show = '{} day to go, be ready...'.format(days)
            else:
                show = '{} days to go'.format(days)
        else:
            show = 'event day, wish you best...'
        return [show, days, hours, int(minutes), int(seconds)]


class event_participants(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_participants')
    club = models.ForeignKey(clubcell, on_delete=models.CASCADE)
    events = models.ForeignKey(events, on_delete=models.CASCADE, related_name='event_participants')
    present = models.BooleanField(default=False)  # attendance of that event
    payment_done = models.BooleanField(default=False)
    payment_status = models.CharField(max_length=120, default='null')
    personal_info_access = models.CharField(max_length=1000, default="all,")
    highlight = models.BooleanField(default=False)
    highlight_reason = models.CharField(max_length=120, default='null')
    time = models.DateTimeField(default=django.utils.timezone.now)


class event_wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_wishlist')
    events = models.ForeignKey(events, on_delete=models.CASCADE, related_name='event_wishlist')
    time = models.DateTimeField(default=django.utils.timezone.now)


class review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(clubcell, on_delete=models.CASCADE)
    event = models.ForeignKey(events, models.CASCADE)
    rating = models.IntegerField
    review = models.CharField(max_length=1000)
    visible = models.BooleanField(default=False)
    vulgar = models.BooleanField(default=False)
    time = models.DateTimeField(default=django.utils.timezone.now)


class event_query(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="event_query")
    event = models.ForeignKey(events, on_delete=models.CASCADE, related_name="event_query")
    query = models.CharField(max_length=350)
    replied = models.ForeignKey('self', on_delete=models.CASCADE, related_name="event_query", blank=True, null=True, default=None)  # replied to which query
    replied_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="event_replied_query", blank=True, null=True, default=None)
    visible = models.BooleanField(default=False)
    time = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return self.query



class posts(models.Model):
    TEXT = 'T'
    IMAGE = 'I'
    VIDEO = 'V'
    POST_TYPE_CHOICE = [
        (TEXT, 'Text'),
        (VIDEO, 'Video'),
        (IMAGE, 'Image'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    club = models.ForeignKey(clubcell, on_delete=models.CASCADE)
    event = models.ForeignKey(events, on_delete=models.CASCADE, blank=True)
    post_type = models.CharField(max_length=1, choices=POST_TYPE_CHOICE, default=IMAGE)
    image = VersatileImageField(upload_to='posts/images', blank=True)
    video = models.FileField(upload_to='posts/videos', blank=True)
    text = models.CharField(max_length=200, blank=True)
    time = models.DateTimeField(default=django.utils.timezone.now)


class like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_liked = models.ForeignKey(posts, models.CASCADE)
    time = models.DateTimeField(default=django.utils.timezone.now)


class comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_commented = models.ForeignKey(posts, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    visible = models.BooleanField(default=True)
    time = models.DateTimeField(default=django.utils.timezone.now)


class General:

    @staticmethod
    def generate(constant):
        """ It generate random string, used for making unique ID's and PAN's for user"""
        random_id = str()
        ch = list(string.ascii_letters + string.digits + '_')
        random_len = 100 - len(constant)
        for i in range(random_len):
            random_id += random.choice(ch)
        random_id = constant + random_id
        return random_id


class Club:

    @staticmethod
    def having_permission(request):
        if request.user.is_authenticated and request.user.details.having_club:
            return True
        return False

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
        return redirect(Paths.CLUB_PROFILE_VIEW)

    @staticmethod
    def update_cell(request):
        if Club.having_permission(request) and request.method == "POST":
            user = request.user
            cell = clubcell.objects.get(user=user)
            cellname = request.POST['cellname'].lower().lstrip()
            offemail = (request.POST['offemail']).lower().lstrip()
            about = (request.POST['about']).lower().lstrip()
            tel = request.POST['tel'].lstrip()
            cell.off_email, cell.clubname, cell.tel, cell.about = offemail, cellname, tel, about
            cell.save();
        return redirect(Paths.CLUB_PROFILE_VIEW)

    @staticmethod
    def add_event_to_database(request):
        if Club.having_permission(request) and request.method == "POST":
            user = request.user
            eventname = request.POST['eventname']
            eventtype = request.POST['cat']
            season = request.POST['season']
            heldon = request.POST['heldon']
            event_UAP = str(request.POST['event_UAP']).upper()

            tags = request.POST['tags_info']

            breif_about = request.POST['breif_info']
            detail_about = request.POST['detail_info']
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
            parent = group_event.objects.get(group_name="MAIN", club=user.clubcell)
            event_id = General.generate('event@')
            event = events(club=user.clubcell, PAN=user.details.PAN, event_id=event_id, eventname=eventname,
                           eventtype=eventtype,
                           season=season, heldon=heldon, breif_about=breif_about, tags=tags,
                           paid=paid, fee=fee, certificate=certificate, dl=duty_leave, event_uen=event_UAP,
                           event_detail=detail_about, parent_event=parent)
            event.save()
        return redirect(Paths.EVENT_TODO_MAIN)

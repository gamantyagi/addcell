from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from clubcell.models import clubcell, details
from django.contrib import messages
from .Common import InCSV, Received
from .Constants import Paths
import random
import string
import os
from django.utils import timezone


class GoTo:

    @staticmethod
    def redirect_to(path):
        return redirect(path)

    @staticmethod
    def render_page(request, page, rending_dict=None):
        return render(request, page, rending_dict)

    @staticmethod
    def landing_page():
        return redirect(Paths.HOMEPAGE)


class General:

    @staticmethod
    def get_remaining_time(last_time):
        deadline = timezone.now() - last_time
        seconds_t = deadline.total_seconds()
        minutes = (seconds_t % 3600) // 60
        seconds = seconds_t % 60
        return [int(minutes), int(seconds)]

    @staticmethod
    def login_by_request(request):
        if request.method == 'POST':
            username = request.POST['username'].lower()
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return True
        return False

    @staticmethod
    def login_by_parameter(request, username=None, password=None):
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return True
        return False

    @staticmethod
    def logout_user(request):
        logout(request)
        return True

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

    @staticmethod
    def signup(request):
        """ This is used to register new users"""
        if request.method == 'POST':
            # Return dict having key and value of HTML inputs form
            request_data = Received.receive_post_data(request)
            try:
                # when we send checkbox input in form it has value 'on' otherwise no value
                request_data['having_club'] = bool(request_data['having_club'])
            except KeyError:
                request_data['having_club'] = False
            # we will create a new user in system and add it to User database
            user = User.objects.create_user(username=request_data['uname'],
                                            email=request_data['email'],
                                            password=request_data['pword1'],
                                            first_name=request_data['fname'],
                                            last_name=request_data['lname'])
            user.save()
            user_details = details(user=user, PAN=General.generate("user@"),
                                   profile_pic="default.jpg",
                                   having_club=request_data['having_club'],
                                   reg_no=request_data['reg_no'],
                                   phone_no=request_data['phone'],
                                   branch=request_data['branch'],
                                   course=request_data['course'],
                                   gender=request_data['Gender'])

            user_details.save()
            if request_data['having_club'] == "True":
                cell = clubcell(user=user, clubname="club"+request_data['uname'])
                cell.save()
            # all user data will be saved in a directory having name same as user PAN (permanent account number)
            user_file_path = os.path.join(Paths.USER_DATA_PATH, user_details.PAN)
            os.mkdir(user_file_path)
            if General.login_by_parameter(request, request_data['uname'], request_data['pword1']):
                return True
        # if user registration failed or request method is not POST  ( if user just open signup page)
        return False

    @staticmethod
    def message_response(request, **kwrgs):
        if request.method == kwrgs['if_method']:
            messages.info(request, kwrgs['alert'])

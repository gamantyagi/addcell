from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.conf.urls.static import static

login_a = {'signup_path': 'signup', 'l_b_active': 'btn btn-light action-button', 's_b_active': 'text-white-50 login'}
signup_a = {'signup_path': '', 'l_b_active': 'text-white-50 login', 's_b_active': 'btn btn-light action-button'}


def home(request):
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("Dashboard/")
        else:
            messages.info(request, 'Wrong username or password')
            return redirect('/')
    else:
        if request.user.is_authenticated:
            return redirect('Dashboard/')
        else:
            return render(request, 'studentcell/login.html', login_a)

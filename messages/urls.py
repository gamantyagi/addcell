from django.conf.urls import include, url
from . import views
from django.urls import path

urlpatterns = [
    path('chat/<str:message_to>', views.chat, name='HomePage'),
    #url(r'^$',  views.ViewTests.test_about, name='about'),
    #url(r'^new/$', views.ViewTests.test_new_room, name='new_room'),
    #url(r'^(?P<label>[\w-]{,50})/$', views.ViewTests.test_chat_room, name='chat_room'),
]
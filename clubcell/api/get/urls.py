from django.conf.urls import url
from clubcell.api.get import views, post_view
from clubcell.api.get import message_views

urlpatterns = [
    url(r'^check-username/(?P<username>[\w-]+)/$', views.Check_Username.as_view(), name="check-username"),
    url(r'^create-user', views.CreateUserSerializer.as_view(), name="create-user"),
    url(r'^user/$', views.Users.as_view(), name="list"),
    url(r'^basicuser/$', views.BasicUsers.as_view(), name="list"),
    url(r'^user/all-messages/$', message_views.AllMessages.as_view(), name="messages"),
    url(r'^user/messages/(?P<chat_to>[\w-]+)/$', message_views.Messages.as_view(), name="messages"),
    url(r'^user/posts/all', post_view.AllPosts.as_view(), name="messages"),
    url(r'^user/(?P<pk>[\w-]+)/$', views.UserDetail.as_view(), name="retrieve"),
]


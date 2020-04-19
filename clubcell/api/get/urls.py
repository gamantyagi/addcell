from django.conf.urls import url
from clubcell.api.get import views

urlpatterns = [
    url(r'^user/$', views.Users.as_view(), name="list"),
    url(r'^basicuser/$', views.BasicUsers.as_view(), name="list"),
    url(r'^user/(?P<pk>[\w-]+)/$', views.UserDetail.as_view(), name="retrieve"),
]


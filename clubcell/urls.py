from django.urls import path
from . import views, Ajax, models, student
urlpatterns = [
    path('', views.Entry.homepage, name='HomePage'),
    path('login/', views.Entry.login, name='Login'),
    path('signup/', views.Entry.signup, name='Signup'),
    path('logout/', views.Entry.logout, name='logout'),

    path('club/dashboard/', views.Club.home, name='Dashboard'),

    path('club/profile/', views.Club.profile_view, name='Dashboard'),
    path('club/addevent/', views.Club.add_event, name='Add Event'),
    path('club/mycell/', views.Club.my_cell, name='Mycell'),
    #path('update/bprofile/', views.ClubCell.update, name="Update"),
    path('club/eventtodo/<str:event_uen>', views.Club.event_todo_main, name="eventToDo"),
    path('club/eventtodo/', views.Club.events_todo, name="eventToDo"),
    path('club/eventdone/', views.Club.event_done, name="eventToDo"),
    path('club/members', views.Club.members, name="eventToDo"),
    path('club/posts', views.Club.posts, name="eventToDo"),
    path('club/addcells', views.Club.addcells, name="eventToDo"),
    path('club/trending', views.Club.trending, name="eventToDo"),
    path('club/update/profile/', models.Club.update_profile, name="eventToDo"),
    path('club/update/cell/', models.Club.update_cell, name="eventToDo"),
    path('club/addevent/add/', models.Club.add_event_to_database, name="eventToDo"),

    path('club/ajax/show_event_public/', Ajax.Ajax.show_event, name="eventToDo"),
    path('club/ajax/addmember', Ajax.Club.add_member, name="add member to club"),
    path('club/ajax/editteam', Ajax.Club.edit_team, name="add member to club"),
    path('club/ajax/dltteam', Ajax.Club.delete_team, name="add member to club"),
    path('club/ajax/addteam', Ajax.Club.add_team, name="add member to club"),
    path('club/ajax/load/queries', Ajax.ClubLoadHtml.queries_and_alerts, name="load queries"),
    path('club/ajax/load/messages', Ajax.ClubLoadHtml.messages_and_queries, name="load messages"),
    path('student/ajax/ajax_event_register/', Ajax.Ajax.event_register, name="eventToDo"),

    path('student/home/', views.Student.home, name='Events'),
    path('student/profile/', views.Student.profile, name='profile'),
    path('student/explore/', views.Student.home, name='explore'),
    path('student/posts/', views.Student.posts, name='explore'),

    path('event/askquery', student.Student.ask_event_query, name="ask event query"),
    path('event/dltquery', student.Student.dlt_event_query, name="dlt event query"),

    path('event/askqueryc', Ajax.Club.ask_event_query, name="ask event query club"),
    path('event/dltqueryc', Ajax.Club.dlt_event_query, name="dlt event query club"),

    path('event/<str:event_uen>/', views.CommonMethod.view_event_detail, name='event display'),
    path('messages/chat/<str:chat_to>/', views.Message.chat, name='check'),
    path('messages/get_new/<str:chat_to>/', views.Message.get_new_message, name='check'),

    path('signup/ajax_username_valid/', Ajax.Ajax.validate_username, name='check'),
    #path('Dashboard/ajax_show_event/', views.Ajax.show_event, name='check'),
    #path('ajax_event_register/', views.Ajax.event_register, name='check')

]

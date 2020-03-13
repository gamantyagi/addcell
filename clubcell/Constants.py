import os
import sys


class Paths:
    HOMEPAGE = "/"
    LOGIN = "login/"
    SIGNUP = "signup/"
    CLUB_HOME = "club/dashboard/"
    STUDENT_HOME = "student/home"
    CLUB_PROFILE_VIEW = "/club/profile/"
    CLUB_MEMBERS = "/club/members"
    EVENT_TODO_MAIN = '/club/eventtodo/'
    USER_DATA_PATH = os.path.join(sys.path[0], "media", "user")


class Pages:
    LOGIN = "clubcell/login.html"
    SIGNUP = "clubcell/signup.html"
    CLUB_HOME = "clubcell/dash.html"
    CLUB_PROFILE_VIEW = "clubcell/profile.html"
    CLUB_MEMBERS = "clubcell/members.html"
    CLUB_POSTS = "clubcell/posts.html"
    CLUB_ADDCELLS = "clubcell/addcells.html"
    CLUB_TRENDING = "clubcell/trending.html"
    STUDENT_HOME = "studentcell/shome.html"
    STUDENT_PROFILE = 'studentcell/sprofile.html'
    STUDENT_POSTS = 'studentcell/sposts.html'
    CLUB_MY_CELL = "clubcell/mycell2.html"
    ClUB_ADD_EVENT = "clubcell/addevent.html"
    CLUB_EVENT_DETAIL = "clubcell/event_show.html"
    CHAT_PANEL = 'common/message_chat.html'
    EVENT_TODO_MAIN = 'clubcell/event_todo_table.html'
    EVENTS_TODO = 'clubcell/events_todos.html'
    EVENTS_DONE = 'clubcell/event_done.html'


class Alerts:
    LOGIN_FAILED_MESSAGE = "Username or Password is wrong"
    SIGNUP_FAILED_MESSAGE = "User registration failed...Please try again."
    NOTHING = ''

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import details, clubcell, events, messages, alerts, members, review, posts, like, comments, \
    event_participants
from .models import following, interest, team, group_event, event_query


class detailsInline(admin.StackedInline):
    model = details
    can_delete = False
    verbose_name_plural = 'details'


class alertsInline(admin.StackedInline):
    model = alerts
    can_delete = False
    fk_name = 'user'
    verbose_name_plural = 'allerts'


class messagesInline(admin.StackedInline):
    model = messages
    can_delete = False
    fk_name = 'user'
    verbose_name_plural = 'messages'


class membersInline(admin.StackedInline):
    model = members
    can_delete = False
    verbose_name_plural = 'members'


class followingInline(admin.StackedInline):
    model = following
    can_delete = False
    verbose_name_plural = 'followings'


class interestInline(admin.StackedInline):
    model = interest
    can_delete = False
    verbose_name_plural = 'interests'


class groupeventInline(admin.StackedInline):
    model = group_event
    can_delete = False
    verbose_name_plural = 'event groups'


class eventsInline(admin.StackedInline):
    model = team
    can_delete = False
    verbose_name_plural = 'teams'


class teamInline(admin.StackedInline):
    model = events
    can_delete = False
    verbose_name_plural = 'events'


class eventparticipantInline(admin.StackedInline):
    model = event_participants
    can_delete = False
    verbose_name_plural = 'registered events'


class postsInline(admin.StackedInline):
    model = posts
    can_delete = True
    verbose_name_plural = 'posts'


class event_queryInline(admin.StackedInline):
    model = event_query
    can_delete = True
    verbose_name_plural = 'posts'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (detailsInline, membersInline, followingInline, interestInline,)


@admin.register(clubcell)
class clubAdmin(admin.ModelAdmin):
    list_display = ('clubname', 'user', 'off_email',)
    ordering = ('clubname',)
    search_fields = ('clubname', 'user',)
    inlines = (eventsInline, groupeventInline, membersInline, teamInline,)


@admin.register(events)
class clubAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'club',)
    ordering = ('event_uen',)
    search_fields = ('event_uen', 'club',)
    inlines = (eventparticipantInline, postsInline)


"""@admin.register(events)
class clubAdmin(admin.ModelAdmin):
    list_display = ('clubname', 'user.username','off_email',)
    ordering = ('clubname',)
    search_fields = ('clubname', 'user',)
    inlines = (membersInline, eventsInline,)
"""

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# admin.site.register(clubcell)
# admin.site.register(events)
admin.site.register(posts)
admin.site.register(event_query)

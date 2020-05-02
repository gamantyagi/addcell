import json
import operator

from clubcell.models import messages


def distinct_messages(request, event_to=None):
    if request.user.is_authenticated:
        user = request.user
        if event_to == "all":
            second_users = (messages.objects.filter(user=user).values('second_user').union(
                messages.objects.filter(second_user=user).values('user')))
            msg_query = {"messages": []}
            chats = set()
            unseen_msg = 0
            for second_user in second_users:
                chat = \
                    (messages.objects.filter(user=second_user['second_user'], second_user=user).union(
                        messages.objects.filter(user=user, second_user=second_user['second_user']))).order_by(
                        'date_and_time').reverse()[0]
                if not chat.seen and chat.user != user:
                    unseen_msg += 1
                chats.add(chat)
            chats = reversed(sorted(chats, key=operator.attrgetter('date_and_time')))
            for i, chat in enumerate(chats):
                if chat.user == user:   profile_pic = chat.get_profile_pic_second_user()
                else:   profile_pic = chat.get_profile_pic_user()
                msg_query["messages"].append([str(i),
                                              str(chat.user.username),
                                              str(chat.second_user.username),
                                              str(chat.message_in),
                                              str(chat.time_old()),
                                              str(chat.seen),
                                              str(profile_pic)])
            msg_query.update({"unseen": unseen_msg})
            return msg_query

        else:
            second_users = (messages.objects.filter(user=user, event=event_to).values('second_user').union(
                messages.objects.filter(second_user=user, event=event_to).values('user')))
            msg_query = set()
            unseen_msg = 0
            for second_user in second_users:
                chat = \
                    (messages.objects.filter(user=second_user['second_user'], second_user=user, event=event_to).union(
                        messages.objects.filter(user=user, second_user=second_user['second_user'],
                                                event=event_to))).order_by('date_and_time').reverse()[0]
                if not chat.seen and chat.user != user:
                    unseen_msg += 1
                msg_query.add(chat)
            if unseen_msg == 0:
                unseen_msg = ''
            msg_query_n = reversed(sorted(msg_query, key=operator.attrgetter('date_and_time')))
            return {'messages': msg_query_n, 'unseen_count': unseen_msg,
                    'first': sorted(msg_query, key=operator.attrgetter('date_and_time'))[-1]}

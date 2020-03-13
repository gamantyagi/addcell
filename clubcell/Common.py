import operator

from django.utils import timezone

from clubcell.models import clubcell, events, details, User, events, messages, typing_message
from .Constants import Paths
import os
import csv
import pickle


def create_objects(**objects_dict):
    class VirtualClass:
        pass
    for key in objects_dict.keys():
        exec("VirtualClass.%s = '%s'" % (key, objects_dict[key]))
    return VirtualClass


class GetData:

    @staticmethod
    def is_user_having_club(request):
        return request.user.details.having_club

    @staticmethod
    def users_club_detail(user):
        club_detail = clubcell.objects.get(PAN=user.details.PAN)
        return club_detail

    @staticmethod
    def users_events_todo(user):
        events_todo = reversed(events.objects.filter(PAN=user.details.PAN))
        return events_todo

    @staticmethod
    def users_messages(user):
        file_path = os.path.join(Paths.USER_DATA_PATH, user.details.PAN)
        return InCSV.read_csv_dict(file_path, 'message.csv')

    @staticmethod
    def users_alerts(user):
        file_path = os.path.join(Paths.USER_DATA_PATH, user.details.PAN)
        return InCSV.read_csv_dict(file_path, 'alert.csv')

    @staticmethod
    def users_info(user):
        # this function use pickle to store users info in object form
        pickle_in = open(os.path.join(Paths.USER_DATA_PATH,user.details.PAN, 'info.pickle'), "rb")
        return pickle.load(pickle_in)

    @staticmethod
    def all_upcoming_events(*args):
        return reversed(events.objects.filter(show_public=True))

    @staticmethod
    def users_registered_events(user):
        return InCSV.read_csv_list_lines(os.path.join(Paths.USER_DATA_PATH, user.details.PAN), 'event_registered.csv')

    @staticmethod
    def load_event_by_uen(event_uen):
        return events.objects.get(event_UAP=event_uen)

    @staticmethod
    def load_event_by_id(event_id):
        return events.objects.get(event_id=event_id)

    @staticmethod
    def load_user_by_uen(event_uen):
        event_detail = events.objects.get(event_UAP=event_uen)
        return details.objects.get(PAN=event_detail.PAN)

    @staticmethod
    def load_user_by_username(username):
        return User.objects.get(username=username)

    @staticmethod
    def users_events_done(user):
        return events.objects.filter(PAN=user.details.PAN)

    @staticmethod
    def distinct_messages(request):
        if request.user.is_authenticated:
            user = request.user
            second_users = (messages.objects.filter(user=user).values('second_user').union(messages.objects.filter(second_user=user).values('user')))
            msg_query = set()
            unseen_msg = 0
            for second_user in second_users:
                chat = (messages.objects.filter(user=second_user['second_user'], second_user=user).union(
                    messages.objects.filter(user=user, second_user=second_user['second_user']))).order_by('date_and_time').reverse()[0]
                if not chat.seen and chat.user != user:
                    unseen_msg += 1
                msg_query.add(chat)
            if unseen_msg == 0:
                unseen_msg = ''
            msg_query = reversed(sorted(msg_query, key=operator.attrgetter('date_and_time')))
            return {'messages': msg_query, 'unseen_count': unseen_msg}

    @staticmethod
    def typing_message(txt_len, user, user_to):
        try:
            typing_model = typing_message.objects.get(user=user, second_user=user_to)
        except:
            typing_model = typing_message(user=user, second_user=user_to, typing=False)
            typing_model.save()
        try:
            second_typing = typing_message.objects.get(user=user_to, second_user=user)
        except:
            second_typing = typing_message(user=user_to, second_user=user, typing=False)
            second_typing.save()
        user_typing = 0
        if second_typing.typing and int(second_typing.last_type_time()) < 1.2:
            user_typing = 1
            second_typing.typing = False
            second_typing.save()
        if txt_len > 0:
            typing_model.typing = True
            typing_model.last_type = timezone.now()
            typing_model.save()
        elif txt_len == 0:
            typing_model.typing = False
            typing_model.save()
        return user_typing

class InCSV:

    @staticmethod
    def write_csv(path, csv_name, data):
        with open(os.path.join(path, csv_name), 'a+') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(data)

    @staticmethod
    def write_multiple_csv(path, csv_names_list, data_list):
        for csv_name, data in zip(csv_names_list, data_list):
            InCSV.write_csv(path, csv_name, data)

    @staticmethod
    def read_csv_dict(path, csv_name):
        with open(os.path.join(path, csv_name)) as csv_file:
            dict_object = csv.DictReader(csv_file)
            csv_data = list(dict_object)
        return csv_data

    @staticmethod
    def read_csv_list_lines(path, csv_name):
        with open(os.path.join(path, csv_name), 'r') as file:
            event_register = file.read().splitlines()
        return event_register

    @staticmethod
    def write_pickle(path, name, data):
        with open(os.path.join(path, name), 'wb') as pickle_file:
            pickle.dump(data, pickle_file)
            

class Rendering:
    """ It gives the data required for rendering the Html page
    """

    @staticmethod
    def render_data(request, page_title=None, *queries):
        final_dict = {}
        if page_title is not None:
            final_dict["pageTitle"] = page_title
        user = request.user
        for query in queries:
            # exec() function is used to execute the statement present in it.
            # we are calling functions that having name same as the string value of query
            # for eg. if query = "username", we are calling username(user) and this function returns some value
            # we are adding that returned value to the final_dict dictionary by using update.
            exec("final_dict.update({'%s': GetData.%s(user)})" % (query, query))
        return final_dict

    @staticmethod
    def club_data_plus(request, page_title=None):
        """ This method is used to add some common values along with queries"""
        common_data = Rendering.render_data(request, page_title,
                                            'users_club_detail',
                                            'users_events_todo',
                                            'users_messages',
                                            'users_alerts',
                                            'users_events_done'
                                            )
        return common_data


class Received:
    """ It receives data from Html request and make it into dictionary having key as name of input
        and value as input value.
        :receive_post_data(request), used for getting values from POST method of request.
        :receive_get_data(request), receive data from GET method of request.
        """

    @staticmethod
    def receive_post_data(request):
        return {key: value for key, value in request.POST.items()}

    @staticmethod
    def receive_get_data(request):
        return {key: value for key, value in request.GET.items()}

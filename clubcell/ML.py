
import sys
import csv
from datetime import datetime


class Logs:

    @staticmethod
    def read_logs(request):
        if request.user.is_authenticated:
            if request.user.details.having_club:
                path = sys.path[0] + "\\media\\user\\" + request.user.details.PAN + "\\logs.csv"
                with open(path, 'r') as file:
                    return list(csv.reader(file))

    @staticmethod
    def get_logs(request,start=1, ends=-1):
        if request.user.is_authenticated:
            if request.user.details.having_club:
                logs = list(filter(None, Logs.read_logs(request)))
                return logs[start:ends]

    @staticmethod
    def put_in(request, log_title, log_detail="No available", suggestion="No suggestion"):
        if request.user.is_authenticated:
                path = sys.path[0] + "\\media\\user\\" + request.user.details.PAN + "\\logs.csv"
                with open(path, 'a+') as file:
                    add_row = csv.writer(file)
                    name = request.user.first_name + " " + request.user.last_name
                    username = request.user.username
                    add_row.writerow([datetime.now().strftime("%d/%m/%Y %H:%M:%S"), name, username, log_title,
                                      log_detail, suggestion])
                return 0

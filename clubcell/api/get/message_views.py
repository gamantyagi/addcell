import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from clubcell.models import User, messages
from .common import distinct_messages
from .serializers import UserSerializer, MessageSerializer
from rest_framework.response import Response
from rest_framework import status, permissions, serializers
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from django.contrib.auth.hashers import make_password


class AllMessages(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        inbox = distinct_messages(request, 'all')
        return Response(inbox)


class Messages(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, chat_to):
        user = request.user
        chat_to_user = User.objects.get(username=chat_to)
        chats = (messages.objects.filter(user=chat_to_user, second_user=user).union(
            messages.objects.filter(user=user, second_user=chat_to_user))).order_by('date_and_time')[::-1][0:100][
                ::-1]
        serializer = MessageSerializer(chats, many=True)
        return Response(serializer.data)

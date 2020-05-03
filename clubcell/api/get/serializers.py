from abc import ABC

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from clubcell.models import messages, posts


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "password"]
        extra_kwargs = {'password': {'write_only': True}}


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = messages
        fields = ["user", "second_user", "message_in", "seen", "time_old"]


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = posts
        fields = ["get_username", "get_clubname", "get_eventname", "get_likes", "get_views", "get_small_image", "get_original_image"]

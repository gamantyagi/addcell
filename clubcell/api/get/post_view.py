from rest_framework.views import APIView

from clubcell.models import User, messages, posts
from .common import distinct_messages
from .serializers import UserSerializer, MessageSerializer, PostSerializer
from rest_framework.response import Response
from rest_framework import status, permissions, serializers
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class AllPosts(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        post = posts.objects.all()
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)
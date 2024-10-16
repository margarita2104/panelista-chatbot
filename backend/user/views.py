from django.contrib.auth import get_user_model
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from backend.user.serializers import UserSerializer


class ListCreateUsersView(ListCreateAPIView):
    serializer_class = UserSerializer


class RetrieveUpdateDestroyUsersView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer

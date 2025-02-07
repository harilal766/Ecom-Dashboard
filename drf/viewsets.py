from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.contrib.auth.models import User
from .serializers import UserSerializer


# Create your views here.
class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
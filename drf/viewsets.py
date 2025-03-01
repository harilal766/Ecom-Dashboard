from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.contrib.auth.models import User
from .serializers import UserSerializer,StoreSerializer

from dashboard.d_models import StoreProfile

# Create your views here.
class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class StoreViewSet(ReadOnlyModelViewSet):
    queryset = StoreProfile.objects.all()
    serializer_class = StoreSerializer
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from drf.viewsets import UserViewSet


router = DefaultRouter()
router.register(r'user',UserViewSet)


urlpatterns =[
    path('api/',include(router.urls)),
]
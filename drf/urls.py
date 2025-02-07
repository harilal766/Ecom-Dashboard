from django.urls import path,include
from rest_framework.routers import DefaultRouter
from drf.viewsets import UserViewSet,StoreViewSet


router = DefaultRouter()
router.register(r'users',UserViewSet)
router.register(r'stores',StoreViewSet)


urlpatterns =[
    path('api/',include(router.urls)),
]
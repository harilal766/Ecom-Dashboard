from django.urls import path
from user.views import *

app_name = 'user'

urlpatterns =[
    path('register',register,name='register'),
    path('login',auth_login,name='login'),
    path('logout',auth_logout,name='logout'),
]
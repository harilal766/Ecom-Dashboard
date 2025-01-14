from django.urls import path
from user import views


app_name = 'user'

urlpatterns =[
    path('register',views.register,name='register'),
    path('login',views.auth_login,name='login'),
    path('logout',views.auth_logout,name='logout'),
]
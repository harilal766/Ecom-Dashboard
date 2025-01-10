from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from sales.views import home 
import re
from helpers.messages import *
# Create your views here.

username_pattern = r"^[a-zA-Z]{6-12}$"
password_pattern = r"\d{8-15}"


auth_context = {"purpose" : None, 
                "form" : None,
                "button_text": None
                }

def register(request):
    auth_context["purpose"] = "Sign up"
    auth_context["button_text"] = "Register"
    if request.method == "POST":
        register_form = UserCreationForm(request.POST)
        if register_form.is_valid():
            form.save()
            return 
    # credentials : username, password, email, confirm password
    return render(request,"authorization/auth_form.html",auth_context)

def login(request):
    pass
    # credentials needed to login : username, password

def logout(request):
    pass


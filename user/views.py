from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from user.forms import Userform
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
    auth_context["purpose"] = "signup"
    auth_context["button_text"] = "Register"
    if request.method == "POST":
        register_form = Userform(request.POST)
        if register_form.is_valid():
            register_form.save()
            auth_context["form"] = register_form
            return redirect("home")
    # credentials : username, password, email, confirm password
    return render(request,"authorization/auth_form.html",auth_context)

def login(request):
    auth_context["purpose"] = "signin"; auth_context["button_text"] = "Login"
    return render(request,"authorization/auth_form.html",auth_context)
    # credentials needed to login : username, password

def logout(request):
    pass


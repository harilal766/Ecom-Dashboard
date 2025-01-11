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
    """
    if the password is strong username and email is not taken already,
        the code should check if it matches with confirm password
        if yes, the user can be created
    """
    purpose_text = "Sign-Up"
    auth_context["purpose"] = purpose_text
    auth_context["button_text"] = "Register"
    if request.method == "POST":
        # request.POST.get("")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password == confirm_password:
            user = User.objects.create_user(username=username,password=password)
            user.save()

            color_text("User Created")
            return home
        else:
            color_text(message="The passwords doesnt match",color="red")

        print(request.POST)
    # credentials : username, password, email, confirm password
    return render(request,"authorization/auth_form.html",auth_context)

def login(request):
    purpose_text = "Sign-In"
    auth_context["purpose"] = purpose_text; 
    auth_context["button_text"] = "Login"
    return render(request,"authorization/auth_form.html",auth_context,)
    # credentials needed to login : username, password

def logout(request):
    pass


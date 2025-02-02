from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,  login,  logout
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from user.forms import Userform
from sales.views import dashboard 
import re
from helpers.messages import *

# Create your views here.

username_pattern = r"^[a-zA-Z]{6-12}$"
password_pattern = r"\d{8-15}"


auth_context = {"purpose" : None, 
                "form" : None,
                "button_text": None,
                "auth_status" : None,
                }

# make a temporary user and filter based on this.


# finding created usernames for verification, email also should be verified this way
def usernames():
    users = User.objects.all()
    usernames = []
    for user in users:
        usernames.append(user.username)
    return usernames

def emails():
    pass

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

        # username verification
        emails = []
        if username not in usernames():

            # email verification, for future use
            if email not in emails:
                pass

            # password verificaion
            if password == confirm_password:
                user = User.objects.create_user(username=username,password=password)
                user.save()
                color_text("User Created")
                return redirect("sales:home")
                #return home
            else:
                color_text(message="The passwords doesn't match",color="red")

        else:
            auth_context["auth_status"] = "username already exists"
            color_text(message=f"Username {username} already exists.",color="red")
    # credentials : username, password, email, confirm password
    return render(request,"authorization/auth_form.html",auth_context)

def auth_login(request):
    purpose_text = "Sign-In"
    auth_context["purpose"] = purpose_text; 
    auth_context["button_text"] = "Login"

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request,username = username, password = password)
        if not user == None:
            login(request,user)
            color_text(message=f"User : {user} signed in.")
            return redirect("sales:home")
        else:
            color_text(message="unable to login",color="red")
        
    return render(request,"authorization/auth_form.html",auth_context,)
    # credentials needed to login : username, password

def auth_logout(request):
    logout(request)
    return redirect("sales:home")


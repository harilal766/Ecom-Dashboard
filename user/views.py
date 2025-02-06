from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,  login,  logout
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from user.forms import Loginform
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
    try:
        if request.method == "POST":
            form = Loginform(request.POST)
            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]

                color_text(username,password)

                user = authenticate(request,username = username,
                                    password = password)
                
                if not user == None:
                    login(request,user)
                    return redirect('sales:home')
                else:
                    color_text(form.add_error(None,"Login failed"))
        else:
            form = Loginform()
    except Exception as e:
        better_error_handling(e)

        
    return render(request,"authorization/auth_form.html",{"form":form})
    # credentials needed to login : username, password

def auth_logout(request):
    logout(request)
    return redirect("sales:home")


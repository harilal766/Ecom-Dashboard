from django.shortcuts import render
from django.contrib.auth.models import User
from sales.views import home 
import re
from helpers.messages import *
# Create your views here.

username_pattern = r"^[a-zA-Z]{6-12}$"
password_pattern = r"\d{8-15}"


def register(request):
    # credentials : username, password, email, confirm password
    context = {"purpose": "Signup" , "status":None, "register": True, "login": None}
    if request.method == 'POST':
        client_username = request.POST["username"]
        client_password = request.POST["password"]
        if client_username and client_password:
            # make sure credentials matches the patterns
            if re.match(username_pattern,client_username) and re.match(password_pattern,client_password):
                user = User.objects.create_user(username = client_username,
                                                password = client_password)
                if user:
                    user.save()
                    context["status"] = "Successfull"
                    return home(request)
            else:
                context["status"] = "Invalid credentials"
        elif len(client_username) == 0 or len(client_password) == 0:
            context["status"] = "Empty credentials!"
    color_text(message=f"Signup Status : {context['status']}")
    return render(request,"authorization/signup.html",context)

def login(request):
    context = {"purpose": "Signup" , "status":None, "register": None, "login": True}
    # credentials needed to login : username, password

def logout(request):
    pass


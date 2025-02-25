from django.shortcuts import render,redirect
from amazon.response_manipulator import amazon_dashboard
from amazon.response_manipulator import *
from amazon.sp_api_utilities import *
from amazon.sp_api_models import Orders,Reports
from datetime import datetime,timedelta
from helpers.sql_scripts import *
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


from django.contrib.auth.decorators import login_required


# Create your views here.    
# create a common context for amazon which can be saved to a json file later

"""
    Home page will display the shipments summary.
    and it will contain the form whiich will trigger the 
    function for report generation.
"""

# Current logged in user
from amazon.report_types import selected_report_types

def stores():
    stores = Store.objects.all()
    stores_name_list = []
    for store in stores:
        stores_name_list.append(store.store_name)
    return stores_name_list


platform_logo_dict = {
    "Amazon" : "A",
    "Shopify" : "S"
}


from user.forms import Loginform
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')
    else:
        form = Loginform(request.POST)
        return render(request,'home.html',{"form":form})


@login_required
def dashboard(request):
    dashboard_context = {"amazon_report_types":None,
                         "added_stores" : None,
                        }
    try:
        dashboard_context['amazon_report_types'] = selected_report_types
        stores = Store.objects.all()
        # loop through available plaforms
        if stores:
            dashboard_context["added_stores"] = {}
            for store in stores:
                dashboard_context["added_stores"][f"{store.store_name}"] = platform_logo_dict[store.platform] 

            print(dashboard_context["added_stores"])
                
            dashboard_context["added_stores"] = stores

        return render(request,'dashboard.html',dashboard_context)
    except Exception as e:
        better_error_handling(e)
    

def store_dash(request,selected_store_name):
    selected_store = Store.objects.filter(store_name = selected_store_name)
    
    selected_platform = None
    print(selected_store)
    return render(request,'dashboard.html')


from dashboard.forms import Addstoreform
from dashboard.d_models import Store 




def add_store(request):
    try:
        if request.method == "POST":
            form = Addstoreform(request.POST)
            if form.is_valid():
                store_name = form.cleaned_data["store_name"]
                platform = form.cleaned_data["platform"]
                
                available_stores = stores()
                if len(available_stores) == 0:
                    color_text("No stores added","red")
                else:
                    color_text(f"Available stores{available_stores}")

                
                if not store_name in available_stores:
                    new_store_data = Store.objects.create(
                        store_name=store_name,
                        platform=platform)
                    new_store_data.save()

                    return redirect("dashboard:home")
                else:
                    color_text(f"Store name : {store_name} already exists","red")
            else:
                color_text("Invalid form","red")
        else:
            form = Addstoreform
    except Exception as e:
        better_error_handling(e)
    return render(request,"add_store_form.html",{"store_form":form})



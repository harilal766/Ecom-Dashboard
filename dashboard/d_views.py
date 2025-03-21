from django.shortcuts import render,redirect
from amazon.response_manipulator import *
from amazon.sp_api_utilities import *
from amazon.sp_api_models import SPAPIBase,Orders,Reports
from helpers.sql_scripts import *
from django.http import FileResponse,HttpResponse
from django.contrib.auth.decorators import login_required
from amazon.report_types import selected_report_types
from user.forms import Loginform
from .forms import Addstoreform
from .d_models import *
from amazon.a_models import SPAPI_Credential
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated



from dashboard.serializers import StoreDebriefSerializer
# Create your views here.    
# create a common context for amazon which can be saved to a json file later
"""
    Home page will display the shipments summary.
    and it will contain the form whiich will trigger the 
    function for report generation.
"""

# Current logged in user




def home(request):
    if request.user.is_authenticated:
        def_slug = StoreProfile.objects.filter(user = request.user)[0].slug
        return view_store(request,def_slug)
        #return dashboard(request)
    else:
        form = Loginform(request.POST)
        return render(request,'home.html',{"form":form})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_store(request,slug):
    stores = StoreProfile.objects.filter(user = request.user)
    dashboard_context = {
        "amazon_report_types": 0,
        "added_stores" : stores,
        "unshipped" : 0,
        "report_types" : None,
        "selected_slug" : slug
    }
    try:
        selected_store = StoreProfile.objects.get(slug = slug)
        selected_store_debrief = StoreDebrief.objects.get_or_create(store = selected_store)
        color_text(selected_store_debrief)

        unshipped_orders = 0; 
        if selected_store.platform == "Amazon":
            sp = SPAPI_Credential.objects.get(user = request.user,store = selected_store)
            
            ord_ins = Orders(access_token=sp.handle_access_token())

            order_count = ord_ins.getOrders(
                CreatedAfter=from_timestamp(7),OrderStatuses = "Unshipped"
            )

            if not order_count == None:
                unshipped_orders = len(order_count)

            dashboard_context["report_types"] = selected_report_types
            
        elif selected_store.platform == "Shopify":
            unshipped_orders = 0


        dashboard_context["unshipped"] = unshipped_orders
        
            

        return render(request,"dashboard.html",dashboard_context)

    except Exception as e:
        better_error_handling(e)

@login_required
def add_store(request):
    try:
        if request.method == "POST":
            form = Addstoreform(request.POST)
            if form.is_valid():
                # created by forms.py
                store_name = form.cleaned_data["store_name"]
                platform = form.cleaned_data["platform"]
                
                # these fields are created by javascript
                client_id = request.POST.get("client_id")
                client_secret = request.POST.get("client_secret")
                refresh_token = request.POST.get("refresh_token")

                available_stores = []
                for store in StoreProfile.objects.filter(user = request.user):
                    available_stores.append(store.store_name)
                
                
                if len(available_stores) == 0:
                    color_text("No stores added","red")
                else:
                    color_text(f"Available stores{available_stores}")

                # store creation
                if not store_name in available_stores:
                    new_store_data = StoreProfile.objects.create(
                        user = request.user, store_name=store_name,
                        platform=platform)
                    new_store_data.save()

                    # Create store profile
                    if platform == "Amazon":
                        api_creds = SPAPI_Credential.objects.create(
                            user = request.user, store = new_store_data,
                            client_id = client_id, client_secret = client_secret,
                            refresh_token = refresh_token)
                        api_creds.save()
                    else:
                        pass

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

def generate_report(request,slug):
    """
    create the suitable dataframe based on the selection
    """
    try:
        if request.method == "POST":
            report_type = request.POST.get("type")
            selected_store = StoreProfile.objects.get(user=request.user,slug=slug)
            start_date = from_timestamp(5); end_date = from_timestamp(0)

            sp = SPAPI_Credential.objects.get(user=request.user,store=selected_store)

            report_df = None
            if selected_store.platform == "Amazon":
                rep = Reports(access_token=sp.handle_access_token())
                report_df = rep.spapi_report_df_creator(report_type,start_date,end_date)
            else:
                pass

            if report_df:
                color_text(report_df)
                
    except Exception as e:
        better_error_handling(e)
    else:
        pass
    return render(request,"dashboard.html")
from django.shortcuts import render,redirect
from amazon.response_manipulator import *
from amazon.sp_api_utilities import *
from amazon.sp_api_models import SPAPIBase,Orders,Reports
from helpers.sql_scripts import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from amazon.report_types import selected_report_types
from user.forms import Loginform
from dashboard.forms import Addstoreform
from dashboard.d_models import *
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


def stores():
    stores = StoreProfile.objects.all()
    stores_name_list = []
    for store in stores:
        stores_name_list.append(store.store_name)
    return stores_name_list

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')
    else:
        form = Loginform(request.POST)
        return render(request,'home.html',{"form":form})

@login_required
def dashboard(request):
    dashboard_context = {"amazon_report_types":None,
                         "added_stores" : None,}
    try:
        dashboard_context['amazon_report_types'] = selected_report_types
        added_stores = StoreProfile.objects.all()
        # loop through available plaforms
        if added_stores:
            dashboard_context["added_stores"] = {}
            default_store_id = added_stores.values_list("id",flat=True)[0]
            default_store_slug = StoreProfile.objects.get(id=default_store_id).slug
            dashboard_context["added_stores"] = added_stores

        return render(request,'dashboard.html',dashboard_context)
    except Exception as e:
        better_error_handling(e)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_store(request,slug):
    try:
        selected_store = StoreProfile.objects.get(slug = slug)
        selected_store_debrief = StoreDebrief.objects.get(store = selected_store)
        if selected_store_debrief:
            color_text(selected_store_debrief,"blue")
            
        common_fields = {
            "Unshipped Orders" : None,
        }
        unshipped = None; 

        if selected_store.platform == "Amazon":
            spapi_model = SPAPI_Credential.objects.get(user=request.user,store=selected_store)
            ord_ins = Orders(access_token=spapi_model.get_or_refresh_access_token()) 
            rep = ord_ins.getOrders(CreatedAfter=from_timestamp(7),OrderStatuses="Unshipped")

            unshipped = len(rep) if rep else 0

        elif selected_store.platform == "Shopify":
            
            unshipped = 0

        # updating the fetched data to the table
        selected_store_debrief.unshipped_orders = unshipped
        selected_store_debrief.save()
        serializer = StoreDebriefSerializer(selected_store_debrief)
        return Response(serializer.data, status=200)
    except Exception as e:
        better_error_handling(e)
        return Response({"error": str(e)}, status=500)

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
                
                available_stores = stores()
                if len(available_stores) == 0:
                    color_text("No stores added","red")
                else:
                    color_text(f"Available stores{available_stores}")
                    color_text(message=f"{client_id} \n {client_secret} \n {refresh_token}")

                # store creation
                if not store_name in available_stores:
                    new_store_data = StoreProfile.objects.create(
                        user = request.user, store_name=store_name,
                        platform=platform)
                    new_store_data.save()

                    # different api credential creation based on platform 
                    if platform == "Amazon":
                        api_creds = SPAPI_Credential.objects.create(
                            user = request.user, store = new_store_data,
                            client_id = client_id, client_secret = client_secret,
                            refresh_token = refresh_token)
                        api_creds.save()
                        api_creds.access_token = api_creds.generate_access_token()
                        api_creds.save()

                    if api_creds:
                        selected_store_debrief= StoreDebrief.objects.create(store = api_creds)


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

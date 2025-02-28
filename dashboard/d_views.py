from django.shortcuts import render,redirect
from amazon.response_manipulator import *
from amazon.sp_api_utilities import *
from amazon.sp_api_models import SPAPIBase,Orders,Reports
from helpers.sql_scripts import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from amazon.report_types import selected_report_types
from user.forms import Loginform
# Create your views here.    
# create a common context for amazon which can be saved to a json file later
"""
    Home page will display the shipments summary.
    and it will contain the form whiich will trigger the 
    function for report generation.
"""

# Current logged in user


def stores():
    stores = Store.objects.all()
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
        stores = Store.objects.all()
        # loop through available plaforms
        if stores:
            dashboard_context["added_stores"] = {}
            for store in stores:
                dashboard_context["added_stores"] = Store.objects.all()
            print(dashboard_context["added_stores"])
            dashboard_context["added_stores"] = stores

        return render(request,'dashboard.html',dashboard_context)
    except Exception as e:
        better_error_handling(e)

@login_required
def view_store(request,slug):
    try:
        selected_store = Store.objects.get(slug = slug)
        color_text(selected_store,"red")
        common_fields = {
            "store_name" : selected_store.store_name,
            "platform" : selected_store.platform,
        }
        additional_fields = {}

        if selected_store.platform == "Amazon":
            spapi_credential = SPAPI_Credential.objects.get(user=request.user,store=selected_store)
            additional_fields["acess_token"] = spapi_credential.access_token

            #SPAPIBase(access_token=spapi_credential.access_token)
            print(spapi_credential.get_or_refresh_access_token())

            """
            order_inst = Orders()
            orders = order_inst.getOrders(CreatedAfter=from_timestamp(7),
                                                      OrderStatuses="Shipped",
                                    EasyShipShipmentStatuses="PendingPickUp")
            """
        else:
            additional_fields["api_Key"] = 0

        common_fields.update(additional_fields)
        return JsonResponse(common_fields)
    except Store.DoesNotExist:
        return JsonResponse({"Error" : f"Store {slug} Not Found"},status=404)


from dashboard.forms import Addstoreform
from dashboard.d_models import Store 
from amazon.a_models import SPAPI_Credential



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
                    new_store_data = Store.objects.create(
                        user = request.user, store_name=store_name,
                        platform=platform)
                    new_store_data.save()

                    # different api credential creation based on platform 
                    api_credentials = {
                        "Amazon" : SPAPI_Credential.objects.create(
                            user = request.user, store = new_store_data,
                            client_id = client_id, client_secret = client_secret,
                            refresh_token = refresh_token, access_token = get_or_generate_access_token()),
                        "Shopify" : 0
                        }

                    # plafrom api details saving
                    api_creds = api_credentials.get(platform,None)
                    if api_creds:
                        api_creds.save()

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




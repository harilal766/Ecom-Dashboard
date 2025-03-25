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
import pdb

import pandas as pd

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

def order_debrief(platform,order_list):
    debrief = {}

    order_id, order_date, ship_date, date = None,None,None,None

    for order in order_list:
        if platform == "Amazon":
            order_id = order["AmazonOrderId"]; ship_date = order["LatestShipDate"]; order_date = order["PurchaseDate"]
            color_text(f"{order_id} - {order_date} - {ship_date}")

        
        

    return debrief

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_store(request,slug):
    stores = StoreProfile.objects.filter(user = request.user)
    dashboard_context = {
        "amazon_report_types": 0,
        "added_stores" : stores,
        "unshipped" : 0,
        "report_types" : None,
        "selected_slug" : slug,
        "api_limit" : False,
        "debrief" : None
    }
    try:
        selected_store = StoreProfile.objects.get(slug = slug,user = request.user, )

        store_debrief = StoreDebrief.objects.get_or_create(store = selected_store,user = request.user)
        
        store_debrief = store_debrief[0]
        if store_debrief:
            unshipped_ord = None

            if selected_store.platform == "Amazon":
                sp = SPAPI_Credential.objects.get(store = selected_store,user = request.user )
                ord_ins = Orders(sp.handle_access_token())
                
                order_list = ord_ins.getOrders(
                    CreatedAfter=from_timestamp(7),OrderStatuses = "Unshipped"
                )

                dashboard_context["debrief"] = order_debrief(selected_store.platform,order_list)

                


                if order_list and "BuyerInfo" in order_list[0]:
                    unshipped_ord = len(order_list)


                dashboard_context["report_types"] = selected_report_types
            elif selected_store.platform == "Shopify":
                unshipped_ord = 0

            
            if unshipped_ord:
                store_debrief.unshipped_orders = unshipped_ord 
                store_debrief.save()

            dashboard_context["unshipped"] = store_debrief.unshipped_orders
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
            report_df = request.FILES.get("report_df")
            selected_store = StoreProfile.objects.get(user=request.user,slug=slug)
            start_date = from_timestamp(5); end_date = from_timestamp(0)

            sp = SPAPI_Credential.objects.get(user=request.user,store=selected_store)

            if selected_store.platform == "Amazon":
                #rep = Reports(access_token=sp.handle_access_token())
                #report_df = rep.report_df_creator(selected_report_types[report_type],start_date,end_date)
                pass
            else:
                pass
    except Exception as e:
        better_error_handling(e)
        return redirect("home")
    else:
        if report_df:
            color_text(f"Creating {selected_store.platform}")
            
            report_df = pd.read_csv(report_df,delimiter='\t')
            
            # DF column filtering based on columns selected by user
            selected_columns = {
                "Amazon" : {
                    "Shipment Report" : [
                        "amazon order id", "purchase date", "last updated date", "order status", "product name",
                        "item status", "quantity", "item price", "item tax", "shipping price", "shipping tax"
                    ],
                    "Return Report" : []
                    },
                "Shopify" : [
                    
                ]
            }            
            filter_cols = []
            for column in selected_columns[selected_store.platform][report_type]:
                filter_cols.append(column.replace(" ","-"))
            col_df = report_df.filter(filter_cols) 
            
            # Df rows filtering
            hour = datetime.today().hour
            next_ship_date = from_timestamp(0) if hour <=  11 else from_timestamp(-1)
            color_text(next_ship_date)

            sp = SPAPI_Credential.objects.get(user=request.user,store=selected_store)
            ord_ins = Orders(sp.handle_access_token())

            next_shipment = ord_ins.getOrders(
                CreatedAfter=from_timestamp(5),OrderStatuses = "Unshipped",
                LatestShipDate= "2025-03-26T18:29:59Z"
            )
            color_text(next_shipment,"red")




            product_name = None; product_price = None
            respective_fields = {
                "Amazon" : {
                    "prod_name" : "product-name", "prod_price" : "item-price"
                }
            }
            

            product = respective_fields[selected_store.platform]["prod_name"]
            price = respective_fields[selected_store.platform]["prod_price"]

        
            color_text(f"Filtered : {col_df}")
            
    return render(request,"dashboard.html")
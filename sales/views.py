from django.shortcuts import render
from amazon.response_manipulator import amazon_dashboard
from amazon.response_manipulator import *
from amazon.sp_api_utilities import *
from amazon.sp_api_models import Orders,Reports
from datetime import datetime,timedelta
from helpers.sql_scripts import *
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.    
# create a common context for amazon which can be saved to a json file later

"""
    Home page will display the shipments summary.
    and it will contain the form whiich will trigger the 
    function for report generation.
"""

amazon_context = {
            'shipment_summary' : None, "ship_date": None, 
            "scheduled_orders":None,"scheduled_dates":None,
            "path" : None, "status":None,
            "excel_out":None
        }


def home(request):
    try:
        # initializing context with none, for handling errors 
        context = {
            'shipment_summary' : None,
            "scheduled_orders":None,"scheduled_dates":None
            }
        orders_instance = Orders(); created_after = (datetime.utcnow() - timedelta(days=4)).isoformat()
        ord_resp = orders_instance.getOrders(CreatedAfter=created_after,OrderStatuses="Unshipped")

        # Finding shipping dates of scheduled and waiting pickup orders
        scheduled_orders = orders_instance.getOrders(CreatedAfter=from_timestamp(7),OrderStatuses="Shipped",
                                EasyShipShipmentStatuses="PendingPickUp",LatestShipDate=from_timestamp(0))
        
        if not scheduled_orders == None:
            context["scheduled_orders"] = True
            scheduled_dates = []

            for order in scheduled_orders:
                ship_date = order["LatestShipDate"]
                if ship_date not in scheduled_dates:
                    scheduled_dates.append(ship_date)
            
            if not scheduled_dates == None:
                context["scheduled_dates"] = scheduled_dates
            

        
        if ord_resp != None:
            summary_dict = amazon_dashboard(response=ord_resp)
            context["shipment_summary"] = summary_dict
            color_text(message=summary_dict.keys(),color="blue")
            color_text(context)
        else:
            color_text(message="Empty response from getOrders",color="red")
        
        
        return render(request,'home.html',context)
    except Exception as e:
        better_error_handling(e)


def df_filter(df,column_or_columns):
    pass


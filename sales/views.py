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

@login_required
def dashboard(request):
    amazon_context = {"amazon_report_types":None}
    try:
        amazon_context['amazon_report_types'] = selected_report_types
        return render(request,'dashboard.html',amazon_context)
    except Exception as e:
        better_error_handling(e)
    

from user.forms import Loginform
def home(request):
    if request.user.is_authenticated:
        return redirect('sales:dashboard')
    else:
        form = Loginform(request.POST)
        return render(request,'home.html',{"form":form})




def df_filter(df,column_or_columns):
    pass


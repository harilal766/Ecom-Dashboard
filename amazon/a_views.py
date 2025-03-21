from django.shortcuts import render,redirect
from amazon.response_manipulator import amazon_dashboard
from amazon.response_manipulator import *
from amazon.sp_api_utilities import *
from amazon.sp_api_models import Orders,Reports

from amazon.report_types import selected_report_types

from django.contrib.auth.models import User

from amazon.a_models import SPAPI_Credential
# Create your views here.





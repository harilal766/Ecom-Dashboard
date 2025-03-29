from django.shortcuts import render,redirect
from amazon.response_manipulator import amazon_dashboard
from amazon.response_manipulator import *
from amazon.sp_api_utilities import *
from amazon.sp_api_models import Amzn_Orders,Amzn_Reports

from amazon.report_types import spapi_report_types

from django.contrib.auth.models import User

from amazon.a_models import SPAPI_Credential
# Create your views here.





from django.shortcuts import render
from amazon.response_manipulator import amazon_dashboard
from amazon.response_manipulator import *
from amazon.sp_api_utilities import *
from amazon.sp_api_models import Orders,Reports

from amazon.report_types import selected_types
# Create your views here.



def add_amazon_store(request):
    return render(request,'amazon_store_form.html')


def report_generator():
    pass


def amazon_detail_page(request):

    context = {"types" : selected_types.keys()}

    """
    Select Report type
    select starting and ending date

    return the orders data based on this.
    the default value of endind date should be today
    """
    type = 0

    if request.method == "POST":
        from_date = request.POST["start_date"]
        to_date = request.POST["end_date"]

        print(from_date,to_date)





    return render(request,"amazon_detail_page.html",context)


def amazon_report_generator():
    pass


"""
show shipment report paramaters only if it is selected.
    amazon order summary
        order shipping dates
        store the summary on a database and call the api if only the data is updated in the api.
"""
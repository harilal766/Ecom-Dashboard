from django.shortcuts import render
from amazon.response_manipulator import amazon_dashboard
from amazon.response_manipulator import *
from amazon.sp_api_utilities import *
from amazon.sp_api_models import Orders,Reports

from amazon.report_types import selected_types
# Create your views here.



def add_amazon_store(request):
    return render(request,'amazon_store_form.html')


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

from sales.views import amazon_context
print(amazon_context)
color_text(message="====",color="red")


def amazon_shipment_report(request):
    if request.method == 'POST':
        selected_ship_date = request.POST.get("date_choice")
        color_text(selected_ship_date,color="red")
        amazon_context["status"] = selected_ship_date

        print(amazon_context)

    return render(request,"home.html",amazon_context)



"""
show shipment report paramaters only if it is selected.
    amazon order summary
        order shipping dates
        store the summary on a database and call the api if only the data is updated in the api.
"""


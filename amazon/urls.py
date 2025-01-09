from django.urls import path
from amazon import views


app_name = 'amazon'


urlpatterns = [
    path('amazon',views.amazon_detail_page,name="amazon"),
    path('amazon_reports',views.amazon_shipment_report,name='amazon_reports'),
    path('add_amazon_store',views.add_amazon_store,name="add_store"),
]
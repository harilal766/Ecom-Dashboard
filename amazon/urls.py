from django.urls import path
from amazon import views


app_name = 'amazon'


urlpatterns = [
    path('add_amazon_store',views.add_amazon_store,name="add_amzn_store"),
]
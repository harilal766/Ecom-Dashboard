from django.urls import path
from amazon import views


app_name = 'amazon'


urlpatterns = [
    path('amazon',views.amazon_detail_page,name="amazon"),
]
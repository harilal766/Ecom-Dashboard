from django.urls import path
from amazon import a_views


app_name = 'amazon'


urlpatterns = [
    path('amazon',a_views.amazon_detail_page,name="amazon"),
    path('amazon_reports',a_views.amazon_report_generator,name='amazon_reports'),
    path('amazon_report_dynamic',a_views.amazon_report_generator_dynamic,name="amazon_report_dynamic"),
]
from amazon.authorization import *
from amazon.sp_api_models import *
from amazon.response_manipulator import *
from helpers.sql_scripts import *
from dashboard.d_views import *



ord_instance = Orders()

ord = ord_instance.getOrders(CreatedAfter=iso_8601_timestamp(4),OrderStatuses="Unshipped")

print(ord)
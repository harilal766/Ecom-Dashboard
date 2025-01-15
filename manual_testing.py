from helpers.sql_scripts import sql_table_CR
from helpers.messages import *
from amazon.response_manipulator import *
from amazon.sp_api_utilities import *


# time is must, if days == 0 , treat time as of todays
# for normal timestamp, there shouldnt be much parameters
# if date is needed only and not time type is not needed.
def timestamp(days,type=None,split=None):
    # types : iso 8601, 
    ind_timestamp = (datetime.now(timezone("Asia/Kolkata"))-timedelta(days=days))
    if type == "iso":
        return ind_timestamp.isoformat()
    elif type == "utc":
        return ind_timestamp.utcnow()
    # if the split is none, return the full time stamp




import pandas as pd
from helpers.excel_ops import *
"""
    Index(['amazon_order_id', 'purchase_date', 'last_updated_date', 'order_status',
        'product_name', 'item_status', 'quantity', 'item_price', 'item_tax',
        'shipping_price', 'shipping_tax'], dtype='object')

"""





def pivot_table(df,columns):
    """
    columns = ["quantity","item_price",'item_tax','shipping_price', 'shipping_tax']
    shipment_report_pivot_table(df=excel,grouping_column="product_name",pivot_columns=columns)
    """
    excel = pd.read_excel(r"D:/5.Amazon/Mathew global/Scheduled report/Scheduled for 2024-12-20 - COD.xlsx",
                      sheet_name="Sheet1")

    pivot = pd.read_excel(r"D:/Ecom-Dashboard/Test documents/pivot/pivot.xlsx",sheet_name="Sheet1")

    out = r"D:/Ecom-Dashboard/Test documents/combined.xlsx"

    excel_appending(dataframes=[excel,pivot],out_path=out)










"""
    Replacing .env with database for the storing of credentials.
    1. Add an option on the front end to add a new store/ ecommmerce platform account.
    2. redirect the user to the amazon/shopify/platform dedicated page.
    3. collect required credentials :
        api keys , tokens, store name, store credential object id in database.
    4. 
"""




def similarity_count():
    pass






orders_instance = Orders()

scheduled_orders = orders_instance.getOrders(CreatedAfter=from_timestamp(7),OrderStatuses="Shipped",
                                EasyShipShipmentStatuses="PickedUp",LatestShipDate=from_timestamp(0))


for i in range(len(scheduled_orders)):
    print(f"{i}. {scheduled_orders[i]}")

#"PendingPickUp"

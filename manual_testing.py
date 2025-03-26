from helpers.sql_scripts import sql_table_CR
from helpers.messages import *
from amazon.response_manipulator import *
from amazon.sp_api_utilities import *




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
    excel = pd.read_excel(
        r"D:/5.Amazon/Mathew global/Scheduled report/Scheduled for 2024-12-20 - COD.xlsx", sheet_name="Sheet1"
    )
    pivot = pd.read_excel(r"D:/Ecom-Dashboard/Test documents/pivot/pivot.xlsx",sheet_name="Sheet1")
    out = r"D:/Ecom-Dashboard/Test documents/combined.xlsx"
    excel_appending(dataframes=[excel,pivot],out_path=out)




















from helpers.label_sorter import *

amazon = dir_switch(win=win_amazon_invoice,lin=lin_amazon_invoice)
post = r"D:\3.Shopify\Sholly ayurveda\labels" ;lin_post = r"/home/hari/Downloads/"
shipping_label_sort(input_pdf_name="26.3.25 cod 25.pdf", input_pdf_path = amazon ,label_type='amazon')
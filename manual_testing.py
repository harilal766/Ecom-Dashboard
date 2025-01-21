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




#"PendingPickUp"



# FBA Lable sorting
"""
    loop through the pdf and split the qrcode page and invoice page of each order into individual units..

    search for the product name and quantity on the invoice page, make sure its an invoice page
    if the order is not mixed and if the order is single item,  add into the dedicated list, 
    this dedicated list should be made prior according to the listed products, also for the mixed items.

"""
def FBA_lable_sort():
    try:
        pdf_file_path = dir_switch(win=win_amazon_invoice,lin=lin_amazon_invoice)

        filename = "21.1.25 cod.pdf"

        pdf_file = os.path.join(pdf_file_path,filename)

        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                # look out for pages without invoice and shipping label
                table = page.extract_table()
                if type(table) == list:
                    """
                    the table inside the invoice page is returned as a linked list
                        1. titles, 2. product name and other values, last two lists are the total and amount in words.
                    """
                    if len(table) > 5: # mixed items order
                        color_text("multi item order","red")
                    else: 
                        heading = table[0]; 
                        product_details = table[1]; 
                        product_name = [product_details][1]
                        amount_in_words = table[-2]; signature = table[-1]
                        print(product_details)
                        color_text("-"*50)

    except Exception as e:
        better_error_handling(e)

FBA_lable_sort()
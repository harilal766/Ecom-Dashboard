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

from PyPDF2 import PdfReader, PdfWriter


def FBA_lable_sort():
    try:
        input_pdf_path = dir_switch(win=win_amazon_invoice,lin=lin_amazon_invoice)

        # todays date folder needs to be created

        input_pdf_name = "22.1.25 prepaid-2.pdf"

        pdf_file = os.path.join(input_pdf_path,input_pdf_name)

        with pdfplumber.open(pdf_file) as pdf:
            page_count = 0
            label_summary_dict = {}
            for page in pdf.pages:
                page_count += 1
                # look out for pages without invoice and shipping label
                table = page.extract_table()
                if type(table) == list:
                    """
                    the table inside the invoice page is returned as a linked list
                        1. titles, 2. product name and other values, last two lists are the total and amount in words.
                    """

                    

                    invoice_page_num = page_count; shipping_label_page_number = invoice_page_num -1
                    heading = table[0]; 
                    product_details = table[1]; 
                    product_name = (product_details[1].split("|")[0]).replace("\n"," ")
                    amount_in_words = table[-2]; signature = table[-1]

                    if len(table) > 5: # mixed items order
                        color_text(f"{page_count} - multi item order","red")
                        label_summary_dict["Mixed"] = []
                        label_summary_dict["Mixed"] +=  [shipping_label_page_number,invoice_page_num]
                    else: 
                        
                        if product_name not in label_summary_dict:
                            label_summary_dict[product_name] = []

                        label_summary_dict[product_name] += [shipping_label_page_number,invoice_page_num]

                        print( f"{shipping_label_page_number} -> {page_count} : {product_name}")
                        color_text("-"*50)
                        

            # merge all the pdf files based on product name
            for index in range(len(label_summary_dict)):

                product_name = list(label_summary_dict.keys())[index]
                page_nums = list(label_summary_dict.values())[index]

                if len(page_nums) > 0:
                    reader = PdfReader(pdf_file); writer = PdfWriter()

                    for num in page_nums:
                        writer.add_page(reader.pages[num-1])


                    # Create a new folder for storing filtered pdf files
                    new_folder_path = os.path.join(input_pdf_path,input_pdf_name.replace(".pdf"," folder")) # new directory path
                    os.makedirs(new_folder_path,exist_ok=True) # creating new directory
                    out_pdf_path = os.path.join(new_folder_path,product_name) # adding out pdf file to the path

                    # writing the pages to the file.
                    with open(f"{out_pdf_path} - {int(len(page_nums)/2)}","wb") as filtered_pdf:
                        writer.write(filtered_pdf)
                

            print(label_summary_dict)

    except Exception as e:
        better_error_handling(e)

FBA_lable_sort()


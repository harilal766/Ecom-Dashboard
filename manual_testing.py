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
import re
from helpers.regex_patterns import *



def FBA_label_sort(input_pdf_name, input_pdf_path,label_type):
    """
    Deal breakers 
        Common : page should not be empty
        Amazon : odd page
    """
    try:
        # Create a new folder for storing filtered pdf files
        todays_date_folder = f"{from_timestamp(0).split("T")[0]} label split" 
        #todays_date_folder = "25.1.25 lable split"
        todays_folder_path = os.path.join(input_pdf_path, todays_date_folder)
        input_pdf_path = os.path.join(input_pdf_path,input_pdf_name)
        """
            open the pdf only if the path exists
            check if the label is amazon or post
        """
        if not os.path.exists(input_pdf_path):
            color_text("The file does not exist..","red")
        else:
            if not label_type:
                color_text("specify the label type, Eg : Amazon, Post etc...","red")
            else:
                with pdfplumber.open(input_pdf_path) as pdf:
                    # make sure the page is not empty
                    #Varible Initialization
                    page_number = 0; product_name = None; product_qty = None
                    label_summary_dict = {}; post_product_line = r"Ref"

                    for page in pdf.pages:
                        page_number += 1

                        page_text = page.extract_text(); page_table = page.extract_table()

                        if page_text == "": # adding the deal breaker conditions first 
                            color_text(f"{page_number} : Empty.","red")
                        else:
                            if label_type == "amazon":
                                if len(page_table) <=2:
                                    color_text("Odd page detected","red")
                                else:
                                    #color_text(page_table)

                                    if len(page_table) > 5: # mixed items order
                                        color_text(f"{page_number} - multi item order","red")
                                        product_name = "Mixed"
                                    else: # single item order
                                        product_row = page_table[1]
                                        product_name = product_row[1].split("\n")[0].split("|")[0]
                                        product_qty = product_row[3]

                                        #color_text(product_row[1])
                                        color_text(f"{page_number} - {product_name} - {product_qty} qty.")
                            
                            elif label_type == "post":
                                order_line = re.findall(post_product_line_pattern,page_text)

                                
                            else:
                                color_text("unsupported label","red")
                            
                            # label summary making
                            if product_name and product_qty:
                                 # first dict based on name
                                if not product_name == "Mixed":
                                    if product_name not in label_summary_dict:
                                        label_summary_dict[product_name] = {}
                                    if product_qty not in label_summary_dict[product_name]:
                                        label_summary_dict[product_name][product_qty] = [] # nested dict based on qty
                                    label_summary_dict[product_name][product_qty] += [page_number-1,page_number]
                                # mixed orders shouldnt have a nested dict inside.
                                else: 
                                    if product_name not in label_summary_dict:
                                        label_summary_dict[product_name] = []
                                    label_summary_dict[product_name] += [page_number-1,page_number]


                    # create a folder based on 
                    # loop through the summary dictionary
                    for product_name,values in label_summary_dict.items():
                        out_pdf_path = os.path.join(todays_folder_path,input_pdf_name.replace(".pdf",""))
                        # make the directory
                        os.makedirs(out_pdf_path,exist_ok=True)
                        # make add the pdf file to the path

                        order_count = 0; page_numbers = []


                        # find page numbers from single item and mixed orders
                        
                        if type(values) == dict:
                            for quantity,page_nums in values.items():
                                page_numbers = page_nums; order_count = int(len(page_nums)/2)
                                pdf_merger(page_numbers,
                                input_pdf_path,
                                os.path.join(out_pdf_path,f"{product_name} qty {quantity} - {order_count} No.s"))
                                
                        elif type(values) == list:
                            page_numbers = values; order_count = int(len(values)/2)
                            pdf_merger(page_numbers,
                            input_pdf_path,
                            os.path.join(out_pdf_path,f"{product_name} qty {quantity} - {order_count} No.s"))
                        
                            
                    print(label_summary_dict)
            
    except Exception as e:
        better_error_handling(e)



def pdf_merger(pages,input_pdf,output_pdf):
    try:
        
        #print(pages)
    
        if len(pages) > 0:
            reader = PdfReader(input_pdf); writer = PdfWriter()
            for page_num in pages:
                writer.add_page(reader.pages[page_num-1])

            
            if not output_pdf == None:
                with open(output_pdf,"wb") as output_pdf_file:
                    writer.write(output_pdf_file)
                
                if output_pdf_file:
                    color_text(f"Created {output_pdf_file} with the pages : {pages}")
            else:
                color_text("The out pdf directory  does not exist","red")
            
            
    except Exception as e:
        better_error_handling(e)

        



# both of these should be from front end in django
amazon = dir_switch(win=win_amazon_invoice,lin=lin_amazon_invoice)


post = r"D:\6.SPEED POST"

lin_post = r"/home/hari/Downloads/"

FBA_label_sort(input_pdf_name="28.1.25 prepaid - 2.pdf", 
    input_pdf_path = amazon ,label_type='amazon')
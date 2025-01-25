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
from helpers.regex_patterns import post_track_id_pattern,post_order_id_pattern

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

        input_pdf_file = os.path.join(input_pdf_path,input_pdf_name)
        """
            open the pdf only if the path exists
            check if the label is amazon or post
        """
        if os.path.exists(input_pdf_path):
            with pdfplumber.open(input_pdf_file) as pdf:
                # make sure the page is not empty
                

                """   
                page_count = 0
                label_summary_dict = {}

                title = None 

                for page in pdf.pages:
                    page_count += 1
                    # look out for pages without invoice and shipping label
                    
                    page_text = page.extract_text()

                    invoice_pattern = "Invoice Number : IN-6834"
                    # invoice length : between 4 to 10 

                    page_table = page.extract_table()


                    if label_type == "amazon":
                        if type(page_table) == list:
                            if len(page_table) > 2: # if this condition succeeds, its not an odd page..
                                # first row
                                invoice_page_num = page_count; label_page_number = invoice_page_num -1
                                heading = page_table[0]; 
                                # second row
                                product_details = page_table[1]; 
                                product_name = (product_details[1].split("|")[0]).replace("\n"," ")
                                product_qty = product_details[3]

                                if len(page_table) > 5: # mixed items order
                                    color_text(f"{page_count} - multi item order","red")
                                    title = "Mixed"
                                else: # single item order
                                    title = product_name
                                    
                            else: # odd page found.
                                color_text(f"{label_page_number} odd page detected.","red")

                    # Post label
                    elif label_type == 'post':
                        post_order_id = re.findall(post_order_id_pattern,page_text)
                        if post_order_id:
                            post_order_id = post_order_id[0]

                        product_details_pattern = r'Ref'

                    if not title == None :
                        color_text(title)
                        if title not in label_summary_dict:
                            label_summary_dict[title] = []
                            label_summary_dict[title] +=  [label_page_number,invoice_page_num]
                            print( f"{label_page_number} -> {page_count} : {product_name}, {product_qty} No.s")
                            color_text("-"*50)

                        
                if label_summary_dict:
                    # merge all the pdf files based on product name
                    for index in range(len(label_summary_dict)):

                        product_name = list(label_summary_dict.keys())[index]
                        page_nums = list(label_summary_dict.values())[index]

                        # def pdf_merger(out_filename,page_num_list):

                        if len(page_nums) > 0:
                            reader = PdfReader(input_pdf_file); writer = PdfWriter()

                            new_folder_path = os.path.join(todays_folder_path,input_pdf_name.replace(".pdf","")) # new directory path by replacing the .pdf in the filename
                            os.makedirs(new_folder_path,exist_ok=True) # creating new directory
                            out_pdf_path = os.path.join(new_folder_path,product_name) # adding out pdf file to the path

                            for num in page_nums:
                                writer.add_page(reader.pages[num-1])


                            # writing the pages to the file.
                            with open(f"{out_pdf_path} - {int(len(page_nums)/2)}","wb") as filtered_pdf:
                                writer.write(filtered_pdf)
                else:
                    color_text("Label summary is empty.","red")
                """

        else:
            color_text("The file does not exist..","red")

            

    except Exception as e:
        better_error_handling(e)



# both of these should be from front end in django
amazon = dir_switch(win=win_amazon_invoice,lin=lin_amazon_invoice)


post = r"D:\6.SPEED POST"

FBA_label_sort(input_pdf_name="25.1.25 prepaid - 1.pdf", 
    input_pdf_path = amazon, 
    label_type = 'amazon')


























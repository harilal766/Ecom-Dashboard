
from PyPDF2 import PdfReader, PdfWriter
import re
from helpers.regex_patterns import *
from helpers.messages import *
import pandas as pd
from helpers.excel_ops import *
from helpers.sql_scripts import sql_table_CR
from helpers.messages import *
from amazon.response_manipulator import *
from amazon.sp_api_utilities import *

# FBA Lable sorting
"""
    loop through the pdf and split the qrcode page and invoice page of each order into individual units..

    search for the product name and quantity on the invoice page, make sure its an invoice page
    if the order is not mixed and if the order is single item,  add into the dedicated list, 
    this dedicated list should be made prior according to the listed products, also for the mixed items.

"""



def shipping_label_sort(input_pdf_name, input_pdf_path,label_type):
    """
    Deal breakers 
        Common : page should not be empty
        Amazon : odd page
    """
    try:
        # Create a new folder for storing filtered pdf files
        todays_date_folder = f"{timestamp(0).split("T")[0]} label split" 
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

                    order_pages = None

                    for page in pdf.pages:
                        page_number += 1

                        page_text = page.extract_text(); page_table = page.extract_table()

                        if page_text == "": # adding the deal breaker conditions first 
                            color_text(f"{page_number} : Empty.","red")
                        else:
                            if label_type == "amazon":
                                order_pages = [page_number-1,page_number]
                                if type(page_table) == list:
                                    if len(page_table) <= 2:
                                        color_text("Odd page detected","red")
                                    else:
                                        #color_text(page_table)
                                        if len(page_table) > 5: # mixed items order
                                            color_text(f"{page_number} - multi item order","red")
                                            product_name = "Mixed"
                                        else: # single item order
                                            product_row = page_table[1]
                                            product_name = product_row[1].split("|")[0].replace("\n","")
                                            product_qty = product_row[3]

                                else:
                                    color_text("the table is not a list","red")
                            
                            elif label_type == "post":
                                order_pages = [page_number]

                                order_id = re.findall(post_order_id_pattern,page_text)

                                # to make sure only one order is in one page
                                if len(order_id) == 1:
                                    
                                    # Updated pattern to capture full product name with variant and quantity separately
                                    pattern = r'([\w\s\(\)&%-]+-\s*\d+\s*(?:GM|ML))\s*-\s*(\d+)'
                                    matches = re.findall(pattern, page_text)

                                    # Convert matches to structured data
                                    products = [{'product_with_variant': match[0].strip().replace("\n"," "), 'quantity': int(match[1])} for match in matches]

                                    if len(products) == 1:
                                        product = products[0]
                                        product_name = product["product_with_variant"]; product_qty = product["quantity"]
                                    else:
                                        color_text("Mixed order","red")
                                        product_name = "Mixed"
                                else:
                                    color_text(order_id,"red")
                                    color_text("More than one order id detected at one page","red")
                                    break
                            else:
                                color_text("unsupported label","red")
                            
                            color_text(f"{order_pages} - {product_name} - {product_qty} qty.")
                            
                            # label summary making , needed parameteres : product_name and qty, an empty dict
                            if product_name and product_qty:
                                 # first dict based on name
                                if not product_name == "Mixed":
                                    if product_name not in label_summary_dict:
                                        label_summary_dict[product_name] = {}
                                    if product_qty not in label_summary_dict[product_name]:
                                        label_summary_dict[product_name][product_qty] = [] # nested dict based on qty
                                    label_summary_dict[product_name][product_qty] += order_pages
                                # mixed orders shouldnt have a nested dict inside.
                                else: 
                                    if product_name not in label_summary_dict:
                                        label_summary_dict[product_name] = []
                                    label_summary_dict[product_name] += order_pages
                            

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
                                page_numbers = page_nums; 

                                if label_type == 'amazon':
                                    order_count = int(len(page_nums)/2)
                                else:
                                    order_count = len(page_nums)
                                pieces = order_count*quantity
                                pdf_merger(page_numbers,
                                input_pdf_path,
                                
                                os.path.join(out_pdf_path,f"{product_name} - {order_count} orders - {quantity} qty"))
                                
                        elif type(values) == list:
                            page_numbers = values; order_count = int(len(values)/2)
                            pdf_merger(page_numbers,
                            input_pdf_path,
                            os.path.join(out_pdf_path,f"{product_name} - {order_count} orders"))
                        
                            
                    print(label_summary_dict)
            
    except Exception as e:
        better_error_handling(e)


def label_summary(product_name, product_qty,order_pages,label_summary_dict):
    if product_name and product_qty:
        # first dict based on name
        if not product_name == "Mixed":
            if product_name not in label_summary_dict:
                label_summary_dict[product_name] = {}
            if product_qty not in label_summary_dict[product_name]:
                label_summary_dict[product_name][product_qty] = [] # nested dict based on qty
                label_summary_dict[product_name][product_qty] += order_pages
        # mixed orders shouldn't have a nested dict inside.
        else: 
            if product_name not in label_summary_dict:
                label_summary_dict[product_name] = []
                label_summary_dict[product_name] += order_pages
        print(label_summary_dict)


import platform
def pdf_merger(pages,input_pdf,output_pdf):
    try:
        
        #print(pages)
    
        if len(pages) > 0:
            reader = PdfReader(input_pdf); writer = PdfWriter()
            for page_num in pages:
                writer.add_page(reader.pages[page_num-1])

            
            if not output_pdf == None:
                operating_sys = (platform.system()).lower()
                if operating_sys == "windows":
                    output_pdf += ".pdf"
                with open(output_pdf,"wb") as output_pdf_file:
                    writer.write(output_pdf_file)
                    
                
                if output_pdf_file:
                    color_text(f"Created {output_pdf_file} with the pages : {pages}")
            else:
                color_text("The out pdf directory  does not exist","red")
            
            
    except Exception as e:
        better_error_handling(e)
from django.shortcuts import render
from amazon.response_manipulator import amazon_dashboard
from amazon.response_manipulator import *
from amazon.sp_api_utilities import *
from amazon.sp_api_models import Orders,Reports

from amazon.report_types import selected_report_types
# Create your views here.





def add_amazon_store(request):
    return render(request,'amazon_store_form.html')


def amazon_detail_page(request):

    context = {"types" : selected_report_types.keys()}

    """
    Select Report type
    select starting and ending date

    return the orders data based on this.
    the default value of endind date should be today
    """
    type = 0

    if request.method == "POST":
        from_date = request.POST["start_date"]
        to_date = request.POST["end_date"]

        print(from_date,to_date)
    return render(request,"amazon_detail_page.html",context)

from sales.views import amazon_context
print(amazon_context)

"""
Display types of reports on the amazon dashbaord.
add the parameters based on the selected type.
generate the report based on the selected type and its parameters.

the current working model should be merged to main, there are for bugs in the new upcoming model.
"""



def amazon_report_generator(request):
    """"
    Step 1 - Order API access
        1. Access the order api and access the shipped (scheduled) and pending pickup orders.
        2. append the cod and prepaid order ids in to seperate lists.

    Step 2 - Report API Access
        1. Request the report api based on the scheduled orders type,starting from 5 days ago to today.
        2. filter the received df based on required fields.
        3. with the help of a for loop,
            filter the df again based on the previous cod and prepaid lists and convert it to an excel sheet 
            the sheet names need to be dynamic in future.
    """
    # go to api docs and find other order statueses like waiting for pickup
    order_instance = Orders()
    todays_timestamp = iso_8601_timestamp(0); todays_ind_date = iso_8601_timestamp(0)
    try:
        # since amazon's time limit for daily orders is 11 am , make \\
        # context initialization for Django...
        amazon_context = {"path" : None}
        #next_ship = amzn_next_ship_date()

        if request.method == 'POST':
            selected_ship_date = request.POST.get("date_choice")

            report_type = request.POST.get("report_choice")

            color_text(selected_ship_date,color="red")
        
            # change it to the output got from front end
            #selected_ship_date = todays_ind_date
            

            """
            last ship date needed to be stored in the database to avoid logical errors 
            if the scheduling report taking is being done after 11 am. 
            """
            
            orders_details = order_instance.getOrders(CreatedAfter=from_timestamp(7),
                                                      OrderStatuses="Shipped",
                                    EasyShipShipmentStatuses="PendingPickUp",
                                    LatestShipDate=selected_ship_date)
            space = " "*14
            if not orders_details == None:
                color_text(message=f"Orders  Count : {len(orders_details)}")
                # Primary Initializations
                cod_orders = []; prepaid_orders = []; order_count = 0; 
                excel_files = []

                if isinstance(orders_details,list) and len(orders_details) != 0:
                    color_text(message=f"Orders scheduled for {todays_ind_date}")
                    for i in orders_details:
                        if isinstance(i,dict):
                            # order fields
                            order_id = i["AmazonOrderId"]; 
                            purchase_date = i["PurchaseDate"]; ship_date = i["LatestShipDate"]
                            payment_method = i["PaymentMethod"]; status = i["EasyShipShipmentStatus"]
                            # verify again to get orders for today only

                            if ship_date.split("T")[0] == selected_ship_date.split("T")[0]:
                                order_count += 1
                                if payment_method == "COD":
                                    cod_orders.append(order_id)
                                else:
                                    prepaid_orders.append(order_id)
                                order_info = f"{order_count}.{order_id} : Status - {status}, puchased on - {purchase_date}, shipping on - {ship_date}, type - {payment_method} date : {selected_ship_date}"
                                print(order_info)
                        else:
                            color_text(message=f"Not a dictionary but of type : {type(i)} ",color="red")
                    # Generate reports only if there are cod or prepaid orders
                    if len(cod_orders) >0 or len(prepaid_orders)>0:
                        shipment_report_df = sp_api_report_df(report_type="GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL",
                                                                start_date=from_timestamp(5),end_date=todays_timestamp)
                        # Filtering based on required columns.
                        fields = ["amazon_order_id","purchase_date","last_updated_date","order_status","product_name","item_status",
                            "quantity","item_price","item_tax","shipping_price","shipping_tax"]
                        column_filtered_df = (shipment_report_df.filter(fields))
                        # find the product names and add it on a list, for adding to an excel sheet
                        

                        # "Pending - Waiting for Pickup"
                        # if the output is available, convert it to excel
                        color_text(message=f"COD {len(cod_orders)} No.s : {cod_orders}\n{"+++++"}\nPrepaid {len(prepaid_orders)} No.s : {prepaid_orders} \nDataframe : \n {column_filtered_df}")
                        color_text(message=column_filtered_df)
                        
                        if not column_filtered_df.empty :
                            # after that, make a loop to convert to convert cod and prepaid orders to excel sheet
                            types = {"COD" : cod_orders,"Prepaid": prepaid_orders}
                            for type_key,type_value in types.items():
                                if not len(type_key) == 0 :
                                    payment_type_filtered_orders_df = column_filtered_df[column_filtered_df['amazon_order_id'].isin(type_value)]

                                    



                                    # Creating manual report for tallying
                                    shipment_manual_report(df=payment_type_filtered_orders_df,
                                        df_prod_name_col="product_name", df_item_price_col="item_price",df_qtys_column="quantity",
                                        template_filename="amazon manual report template.xlsx",
                                        template_filepath=dir_switch(win=win_amazon_manual_report,lin=lin_amazon_manual_report),
                                        out_filename=f"Amazon manual report {type_key}.xlsx",
                                        out_filepath=dir_switch(win=win_amazon_manual_report_out,lin=lin_amazon_manual_report_out))

                                    print(payment_type_filtered_orders_df)
                                    # Excel path should be changed to dynamic for django.
                                    excel_dir = dir_switch(win=win_amazon_scheduled_report,lin=lin_amazon_scheduled_report)
                                    excel_name = f"Scheduled for {str(selected_ship_date).split("T")[0]} - {type_key}.xlsx"

                                    # store the excel filenames to a list
                                    excel_files.append(excel_name)

                                    color_text(message=f"Ship date : {selected_ship_date}")
                                    excel_path = os.path.join(excel_dir,excel_name)
                                    # verify the path exists..
                                    if not len(excel_path) == 0:
                                        payment_type_filtered_orders_df.to_excel(excel_writer=excel_path,index="False",
                                                                        sheet_name=f"Sheet 1")
                                        amazon_context["path"] = excel_path
                                    else:
                                        color_text(f"The path {excel_path} does not exist",color="red")
                                else:
                                    color_text(message=f"There are no orders in the type : {type_key}")

                            if excel_path:
                                amazon_context["status"] = f"Files {excel_files} saved to {excel_dir}"
                        else:
                            color_text("There are no scheduled orders",color="red")
                else:
                    color_text(message=f"No pending schedules for {todays_timestamp.split("t")[0]}",color="red")
            else:
                color_text(message="Empty order response",color="red")
        
        return render(request,"home.html",amazon_context)
    except Exception as e:
        better_error_handling(e)




































"""
show shipment report paramaters only if it is selected.
    amazon order summary
        order shipping dates
        store the summary on a database and call the api if only the data is updated in the api.
"""


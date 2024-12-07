from helpers.messages import *
from datetime import datetime,timedelta
from amazon.sp_api_models import *
from amazon.report_types import *
from amazon.response_manipulator import *
import requests
import pandas as pd
from io import StringIO
from helpers.sql_scripts import sql_to_excel
from collections import namedtuple

today = datetime.today()
today_start_time = today.replace(hour=0,minute=0,second=0,microsecond=0).isoformat()+"Z"
today_end_time = today.replace(hour=23,minute=59,second=59,microsecond=99999).isoformat()+"Z"

def amzn_next_ship_date(out=None):
    if datetime.now().time().hour >= 11:
    # if the time is past 11:00 AM and todays scheduling is done, return tomorrows date if not a holiday
        return iso_8601_timestamp(-1)
    else:
        return iso_8601_timestamp(0)


def sp_api_shipment_summary(response):
    try:# only for amazon api, these api contains the field -> AmazonOrderId.
        #out_list = response['payload']['Orders']
        next_shipment_date = ''
        
        cod_orders = []; prepaid_orders = []
        # Counter Initialization
        order_count = 0; cod_count = 0; prepaid_count = 0; field_count = 0
        if response != None:
            for item in response:
                ship_by_date = item["LatestShipDate"].split("T")[0]
                last_update_date_string = str(item["LastUpdateDate"]).split("T")[0]
                #print(f"Ship date : {ship_date_string},  Today : {today_string} :- {ship_date_string == today_string}")
                order_id = item['AmazonOrderId']
                payment_method = item["PaymentMethod"]
                #color_print(message=f"Order : {order_count}{'-'*40}",color='blue')
                if type(item) == dict:
                    if  ship_by_date == iso_8601_timestamp(0).split("T")[0]: 
                        field_count+=1; order_count += 1
                        if item['PaymentMethodDetails'] == ['CashOnDelivery']:
                            cod_orders.append(order_id)
                        elif item['PaymentMethodDetails'] == ['Standard']:
                            prepaid_orders.append(order_id)
                    print(f"{order_count}. {item['AmazonOrderId']}, Ship by date : {ship_by_date}, Payment : {payment_method}")
            # To return the vaules in a tuple..
            orders = namedtuple("Orders",["cod","prepaid","order_count"])
            return orders (cod_orders,prepaid_orders,order_count)
    
        else:
            color_text(message="Empty Response Received",color="red")
            return None

    
    except Exception as e:
        better_error_handling(e)



def iso_8601_timestamp(days):
    try:
        if type(days) == int: 
            # Substract (time now - time n days back) and return the answer in iso format
            return (datetime.utcnow() - timedelta(days=days)).isoformat()
        else:
            color_text(message="Enter a number.",color='red')
    except Exception as e:
        better_error_handling(e)




def rep_doc_id_generator(report_id):
    retries =0 ; max_retries = 100 ; delay = 2
    while retries <  max_retries:
        R = Reports(); last_status = None
        report = R.getReport(reportId=report_id)
        if report != None:
            last_status = ''
            status = report["processingStatus"]
            if status == "DONE":
                color_text(message=status,color='green')
                return report.get('reportDocumentId')
            if status in ["IN_QUEUE", "IN_PROGRESS"]:
                if status != last_status:
                    color_text(message=status,color='blue')
                    last_status = status
            elif status == "CANCELLED":
                color_text(message=status,color='red')
                break
            else:
                color_text(message=f"Unknown Status : {status}",color='red')
        else:
            color_text(message="Report Error",color='red')
            break
        retries += 1
        time.sleep(delay)
    raise Exception("Report processing did not complete within the maximum retries.")


def sp_api_report_df_generator(report_type,start_date,end_date):
    try:
        instance = Reports()
        report_id = instance.createReport(reportType=report_type,
                                          dataStartTime=start_date,dataEndTime=end_date)
        report_id = report_id.get('reportId')
        if report_id:
            color_text(message=f"Report Id Created : {report_id}")
            # Report document id generation.
            rep_doc_id = rep_doc_id_generator(report_id=report_id)
            if rep_doc_id != None:
                color_text(message=f"Report document Id generated : {rep_doc_id}")
                report_document = instance.getReportDocument(reportDocumentId=rep_doc_id)
                document_url = report_document['url']
                document_response = requests.get(document_url)
                print(f"Status code - {document_response.status_code}")
                if document_response.status_code == 200:
                    byte_string = document_response.content
                    decoded_data = byte_string.decode("utf-8") # Decoding the response into utf-8

                   # Returning the dataframe
                    data_io = StringIO(decoded_data) # converting the decode data into a file simulation
                    df = pd.read_csv(data_io,sep = '\t')

                    new_headers = []
                    if not df.empty:
                        # making sure column have underscore word seperator
                        for column in  df.columns.tolist():
                            underscore = column.replace("-","_")
                            new_headers.append(underscore)

                        df.columns = new_headers
                        return df
                            
                    else : 
                        color_text(message="There was an error in generating the dataframe",color='red')
                else:
                    color_text(message="Unable to generate report, status code is not 200",color='red')
            else:
                color_text(message="Report document Id failed,",color='red')
        else:
            color_text(message="Report id failed",color='red')
    except Exception as e:
        better_error_handling(e)

from helpers.sql_scripts import db_connection,sql_table_CR
from amazon.sp_api_models import *
from amazon.response_manipulator import *
import pandas as pd






# FUNCTIONS FOR DJANGO ---------------------------------------------------------

def amazon_dashboard(response):
    try:
        if response != None:
            summary_dict = {}
            summary_dict["total_orders"] = 0
            for order in response:
                if type(order) == dict:
                    # taking orders count
                    summary_dict["total_orders"] += 1 

                    ship_by_date = (order['LatestShipDate']).split("T")[0]
                    payment_method = order['PaymentMethod']

                    if ship_by_date not in summary_dict.keys():
                        summary_dict[ship_by_date] = {}
                    if payment_method not in summary_dict[ship_by_date]:
                        summary_dict[ship_by_date][payment_method] = 0
                    summary_dict[ship_by_date][payment_method] += 1
            return summary_dict
        else:
            color_text(message=f"Response : {response}, please check",color="red")
            return None
    except Exception as e:
        better_error_handling(e)
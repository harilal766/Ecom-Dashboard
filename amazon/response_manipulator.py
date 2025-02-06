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
from amazon.sp_api_utilities import *


def rep_doc_id_generator(report_id):
    retries =0 ; max_retries = 100 ; delay = 2
    report_status_json = {"status":None}
    while retries <  max_retries:
        R = Reports(); last_status = None
        report = R.getReport(reportId=report_id)
        if report != None:
            last_status = ''
            status = report["processingStatus"]
            report_status_json["status"] = status
            color_text(message=f"Status :\n{report_status_json}",end="\r")
            if status == "DONE":
                color_text(message=status,color='green',end="\r")
                return report.get('reportDocumentId')
            if status in ["IN_QUEUE", "IN_PROGRESS"]:
                if status != last_status:
                    color_text(message=status,color='blue',end="\r")
                    last_status = status
            elif status == "CANCELLED":
                color_text(message=status,color='red',end="\r")
                break
            else:
                color_text(message=f"Unknown Status : {status}",color='red',end="\r")
        else:
            color_text(message="Report Error",color='red',end="\r")
            break
        retries += 1
        time.sleep(delay)
    raise Exception("Report processing did not complete within the maximum retries.")


def sp_api_report_df(report_type,start_date,end_date):
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

                    ship_by_date = str(order.get('LatestShipDate',None)).split("T")[0] # 2024-12-28T18:29:59Z
                    payment_method = order.get('PaymentMethod',None)

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
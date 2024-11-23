from helpers.messages import *
from datetime import datetime,timedelta
from amazon.api_models import *
from amazon.report_types import *
from amazon.response_manipulator import *
import requests
import pandas as pd
from io import StringIO



def next_shipment_summary(response):
    try:# only for amazon api, these api contains the field -> AmazonOrderId.
        #out_list = response['payload']['Orders']
        next_shipment_date = ''
        today_string = str(datetime.today()).split(" ")[0]
        cod_orders = []; prepaid_orders = []
        # Counter Initialization
        order_count = 0; cod_count = 0; prepaid_count = 0; field_count = 0
        for item in response:
            #print(item); color_print(message=f"{'-'*80}",color='green')
            ship_date_string = str(item['EarliestShipDate']).split("T")[0]
            #ship_date_string = today_string
            last_update_date_string = str(item["LastUpdateDate"]).split("T")[0]
            #print(f"Ship date : {ship_date_string},  Today : {today_string} :- {ship_date_string == today_string}")
            order_id = item['AmazonOrderId']
            order_count += 1
            #color_print(message=f"Order : {order_count}{'-'*40}",color='blue')
            if type(item) == dict:
                if  today_string == ship_date_string: 
                    field_count+=1
                    if item['PaymentMethodDetails'] == ['CashOnDelivery']:
                        cod_orders.append(order_id)
                    elif item['PaymentMethodDetails'] == ['Standard']:
                        prepaid_orders.append(order_id)
                print(f"{order_count}. {item['AmazonOrderId']}, Ship by date : {ship_date_string}")
                
        boundary = " "   
        id_and_date = f"COD :{cod_orders}\n{boundary}\nPrepaid :{prepaid_orders}\n{boundary}"
        color_text(message=id_and_date,color='blue')
        
    except Exception as e:
        better_error_handling(e)
    color_text(f"Total orders: {order_count}\nCOD for {today_string} : {len(cod_orders)}\nPrepaid for {today_string} : {len(prepaid_orders)}",color='blue')

def report_display(response):
    if len(response) == 0:
        color_text(message=f"Empty Output. : {response}",color='red')
    else:
        for i in response:
            for key,value in i.items():
                    print(f"{key} -:- {value}")
            color_text("------------",color="blue")

def requested_reports(response,report_id = None):
    color = 'blue'
    for report in response:
        if type(report) == dict:
            for key,value in report.items():
                if report['reportId'] == report_id:
                    color_text(message="Target id found.")
                    color = 'green'
                color_text(message = f"{key} - {value}",color=color)
            color_text(message="----------",color='blue')




def n_days_back_timestamp(days):
    try:
        if type(days) == int: 
            # Substract (time now - time n days back) and return the answer in iso format
            return (datetime.utcnow() - timedelta(days=days)).isoformat()
        else:
            color_text(message="Enter a number.",color='red')
    except Exception as e:
        better_error_handling(e)




def rep_doc_id_generator(report_id):
    while True:
        R = Reports()
        report = R.getReport(reportId=report_id)
        status = report["processingStatus"]
        if status == "DONE":
            color_text(message=status,color='green')
            return report['reportDocumentId']
        if status == "IN_QUEUE":
            color_text(message=status,color='blue')
        elif status == "CANCELLED":
            color_text(message=status,color='red')
        else:
            color_text(message=status,color='green')

def sp_api_report_generator(report_type,start_date,end_date,file_dir,filename):
    try:
        instance = Reports()
        report_id = instance.createReport(reportType=report_type,
                                          dataStartTime=start_date,dataEndTime=end_date)
        report_id = report_id['reportId']
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
                    file_content = document_response.content
                    decoded_data = file_content.decode("utf-8") # Decoding the response into utf-8
                    # Writing the data into a csv file
                    filepath = os.path.join(file_dir,filename)
                    data_io = StringIO(decoded_data) # converting the decode data into a file simulation
                    df = pd.read_csv(data_io,sep = '\t')
                    df.to_csv(filepath,index=False)
                else:
                    color_text(message="Unable to generate report.",color='red')
            else:
                color_text(message="Report document Id failed,",color='red')
        else:
            color_text(message="Report id failed",color='red')
    except Exception as e:
        better_error_handling(e)
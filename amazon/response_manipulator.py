from helpers.messages import *
from amazon.sp_api_models import *
from amazon.report_types import *
from amazon.response_manipulator import *
import requests
import pandas as pd
from io import StringIO
from amazon.sp_api_utilities import *




def rep_doc_id_generator(report_id,access_token):
    retries =0 ; max_retries = 100 ; delay = 2
    report_status_json = {"status":None}
    while retries <  max_retries:
        R = Reports(access_token=access_token); last_status = None
        report = R.getReport(reportId=report_id)
        if report:
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
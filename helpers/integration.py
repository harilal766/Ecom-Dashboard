from sp_api.api import Reports
from sp_api.base import Marketplaces,ReportType,ProcessingStatus
import time,requests,csv,json
from messages import better_error_handling

credentials = dict(
    refresh_token = "Atzr|IwEBIPBY5e0kXS-uM-K5RFXeu8lhrFWvjUNENau8MJk1L7XWAli848mP2ctunWJVQrRk-wqYhAer-_5hS1v847tIrAOBeSqHRbPWuuF7Gp-4fmGwEEWezZ3PicU-LuxybRfikuIX4gJG4EWx3jdm9UpQUcTHmS5Pl4avCzsnnpDs0x0OAXG3Ag597I6cGsrUd0k4WqD4fw4MpFLCIntIS_XdNxwvkCNGhmgEMeqNwOXWp8G346UZq4OxAqGB9yOlOhjqQw86yjQr6fNftlcSA8DjCKkMsVipC_mU-a8FHwULJdCkFyQwebP4FdI3W6rBLJqyVm-kaoicaXxz1BS2y3T8EtSW",
    lwa_app_id = "amzn1.sp.solution.5539b8b8-540d-436d-adfe-75eab1bd3eef",
    lwa_client_secret = "amzn1.oa2-cs.v1.eb00728cdc563d873782ce1ab021b92f94329493eb37c945e2095542a9885b9e"
)

marketplace = Marketplaces.US

def getOrders():
    try:
        report_type = ReportType.GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL
        res = Reports(credentials=credentials,marketplace=marketplace)
        data = res.create_report(reportType=report_type,dataStartTime="2021-01-29")
        reportId = data.payload('reportId')
        res.get_report(reportId)

        while data.payload.get('processingStatus') not in [ProcessingStatus.DONE,ProcessingStatus.FATAL,ProcessingStatus.CANCELLED]:
            time.sleep(2)
            data=res.get_report(reportId)
            print(data.payload.get('processingStatus'))

        if data.payload.get('processingStatus') in [ProcessingStatus.FATAL,ProcessingStatus.CANCELLED]:
            print("Report Failed.")

        print(data.payload.get('processingStatus'))

        reportData = res.get_report_document(data.payload['reportDocumentId'],decrypt=True)
        reportUrl = reportData.payload.get('url')
        res = requests.get(reportUrl)

        print(reportUrl)
    except Exception as e:
        better_error_handling(e)
    
getOrders()

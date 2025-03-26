import requests
from datetime import datetime, timedelta, timezone
from helpers.messages import color_text
from helpers.file_ops import *
import sys
import requests
import time


created_after = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()

production_endpoint = "https://sellingpartnerapi-eu.amazon.com"
sandbox_endpoint = "https://sandbox.sellingpartnerapi-eu.amazon.com"


class SPAPIBase:
    def __init__(self,access_token):
        if access_token:
            self.access_token = access_token
            self.base_url = production_endpoint
            self.marketplace_id = "A21TJRUUN4KGV"
            self.headers = {
                "Authorization" : "access token",
                "x-amz-access-token": self.access_token,
                "Content-Type": "application/json",
                "Connection" : "keep-alive",
                "Accept": "application/json"
                }
            # Common parameters, individual ones will be added from the respective functions
            self.params = {"MarketplaceIds": self.marketplace_id}
    
            
    def make_request(self,endpoint,method,params=None,requested_key=None,data=None):
        """
        lets assign status code as 429 in the beginning and let it update once 200 is obtained
        """
        status_code = None
        url = self.base_url + endpoint 
        color_text(f"Endpoint : {endpoint}","blue",end=", ")
        request_dict = {
            "get" : requests.get(url, headers=self.headers, params = self.params,timeout=10),
            "post" : requests.post(url, headers=self.headers, params= self.params,json=data,timeout=10),
            "delete" : requests.delete(url, headers=self.headers,timeout=10)
        }
        try: 
            response = request_dict.get(method.lower(),None)
            
            status_code = response.status_code
            
            color_text(f"Status code : {status_code}","green" if 200 <= status_code < 400 else "red")
            
            """
            a while loop should look for if the status code is 429
            """
        except requests.exceptions.RequestException as e: 
            better_error_handling(e)
        except requests.exceptions.ConnectTimeout:
            color_text("Timeout","red")
        except Exception as e:
            better_error_handling(e)
        else:
            if method.lower() != "get" and response:
                return response.json()
            else:
                pages = []
                response_payload = response.json().get('payload',None)
                if response_payload:
                    next_token = response_payload.get("NextToken",None) if response else None
                    if next_token:
                        # need to filter further and add Orders / Reports etc
                        if requested_key:
                            pages += (response_payload.get(requested_key))
                        else:
                            pages += response_payload
                            
                        while next_token:
                            # the payload is added to the pages list
                            # now we need to request the next page by updating the params first
                            if next_token != None:
                                self.params["NextToken"] = next_token
                                # requesting the next page and get the payload from it
                                next_page = requests.get(
                                    url, headers=self.headers, params = self.params,timeout=10
                                )
                                if next_page:
                                    next_payload = next_page.json().get('payload',None)
                                    if next_payload:
                                        # adding the next page to the list the moment next page is received
                                        if requested_key:
                                            pages += (next_payload.get(requested_key))
                                        else:
                                            pages += (next_payload)
                                        # updating the next token to a value or None if unavailable
                                        next_token = next_payload.get("NextToken",None)
                        color_text(f"Requested Key : {requested_key}, Data length : {len(pages)}")
                        return pages
                    else:
                        return response_payload.get(requested_key)
                    
                else:
                    return response


class Orders(SPAPIBase):
    def getOrders(
            self,CreatedAfter=None,CreatedBefore=None,OrderStatuses=None,LastUpdatedAfter=None,
            PaymentMethods=None,EasyShipShipmentStatuses=None,EarliestShipDate=None,
            LatestShipDate=None,FulfillmentChannels=None
        ):
        
        order_statuses = [
        "PendingAvailability","Pending","Unshipped",
        "PartiallyShipped","Shipped","InvoiceUnconfirmed",
        "Canceled","Unfulfillable"
    ]
        endpoint = "/orders/v0/orders"
        #color_text(message=f"Before update : {self.params}",color="red")
        self.params.update(
            {
                "CreatedAfter" : CreatedAfter,
                "CreatedBefore" : CreatedBefore,
                "OrderStatuses": OrderStatuses,
                "LastUpdatedAfter" : LastUpdatedAfter,
                "PaymentMethods" : PaymentMethods,
                "FulfillmentChannels":FulfillmentChannels,
                "EarliestShipDate" : EarliestShipDate, 
                "LatestShipDate" : LatestShipDate,
                "EasyShipShipmentStatuses" : EasyShipShipmentStatuses
            }
        ) 
        if not (CreatedAfter or  LastUpdatedAfter or OrderStatuses):
            color_text(message="Either the CreatedAfter or the LastUpdatedAfter parameter is required,\nBoth cannot be empty",color="red")
            return None
        else:
            if OrderStatuses in order_statuses:
                response_payload = self.make_request(
                    endpoint=endpoint,method="get",params=self.params,requested_key="Orders"
                )
                if response_payload:
                    return response_payload


    def getOrder(self,orderId):
        endpoint = f"/orders/v0/orders/{orderId}"
        self.params.update ({"orderId" : orderId})
        
    def getOrderBuyerInfo(self,orderId):
        endpoint = f"/orders/v0/orders/{orderId}/buyerInfo"
        self.params.update ({"orderId" : orderId})

    def getOrderAddress(self,):
        pass 

    def getOrderItems(self,):
        pass

    def getOrderItemsBuyerInfo(self,):
        pass

    def updateShipmentStatus(self,):
        pass

    def getOrderRegulatedInfo(self,):
        pass

    def updateVerificationStatus(self,):
        pass

    def confirmShipment(self,):
        pass
    

class EasyShip(SPAPIBase):
    # https://developer-docs.amazon.com/sp-api/docs/easy-ship-api-v2022-03-23-reference#listhandoverslots
    """
    Operations
    listHandoverSlots - post
    getScheduledPackage
    createScheduledPackage
    updateScheduledPackages
    createScheduledPackageBulk
    """ 
    version = "2022-03-23"

    def listHandoverSlots(self,ListHandoverSlotsRequest):
        endpoint = f"/easyShip/{self.version}/timeSlot"
        self.params.update(
            {"ListHandoverSlotsRequest" : ListHandoverSlotsRequest}
        )
        rate = 1
        burst = 5
        #self.params.update({"ListHandoverSlotsRequest" : 0})
        return super().execute_request(endpoint = endpoint,method='post',params=self.params,burst=5)
    
    def getScheduledPackage(self,amazonOrderId):
        endpoint = f"/easyShip/{self.version}/package"
        self.params.update(
            { "amazonOrderId" : amazonOrderId }
        )
        print(f"Params : {self.params}")
        print(self.headers)
        return super().execute_request(endpoint=endpoint,params=self.params,method='get',burst=5)
    
    def createScheduledPackage(self):
        pass
    def updateScheduledPackages(self):
        pass
    def createScheduledPackageBulk(self):
        endpoint = f"/easyShip/{self.version}/packages/bulk"


class Reports(SPAPIBase):
    # https://developer-docs.amazon.com/sp-api/docs/reports-api-v2021-06-30-reference        
    def createReport(self,reportType,reportOptions=None,dataStartTime=None,dataEndTime=None):
        endpoint = '/reports/2021-06-30/reports'
        data = {
            "reportType": reportType,
            "reportOptions" : reportOptions,
            "marketplaceIds" : [self.marketplace_id],
            "dataStartTime" : dataStartTime,
            "dataEndTime" : dataEndTime
        }
        created_report = self.make_request(endpoint=endpoint,method="post",params=self.params, data = data)
        color_text(created_report)
        if created_report:
            report_id = created_report.get("reportId",None)
            return report_id if report_id else None

    def getReport(self,reportId):
        endpoint = f"/reports/2021-06-30/reports/{reportId}"
        
        if not ("reportId" in self.params.keys() and self.params["reportId"]):
            self.params.update({"reportId" : reportId})
            color_text("report id added to params")
            
        
        report_status = self.make_request(endpoint=endpoint,method="get",params=self.params)
        return report_status.json()

    # Report Df creator
    def report_df_creator(self,report_type,start_date,end_date):
        try:
            # report creation
            report_id = None
            if not report_id:
                report_id = self.createReport(
                    reportType=report_type,dataStartTime=start_date,dataEndTime=end_date
                )
            self.params.update({"reportId" : report_id})
            
            # report schedule
            schedule = self.getReportSchedules(reportTypes=report_type)
            color_text(schedule,"blue")
            
            while True:
                # report processing
                rep_processing = self.getReport(report_id)
                #processing_status = doc_resp.get("processingStatus",None)
                report_status = (rep_processing.get("processingStatus"))
                if report_status == "DONE":
                    rep_doc_id = rep_processing.get("reportDocumentId")
                    color_text(f"report doc id : {rep_doc_id}")
                    if rep_doc_id:
                        document_response = self.getReportDocument(reportDocumentId = rep_doc_id).json()
                        color_text(document_response,"blue")
                        if document_response:
                            color_text(document_response)
                            df_url = document_response.get("url")
                            rep_df = requests.get(df_url)
                            color_text(rep_df)
                            return rep_df

                elif report_status in  ("CANCELLED","FATAL"):
                    color_text(report_status,"red")
                    return None
                color_text(rep_processing)
                time.sleep(15)

        except AttributeError as ae:
            #color_text(f"Attribute Error found :\n {ae}")
            better_error_handling(ae)
        except Exception as e:
            better_error_handling(e)
        else:
            pass
                        
            
    def getReports(self,reportTypes=None,processingStatuses=None,marketplaceIds=None,
            pageSize=None,createdSince=None,CreatedUntil=None,nextToken=None
        ):
        endpoint = "/reports/2021-06-30/reports"
        self.params.update({ 
            "reportTypes" : reportTypes,
            "processingStatuses" : processingStatuses,
            "marketplaceIds" : marketplaceIds,
            "pageSize" : pageSize,
            "createdSince" : createdSince,
            "createdUntil" : CreatedUntil,
            "nextToken" : nextToken
        })
        
    def cancelReport(self,reportId):
        endpoint = f"/reports/2021-06-30/reports/{reportId}"
        self.params.update({"reportId" : reportId})
    # Report scheduling
    def createReportSchedule(self):
        endpoint = f"/reports/2021-06-30/schedules"
        
    def getReportSchedule(self,reportScheduleId):
        endpoint = f"/reports/2021-06-30/schedules/{reportScheduleId}"
        
    def getReportSchedules(self,reportTypes):
        endpoint = "/reports/2021-06-30/schedules"
        self.params.update({"reportTypes" : reportTypes})
        
    def cancelReportSchedule(self,reportScheduleId):
        endpoint = f"/reports/2021-06-30/schedules/{reportScheduleId}"

    def getReportDocument(self,reportDocumentId):
        endpoint = f"/reports/2021-06-30/documents/{reportDocumentId}"
        self.params.update({"reportDocumentId" : reportDocumentId})
        return super().make_request(
            endpoint=endpoint,params=self.params,method='get'
        )
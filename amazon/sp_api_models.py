import requests
from datetime import datetime, timedelta, timezone
from helpers.messages import color_text
from helpers.file_ops import *
import sys
import requests


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
    
            
    def make_request(self,endpoint,method,params=None,requested_key=None):
        """
        lets assign status code as 429 in the beginning and let it update once 200 is obtained
        """
        status_code = 400
        url = self.base_url + endpoint 
        request_dict = {
            "get" : requests.get(url, headers=self.headers, params = self.params,timeout=10),
            "post" : requests.post(url, headers=self.headers, params= self.params,timeout=10),
            "delete" : requests.delete(url, headers=self.headers,timeout=10)
        }
        try: 
            response = request_dict.get(method.lower(),None)
            codes = {
                200 : "green", 429 : "red"
            }
            color_text(response.status_code,codes[response.status_code])
            
            """
            a while loop should look for if the status code is 429
            """
        except requests.exceptions.TooManyRedirects:
            color_text("429")
        except Exception as e:
            better_error_handling(e)
        else:
            if method.lower() != "get" and response:
                return response
            else:
                pages = []
                response_payload = response.json().get('payload',None)
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
                    return response.json()


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
        if not (CreatedAfter or  LastUpdatedAfter):
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
            "reportType":reportType,
            "reportOptions" : reportOptions,
            "marketplaceIds" : [self.marketplace_id],
            "dataStartTime" : dataStartTime,
            "dataEndTime" : dataEndTime
        }
    
    def getReports(self,reportTypes=None,processingStatuses=None,marketplaceIds=None,
                   pageSize=None,createdSince=None,CreatedUntil=None,nextToken=None):
        endpoint = "/reports/2021-06-30/reports"
        self.params.update({ 
            "reportTypes" : reportTypes,
            "processingStatuses" : processingStatuses,
            "marketplaceIds" : marketplaceIds,
            "pageSize" : pageSize,
            "cretedSince" : createdSince,
            "createdUntil" : CreatedUntil,
            "nextToken" : nextToken
        })
        
    
    def getReport(self,reportId):
        endpoint = f"/reports/2021-06-30/reports/{reportId}"
        self.params.update({"reportId" : reportId})
        

    def cancelReport(self,reportId):
        endpoint = f"/reports/2021-06-30/reports/{reportId}"
        self.params.update({"reportId" : reportId})
        

    def getReportSchedules(self,reportTypes):
        endpoint = "/reports/2021-06-30/schedules"
        self.params.update({"reportTypes" : reportTypes})
        

    def createReportSchedule(self):
        endpoint = f"/reports/2021-06-30/schedules"

    def getReportSchedule(self,reportScheduleId):
        endpoint = f"/reports/2021-06-30/schedules/{reportScheduleId}"

    def cancelReportSchedule(self,reportScheduleId):
        endpoint = f"/reports/2021-06-30/schedules/{reportScheduleId}"

    def getReportDocument(self,reportDocumentId):
        endpoint = f"/reports/2021-06-30/documents/{reportDocumentId}"
        self.params.update({"reportDocumentId" : reportDocumentId})
        return super().execute_request(endpoint=endpoint,params=self.params,
                                       method='get',burst=15)
        

    # Report Df creator
    def report_df_creator(self,report_type,start_date,end_date):
        try:
            df = self.createReport(
                reportType=report_type,dataStartTime=start_date,dataEndTime=end_date
            )
            return df
        except AttributeError as ae:
            color_text(f"Attribute Error found :\n {ae}")
        except Exception as e:
            better_error_handling(e)
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
            
    def make_request(self,endpoint,method,params=None):
        status_code = 400
        url = self.base_url + endpoint 
        request_dict = {
            "get" : requests.get(url, headers=self.headers, params = params,timeout=10),
            "post" : requests.post(url, headers=self.headers, params= params,timeout=10),
            "delete" : requests.delete(url, headers=self.headers,timeout=10)
        }
        try: 
            response = request_dict.get(method.lower(),None)
        except requests.exceptions.TooManyRedirects:
            color_text("429")
        except Exception as e:
            better_error_handling(e)
        else:
            response = response.json().get('payload',None)
            next_token = response.get("NextToken",None) if response else None
            color_text(next_token)
            if response:
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
        color_text(sys.argv)
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
                response_payload = self.make_request(endpoint=endpoint,method="get",params=self.params)
                return response_payload.get("Orders",None) if response_payload else None
            
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
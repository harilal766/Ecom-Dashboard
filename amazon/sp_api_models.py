import requests
from datetime import datetime, timedelta, timezone
from helpers.messages import color_text
from helpers.file_ops import *
from amazon.authorization import *
import time

created_after = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()


production_endpoint = "https://sellingpartnerapi-eu.amazon.com"
sandbox_endpoint = "https://sandbox.sellingpartnerapi-eu.amazon.com"

import logging
import requests

class SPAPIBase:
    def __init__(self,base_url=production_endpoint,marketplace_id="A21TJRUUN4KGV"):
        color_text(message="Initializing SPAPIBase")
        access_token = get_or_generate_access_token()
        if access_token != None:
            self.access_token = access_token
            self.base_url = base_url
            self.marketplace_id = marketplace_id
            self.headers = {
                "Authorization" : "access token",
                "x-amz-access-token": self.access_token,
                "Content-Type": "application/json",
                "Connection" : "keep-alive",
                "Accept": "application/json"
                }
            # Common parameters, individual ones will be added from the respective functions
            self.params = {"MarketplaceIds": self.marketplace_id}
            status = f"Params : {getattr(self,'params','Not Initialized')}"
            #color_text(message=status)
            self.success_codes = {200,201}
            self.rate_limit = {}
        else:
            color_text(message="Access token returned None, Please check",color="red")

    def dynamic_request_delay():
        pass

    def make_request(self,endpoint,method,params=None,json_input=None):
        url = self.base_url + endpoint 
        try: 
            if method.lower() == 'get':
                    response = requests.get(url, headers=self.headers,params = params,timeout=10)
            elif method.lower() == 'post':
                    response = requests.post(url, headers=self.headers,json = json_input,timeout=10)
            elif method.lower() == 'delete':
                response = requests.delete(url, headers=self.headers,timeout=10)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            if response != None :
                return response
            else:
                color_text(message="Response Error",color="red")
                return None
            
        except Exception as e:
            better_error_handling(e)
    
    def endpoint_checker(self):
        color_text(message=self)
        if self.base_url == sandbox_endpoint:
            color_text(message="Endpoint : sandbox endpoint",color="blue")
        else:
            color_text(message="Endpoint : production endpoint",color="blue")

    def limit_analyzer(response):
        try:
            color_text(message=f"Headers : \n{response.headers}",color="red")

            rate_limit = response.headers.get('x-amzn-RateLimit-Limit',None)
            remaining_rate_limit = response.headers.get('x-amzn-RateLimit-Remaining',None)
            
            if not (rate_limit == None) or (remaining_rate_limit == None):
                color_text(message=f"Limit : {rate_limit}, Remaining Limit : {remaining_rate_limit}, Request Count : {request_count}/{burst}")
        
        except Exception as e:
            better_error_handling(e)         

    def manage_request(self,endpoint,method,burst,json_input=None,params=None,payload=None):
        self.endpoint_checker()
        try:
            response = self.make_request(endpoint=endpoint,method=method,params=params,
                                             json_input=json_input)
            
            self.limit_analyzer(response=response)

            if response.status_code == 200:
                response = response.json()

                if payload != None:
                    return response.get(payload)
                else:
                    return response
                
            else:
                return color_text(message="The status code is not 200",color="red")
            
        except:
            pass

    def execute_request(self,endpoint,method,burst,json_input=None,params=None,payload=None):
        retry = 5; delay=1

        self.endpoint_checker()

        # detecting burst limit should have top priority...
        for request_count in range(burst):
            try:
                # make sure the endpoint have a "/" at the begining and does not end with "/"
                if endpoint[0] != '/':
                    endpoint = '/'+endpoint
                status_end = " | "

                url = self.base_url+endpoint
                
                # making requests is converted to a seperate function
                response = self.make_request(endpoint=endpoint,method=method,params=params,
                                             json_input=json_input)

                color_text(message=f"Headers {request_count}: \n{response.headers}",color="red")

                rate_limit = response.headers.get('x-amzn-RateLimit-Limit',None)
                remaining_rate_limit = response.headers.get('x-amzn-RateLimit-Remaining',None)

                color_text(message=f"Limit : {rate_limit}, Remaining Limit : {remaining_rate_limit}, Request Count : {request_count}/{burst}")
                
                #color_text(message=response.headers,color="red")
                
                if request_count == burst:
                    color_text(message="Burst Limit reached",color="red")

                if response.status_code == 429:
                    delay *=2
                    time.sleep(delay)
                    color_text(message=f"Rate limit reached, retrying in {delay} seconds.",color='red')
                elif response.status_code >= 400:
                    response.raise_for_status()
                    break
                else:
                    color_text(message=request_count,color="red")
                    request_count += 1
                    time.sleep(1) # to delay based on the rate limit which is negligible
                    response_data = response.json()
                    return response_data.get(payload,None) if payload else response_data
                
            except AttributeError as e:
                color_text(message=f"Attribute Error Found : {e}\n{response}\n-----------------------------------",color='red')
                break
            except requests.exceptions.RequestException as e:
                better_error_handling(f"Error : {e}")
                break
        return None

class Orders(SPAPIBase):

    def getOrders(self,CreatedAfter=None,CreatedBefore=None,
                  OrderStatuses=None,
                  LastUpdatedAfter=None,
                  PaymentMethods=None,EasyShipShipmentStatuses=None,
                  EarliestShipDate=None,LatestShipDate=None,
                  FulfillmentChannels=None):
        
        order_statuses = [
        "PendingAvailability","Pending","Unshipped",
        "PartiallyShipped","Shipped","InvoiceUnconfirmed",
        "Canceled","Unfulfillable"
    ]
        """
        
        Note: Either the CreatedAfter parameter or the LastUpdatedAfter parameter is required.
        Both cannot be empty. CreatedAfter or CreatedBefore cannot be set when LastUpdatedAfter is set.

        Note: LastUpdatedBefore is optional when LastUpdatedAfter is set. But if specified, LastUpdatedBefore
        must be equal to or after the LastUpdatedAfter date and at least two minutes before current time.
        
        Possible values of EasyShipShipmentStatuses :
        - PendingSchedule (The package is awaiting the schedule for pick-up.)
        - PendingPickUp (Amazon has not yet picked up the package from the seller.)
        - PendingDropOff (The seller will deliver the package to the carrier.)
        - LabelCanceled (The seller canceled the pickup.)
        - PickedUp (Amazon has picked up the package from the seller.)
        - DroppedOff (The package is delivered to the carrier by the seller.)
        - AtOriginFC (The packaged is at the origin fulfillment center.)
        - AtDestinationFC (The package is at the destination fulfillment center.)
        - Delivered (The package has been delivered.)
        - RejectedByBuyer (The package has been rejected by the buyer.)
        - Undeliverable (The package cannot be delivered.)
        - ReturningToSeller (The package was not delivered and is being returned to the seller.)
        - ReturnedToSeller (The package was not delivered and was returned to the seller.)
        - Lost (The package is lost.)
        - OutForDelivery (The package is out for delivery.)
        - Damaged (The package was damaged by the carrier.)
        """
        endpoint = "/orders/v0/orders"
        #color_text(message=f"Before update : {self.params}",color="red")
        self.params.update({"CreatedAfter" : CreatedAfter,
                            "CreatedBefore" : CreatedBefore,
                            "OrderStatuses": OrderStatuses,
                            "LastUpdatedAfter" : LastUpdatedAfter,
                            "PaymentMethods" : PaymentMethods,"FulfillmentChannels":FulfillmentChannels,
                            "EarliestShipDate" : EarliestShipDate, "LatestShipDate" : LatestShipDate,
                            "EasyShipShipmentStatuses" : EasyShipShipmentStatuses}) 
         
        #color_text(message=f"After update : {self.params}")
        """
        Note: Either the CreatedAfter parameter or the LastUpdatedAfter parameter is required.
        Both cannot be empty. CreatedAfter or CreatedBefore cannot be set when LastUpdatedAfter is set.
        """
        if (CreatedAfter != None) or (LastUpdatedAfter != None):
            # Verification conditions.
            if OrderStatuses not in order_statuses:
                return color_text(message="The order status you gave is not available in sp api",color="red")
            #breakpoint()
            response = super().execute_request(endpoint=endpoint,params=self.params,
                                                payload='payload',method='get',burst=20)
            if response != None:
                #color_text(message=f"{response}\n+++++++++++++++++",color="blue")
                return response.get("Orders")
            
            else:
                color_text(message=f"getOrders response : {response},please check",color="red")
        elif CreatedAfter == None and LastUpdatedAfter == None:
            return color_text(message="Either the CreatedAfter or the LastUpdatedAfter parameter is required,\nBoth cannot be empty",color="red")

    def getOrder(self,orderId):
        endpoint = f"/orders/v0/orders/{orderId}"
        self.params.update ({"orderId" : orderId})
        return super().execute_request(endpoint=endpoint,params=self.params,
                                       payload='payload',method='get',burst=30)
    
    def getOrderBuyerInfo(self,orderId):
        endpoint = f"/orders/v0/orders/{orderId}/buyerInfo"
        self.params.update ({"orderId" : orderId})
        return super().execute_request(endpoint=endpoint,params=self.params,method='get',burst=30
                                       ,delay=1)
    
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
    """
    Operations

    listHandoverSlots - post
    getScheduledPackage
    createScheduledPackage
    updateScheduledPackages
    createScheduledPackageBul
    """ 
    def listHandoverSlots(self):
        endpoint = "/easyShip/2022-03-23/timeSlot"
        rate = 1
        burst = 5
        #self.params.update({"ListHandoverSlotsRequest" : 0})
        return super().execute_request(endpoint = endpoint,method='post',params=self.params,burst=5)
    
    def getScheduledPackage(self,amazonOrderId):
        endpoint = "/easyShip/2022-03-23/package"
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
        """

        """
        endpoint = "/easyShip/2022-03-23/packages/bulk"
        

class Reports(SPAPIBase):
    # https://developer-docs.amazon.com/sp-api/docs/reports-api-v2021-06-30-reference        
    def createReport(self,reportType,reportOptions=None,dataStartTime=None,dataEndTime=None):
        endpoint = '/reports/2021-06-30/reports'
        data = {"reportType":reportType,
                "reportOptions" : reportOptions,
                "marketplaceIds" : [self.marketplace_id],
                "dataStartTime" : dataStartTime,
                "dataEndTime" : dataEndTime}
        return super().execute_request(method='post',endpoint=endpoint,
                                       json_input=data,burst=15)
    
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
        response = super().execute_request(endpoint=endpoint,params=self.params,
                                           payload='reports',method='get',burst=10)
        return response
    
    def getReport(self,reportId):
        endpoint = f"/reports/2021-06-30/reports/{reportId}"
        self.params.update({"reportId" : reportId})
        return super().execute_request(endpoint=endpoint,params=self.params,
                                       method='get',burst=15)

    def cancelReport(self,reportId):
        endpoint = f"/reports/2021-06-30/reports/{reportId}"
        self.params.update({"reportId" : reportId})
        return super().execute_request(endpoint=endpoint,params=self.params,
                                       method='delete',burst=10)

    def getReportSchedules(self,reportTypes):
        endpoint = "/reports/2021-06-30/schedules"
        self.params.update({"reportTypes" : reportTypes})
        return super().execute_request(endpoint=endpoint,params=self.params,
                                       method='get',burst=10)

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
        




class Shipping(SPAPIBase):
    pass

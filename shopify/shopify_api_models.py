import requests,json
from helpers.messages import *
import re


class ShopifyApiBase():
    def __init__(self,access_token,storename):
        if access_token and storename:
            self.access_token = access_token
            self.storename = storename
            
            self.headers = {
            "Content-Type" : 'application/json',
            "X-Shopify-Access-Token" : self.access_token
            }
            
    def make_shopify_request(self,endpoint,method):
        try:
            domain = f"https://{self.storename}.myshopify.com/admin/api/"
            limit = "limit=100"
            version = "/2025-01/"
            api_url = domain + version + endpoint + limit
            request_dict = {
                "get" : requests.get(api_url,headers=self.headers),
                "post" : requests.post(api_url,headers=self.headers),
            }
            # finding the model from the endpoint
            model = re.search(r'[a-z]+\.json\b',endpoint)
            color_text(message=f"Detected Model : {str(model)} from : {endpoint}")
            
        except Exception as e:
            better_error_handling(e)
        else:
            response = request_dict.get(method.lower(),None)
            if response.status_code==200:
                return response.json()
    
class Sh_Orders(ShopifyApiBase):
    def get_orders(self):
        return self.make_shopify_request(endpoint=f"orders.json?",method="get")["orders"]
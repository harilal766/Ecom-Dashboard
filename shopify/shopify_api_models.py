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
            fields = "limit=2"
            version = "/2024-01/"
            base_url = domain + version +endpoint + fields
            request_dict = {
                "get" : requests.get(base_url,headers=self.headers),
                "post" : requests.post(base_url,headers=self.headers),
            }
            # finding the model from the endpoint
            model = re.search(r'[a-z]+\.json\b',endpoint)
            color_text(message=f"Detected Model : {str(model)} from : {endpoint}")
            
        except Exception as e:
            better_error_handling(e)
        else:
            result = request_dict.get(method.lower(),None)
            if result:
                return result.json()
    
class Sh_Orders(ShopifyApiBase):
    def get_orders(self):
        return self.make_shopify_request(endpoint=f"orders.json?",method="get")
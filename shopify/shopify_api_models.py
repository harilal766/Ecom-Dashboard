import requests,json
from helpers.messages import *


class ShopifyApiBase():
    def __init__(self,access_token,storename):
        if access_token and storename:
            self.access_token = access_token
            self.storename = storename
            
            self.headers = {
            "Content-Type" : 'application/json',
            "X-Shopify-Access-Token" : self.access_token
            }
            
    def make_request(self,endpoint,method):
        try:
            domain = f"https://{self.storename}.myshopify.com/admin/api/"
            fields = "limit=2"
            base_url = domain + endpoint + fields
            request_dict = {
                "get" : requests.get(base_url,headers=self.headers),
                "post" : requests.post(base_url,headers=self.headers),
            }
        except Exception as e:
            better_error_handling(e)
        else:
            result = request_dict.get(method.lower(),None)
            if result:
                return result.json()
        
        
class Sh_Products(ShopifyApiBase):
    def get_products(self):
        return self.make_request(endpoint=f"/2024-01/products.json?",method="get")
    
class Sh_Orders(ShopifyApiBase):
    def get_orders(self):
        return self.make_request(endpoint=f"/2024-01/orders.json?",method="get")
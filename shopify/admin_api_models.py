import requests,json


class ShopifyApiBase():
    def __init__(self,api_key,api_secret,access_token,storename):
        if api_key and api_secret and access_token and storename:
            self.headers = {
            "Content-Type" : 'application/json',
            "X-Shopify-Access-Token" : access_token
            }
            
    def make_request(self,endpoint,method):
        try:
            domain = f"https://{storename}.myshopify.com/admin/api/"
            endpoint = "/2024-01/products.json?"
            fields = "limit=2"
            base_url = domain + endpoint + fields
            request_dict = {
                "get" : requests.get(base_url,headers=self.headers),
                "post" : requests.post(base_url,headers=self.headers),
            }
        except:
            pass
        else:
            pass
        
        
class Products(ShopifyApiBase):
    pass
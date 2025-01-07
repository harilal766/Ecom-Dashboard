from django.db import models

# Create your models here.
class Configuration(models.Model):
    platform = models.CharField(max_length=200,default="Ecom")
    account_name = models.CharField(max_length=400,unique=True,default="seller")
    total_orders = models.IntegerField(default=0)
    last_schedule = models.DateTimeField(default=None)


class SPAPI_Credential(models.Model):
    client_id = models.CharField(max_length=500)
    client_secret = models.CharField(max_length=500)
    refresh_token = models.CharField(max_length=500)
    access_token = models.CharField(max_length=500)
    access_token_updation_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.access_token_updation_time)
    

class Store(models.Model):
    platform = models.CharField(max_length=200,default="Ecom")
    store_name = models.CharField(max_length=400,unique=True,default="seller")
    

    

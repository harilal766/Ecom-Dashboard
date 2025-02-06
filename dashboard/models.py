from django.db import models


# Create your models here.
class Configuration(models.Model):
    platform = models.CharField(max_length=200,default="Ecom")
    account_name = models.CharField(max_length=400,unique=True,default="seller")
    total_orders = models.IntegerField(default=0)
    last_schedule = models.DateTimeField(default=None)



    

class Store(models.Model):
    store_name = models.CharField(max_length=400,unique=True,default="seller")
    platform = models.CharField(max_length=200,default="Ecom")
    

    
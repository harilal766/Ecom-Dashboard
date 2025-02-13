from django.db import models


# Create your models here.
class Configuration(models.Model):
    platform = models.CharField(max_length=200,default="Ecom")
    account_name = models.CharField(max_length=400,unique=True,default="seller")
    total_orders = models.IntegerField(default=0)
    last_schedule = models.DateTimeField(default=None)

    

class Store(models.Model):
    store_name = models.CharField(max_length=400,unique=True,default="seller")
    slug = models.SlugField(max_length=100,unique=True,blank=True,default = str(store_name).replace(" ","_"))
    platform = models.CharField(max_length=200,default="Ecom")

    def __str__(self):
        return self.store_name
    

    
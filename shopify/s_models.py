from django.db import models
from django.contrib.auth.models import User
from dashboard.d_models import StoreProfile
# Create your models here.


class ShopifyApiCredentials(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    store = models.ForeignKey(StoreProfile,on_delete=models.CASCADE)
    api_Key = models.CharField(max_length=100)
    api_secret = models.CharField(max_length=100)
    access_token = models.CharField(max_length=100)
    store_name = models.CharField(max_length=15,blank=True,null=True)
    
    def __str__(self):
        return f"{self.store}"
    
    

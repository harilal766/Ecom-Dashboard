from django.db import models
from django.contrib.auth.models import User 
from django.contrib.auth.models import User 
# Create your models here.
class SPAPI_Credential(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    client_id = models.CharField(max_length=500)
    client_secret = models.CharField(max_length=500)
    refresh_token = models.CharField(max_length=500)
    access_token = models.CharField(max_length=500)
    access_token_updation_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.access_token_updation_time)
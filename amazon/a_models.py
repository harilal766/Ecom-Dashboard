from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User 
from dashboard.d_models import StoreProfile
from helpers.messages import better_error_handling
from datetime import datetime
import requests
from helpers.messages import color_text
# Create your models here.
class SPAPI_Credential(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    store = models.ForeignKey(StoreProfile,on_delete=models.CASCADE)

    client_id = models.CharField(max_length=500)
    client_secret = models.CharField(max_length=500)
    refresh_token = models.CharField(max_length=500)
    # the access token is generated with the 3 credentials given on top
    access_token = models.CharField(max_length=500,default=None)
    access_token_updation_time = models.DateTimeField(default=None)


    def __str__(self):
        return f"{self.store} - updated at {str(self.access_token_updation_time)}"
    
    def is_access_token_expired(self):
        token_expiry = 3600
        current_time = datetime.now()
        if self.access_token_updation_time:
            time_difference = current_time - self.access_token_updation_time.replace(tzinfo=None)
            difference_seconds = time_difference.total_seconds()
            return difference_seconds >= token_expiry
            #return self.access_token_updation_time
        else:
            return None

    def generate_access_token(self):
        url = "https://api.amazon.com/auth/o2/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        try:
            response = requests.post(url, headers= headers, data=data)
            response = response.json()
            refreshed_access_token = response.get("access_token")
            self.access_token = refreshed_access_token
            self.access_token_updation_time = datetime.now()
            self.save()
            print(self.access_token_updation_time)
            return refreshed_access_token
        except Exception as e:
            better_error_handling(e)

    def get_or_refresh_access_token(self):
        if self.is_access_token_expired() == True:
            color_text("Access token expired, Refreshing....","red")
            return self.generate_access_token()
        else:
            color_text("Reusing Access token","green")
            return self.access_token

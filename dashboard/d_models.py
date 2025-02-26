from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.

class Store(models.Model):
    store_name = models.CharField(max_length=400,unique=True,default="seller")
    slug = models.SlugField(max_length=100,unique=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    platform = models.CharField(max_length=200,default="Ecom")

    def __str__(self):
        return f"{self.store_name} : {self.platform}"
    
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.store_name)
        return super().save(*args,**kwargs)
    

    
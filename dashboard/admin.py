from django.contrib import admin
from dashboard.d_models import *

# Register your models here


admin.site.register(Configuration)


class Storeadmin(admin.ModelAdmin):
    list_display = ["store_name"]
    prepopulated_fields = {"slug" : ("store_name",)}
admin.site.register(Store,Storeadmin)
    



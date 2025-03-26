from django.contrib import admin
from amazon.a_models import SPAPI_Credential,SPAPI_Limits
# Register your models here.

class SPAPICredentialAdmin(admin.ModelAdmin):
    readonly_fields = ("access_token","access_token_updation_time")
admin.site.register(SPAPI_Credential, SPAPICredentialAdmin)

admin.site.register(SPAPI_Limits)
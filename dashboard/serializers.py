from dashboard.d_models import StoreDebrief
from rest_framework import serializers



class StoreDebriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreDebrief
        fields = "__all__"

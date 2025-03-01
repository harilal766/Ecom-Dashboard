from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


from dashboard.d_models import StoreProfile
class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreProfile
        fields = '__all__'

from rest_framework import serializers

class ShipmentSummarySerializer(serializers.Serializer):
    shipment_summary = serializers.DictField()
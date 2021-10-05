from rest_framework import serializers

from famis import models
from commons.serializers import UnitSerializer, RegionSerializer

# class FacilitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Facility
#         fields = '__all__'

class FacilityInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FacilityInfo
        fields = '__all__'

class FacilityMaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FacilityMaintenance
        fields = '__all__'

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Inventory
        fields = '__all__'
from rest_framework import serializers

from samb import models
from commons.serializers import UnitSerializer, RegionSerializer

class RosterOfTroopsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RosterOfTroops
        fields = '__all__'
 

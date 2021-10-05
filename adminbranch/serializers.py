from rest_framework import serializers

from adminbranch import models
from commons.serializers import UnitSerializer, RegionSerializer

class RosterOfTroopsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RosterOfTroops
        fields = '__all__'

class AdminMooeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AdminMooe
        fields = '__all__'

class AdminEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AdminEquipment
        fields = '__all__'

class IncomingCommunicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IncomingCommunication
        fields = '__all__'

class OutgoingCommunicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OutgoingCommunication
        fields = '__all__'
        

from rest_framework import serializers

from firepower import models
from commons.serializers import UnitSerializer, RegionSerializer

class ExpenditureAmmunitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExpenditureAmmunition
        fields = '__all__'
        
class ProgramsDemilitarizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProgramsDemilitarization
        fields = '__all__'

class ProgramsDisposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProgramsDisposal
        fields = '__all__'

class ProgramsRepairAndMaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProgramsRepairAndMaintenance
        fields = '__all__'

class ProgramsProcurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProgramsProcurement
        fields = '__all__'

class TOEMotherUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TOEMotherUnit
        fields = '__all__'

class TOEPaWideSerializer(serializers.ModelSerializer):
    class Meta:        
        model = models.TOEPaWide
        fields = '__all__'

class StatusOfFillUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StatusOfFillUp
        fields = '__all__'

class SparePartsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SpareParts
        fields = '__all__'

class AccessoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Accessories
        fields = '__all__'

class AmmunitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ammunition
        fields = '__all__'

class FirearmSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Firearm
        fields = '__all__'

class IncomingCommunicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IncomingCommunication
        fields = '__all__'

class OutgoingCommunicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OutgoingCommunication
        fields = '__all__'
        

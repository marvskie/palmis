from rest_framework import serializers

from camb import models
from commons.serializers import UnitSerializer, RegionSerializer

class DASProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DASProjects
        fields = '__all__'

class FMSProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FMSProjects
        fields = '__all__'

class SRDPProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SRDPProjects
        fields = '__all__'

class InternationalLogisticsActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InternationalLogisticsActivities
        fields = '__all__'

class DraftDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DraftDocuments
        fields = '__all__'

class ReferencesHelpfulLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReferencesHelpfulLinks
        fields = '__all__'

class ReferencesDefenseExhibitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReferencesDefenseExhibits
        fields = '__all__'

class ReferencesPoliciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReferencesPolicies
        fields = '__all__'

class ReferencesBrochuresSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReferencesBrochures
        fields = '__all__'

class IncomingCommunicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IncomingCommunication
        fields = '__all__'

class OutgoingCommunicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OutgoingCommunication
        fields = '__all__'
        

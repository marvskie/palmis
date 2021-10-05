from rest_framework import serializers

from tosb import models


class NomenclatureIcieSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NomenclatureIcie
        fields = ('id', 'name')

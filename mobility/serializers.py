from rest_framework import serializers

from mobility import models


class NomenclatureTireSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NomenclatureTire
        fields = ('id', 'name')


class NomenclatureBatterySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NomenclatureBattery
        fields = ('id', 'name')


class TypeSerializer(serializers.ModelSerializer):
    prepend = serializers.SerializerMethodField()

    class Meta:
        model = models.Type
        fields = ('id', 'name', 'prepend')

    def get_prepend(self, instance):
        return f'{instance.category.name}, {instance.name}'


class TonnageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tonnage
        fields = ('id', 'name')


class CategorySerializer(serializers.ModelSerializer):
    transport_type = serializers.ReadOnlyField(source='get_transport_type_display')

    class Meta:
        model = models.Category
        fields = ('id', 'transport_type', 'name')


class NomenclatureCUSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NomenclatureVehicle
        fields = ('id', 'name', 'vehicle_type', 'tonnage')


class NomenclatureSerializer(serializers.ModelSerializer):
    vehicle_type = TypeSerializer()
    tonnage = TonnageSerializer()

    class Meta:
        model = models.NomenclatureVehicle
        fields = ('id', 'name', 'vehicle_type', 'tonnage', 'nomenclature')


class VehicleRecordListSerializer(serializers.ModelSerializer):
    nomenclature = serializers.ReadOnlyField(source='nomenclature.nomenclature')
    serviceability = serializers.ReadOnlyField(source='serviceability.name')
    unit = serializers.ReadOnlyField(source='unit.name')

    class Meta:
        model = models.VehicleRecord
        fields = ('id', 'item_code', 'nomenclature', 'serviceability', 'unit', 'engine_no', 'chassis_no', 'plate_no')


class VehicleRecordRetrieveSerializer(serializers.ModelSerializer):
    nomenclature = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    serviceability = serializers.SerializerMethodField()
    acquisition_mode = serializers.SerializerMethodField()
    geographical_location = serializers.SerializerMethodField()
    unit = serializers.SerializerMethodField()
    pamu = serializers.SerializerMethodField()

    class Meta:
        model = models.VehicleRecord
        fields = ('id', 'item_code', 'category', 'nomenclature', 'serviceability', 'plate_no', 'engine_no',
                  'chassis_no', 'mvf', 'acquisition_year', 'acquisition_mode', 'geographical_location', 'location',
                  'unit', 'pamu', 'has_bfp', 'conduction_no', 'unit_price')

    def get_category(self, instance):
        return {
            'id': instance.nomenclature.vehicle_type.category_id,
            'name': instance.nomenclature.vehicle_type.category.name
        }

    def get_nomenclature(self, instance):
        return {
            'id': instance.nomenclature_id,
            'nomenclature': instance.nomenclature.nomenclature
        }

    def get_serviceability(self, instance):
        return {
            'id': instance.serviceability_id,
            'name': instance.serviceability.name
        }

    def get_acquisition_mode(self, instance):
        if instance.acquisition_mode_id:
            return {
                'id': instance.acquisition_mode_id,
                'name': instance.acquisition_mode.name
            }

    def get_geographical_location(self, instance):
        if instance.geographical_location:
            return {
                'code': instance.geographical_location,
                'name': instance.get_geographical_location_display()
            }

    def get_unit(self, instance):
        if instance.unit_id:
            return {
                'id': instance.unit_id,
                'name': instance.unit.name
            }

    def get_pamu(self, instance):
        if instance.unit_id:
            return {
                'id': instance.unit.pamu_id,
                'name': instance.unit.pamu.name
            }


class VehicleRecordMbCUSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VehicleRecord
        fields = ('id', 'nomenclature', 'serviceability', 'plate_no', 'engine_no', 'chassis_no', 'mvf',
                  'acquisition_year', 'acquisition_mode', 'geographical_location', 'location', 'unit', 'has_bfp',
                  'unit_price', 'conduction_no', 'unit')


class VehicleRecordPamuUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VehicleRecord
        fields = ('id', 'serviceability', 'mvf')


class RepairRecordCUSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RepairRecord
        fields = ('id', 'vehicle', 'requested_on', 'completed_on', 'implementation', 'authority', 'advice_no',
                  'period_covered', 'amount_released', 'has_fur', 'unit')

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        for implementation in models.REPAIR_IMPLEMENTATION:
            if ret['implementation'] == implementation[0]:
                ret['implementation'] = {'code': implementation[0], 'name': implementation[1]}
                break

        for quarter in models.QUARTER_CHOICES:
            if ret['period_covered'] == quarter[0]:
                ret['period_covered'] = {'code': quarter[0], 'name': quarter[1]}
                break

        ret['unit'] = {'id': instance.unit_id, 'name': instance.unit.name}

        return ret


class RepairRecordSerializer(serializers.ModelSerializer):
    implementation = serializers.SerializerMethodField()
    period_covered = serializers.SerializerMethodField()
    unit = serializers.SerializerMethodField()

    class Meta:
        model = models.RepairRecord
        fields = ('id', 'vehicle', 'requested_on', 'completed_on', 'implementation', 'authority', 'advice_no',
                  'period_covered', 'amount_released', 'has_fur', 'unit')

    def get_implementation(self, instance):
        return {
            'code': instance.implementation,
            'name': instance.get_implementation_display()
        }

    def get_period_covered(self, instance):
        if instance.period_covered:
            return {
                'code': instance.period_covered,
                'name': instance.get_period_covered_display()
            }

    def get_unit(self, instance):
        return {
            'id': instance.unit_id,
            'name': instance.unit.name
        }

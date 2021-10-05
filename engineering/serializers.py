from rest_framework import serializers

from engineering import models
from commons.serializers import UnitSerializer, RegionSerializer
from ppb.serializers import ObjectCodeSerializer


# class RepairRecordCUSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.RepairRecord
#         fields = ('id', 'building', 'requested_on', 'completed_on', 'authority', 'advice_no', 'period_covered',
#                   'amount_released', 'has_fur', 'unit')

#     def to_representation(self, instance):
#         ret = super().to_representation(instance)

#         ret['unit'] = {'id': instance.unit_id, 'name': instance.unit.name}

#         for quarter in models.QUARTER_CHOICES:
#             if ret['period_covered'] == quarter[0]:
#                 ret['period_covered'] = {'code': quarter[0], 'name': quarter[1]}
#                 break

#         return ret


# class RepairRecordSerializer(serializers.ModelSerializer):
#     period_covered = serializers.SerializerMethodField()
#     unit = serializers.SerializerMethodField()

#     class Meta:
#         model = models.RepairRecord
#         fields = ('id', 'building', 'requested_on', 'completed_on', 'authority', 'advice_no', 'period_covered',
#                   'amount_released', 'has_fur', 'unit')

#     def get_unit(self, instance):
#         return {
#             'id': instance.unit_id,
#             'name': instance.unit.name
#         }

#     def get_period_covered(self, instance):
#         if instance.period_covered:
#             return {
#                 'code': instance.period_covered,
#                 'name': instance.get_period_covered_display()
#             }


# class BuildingRecordListSerializer(serializers.ModelSerializer):
#     reservation = serializers.ReadOnlyField(source='reservation.name')
#     location = serializers.ReadOnlyField(source='reservation.location')
#     unit = serializers.ReadOnlyField(source='unit.name')
#     category = serializers.ReadOnlyField(source='category.name')

#     class Meta:
#         model = models.BuildingRecord
#         fields = ('id', 'building_code', 'description', 'reservation', 'location', 'unit', 'category')


# class BuildingRecordSerializer(serializers.ModelSerializer):
#     reservation = serializers.SerializerMethodField()
#     unit = serializers.SerializerMethodField()
#     category = serializers.SerializerMethodField()

#     class Meta:
#         model = models.BuildingRecord
#         fields = ('id', 'building_code', 'description', 'reservation', 'unit', 'category')

#     def get_category(self, instance):
#         return {
#             'id': instance.category_id,
#             'name': instance.category.name
#         }

#     def get_reservation(self, instance):
#         return {
#             'id': instance.reservation_id,
#             'name': instance.reservation.name,
#             'location': instance.reservation.location
#         }

#     def get_unit(self, instance):
#         return {
#             'id': instance.unit_id,
#             'name': instance.unit.name
#         }


# class BuildingRecordCUSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.BuildingRecord
#         fields = ('id', 'building_code', 'description', 'reservation', 'unit', 'category')


# class BuildingCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.BuildingCategory
#         fields = ('id', 'name', )


# class ReservationRecordSerializer(serializers.ModelSerializer):
#     region = RegionSerializer()

#     class Meta:
#         model = models.ReservationRecord
#         fields = ('id', 'name', 'location', 'region', 'lot_area', 'camp_administrator', 'code')


# class ReservationRecordCUSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.ReservationRecord
#         fields = ('id', 'name', 'location', 'region', 'lot_area', 'camp_administrator', 'code')


# class CoStatusSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.CoStatus
#         fields = ('id', 'name')


# class CoProjectRecordListSerializer(serializers.ModelSerializer):
#     status = serializers.ReadOnlyField(source='status.name')
#     end_user = serializers.ReadOnlyField(source='end_user.name')

#     class Meta:
#         model = models.CoProjectRecord
#         fields = ('id', 'project_name', 'status', 'end_user', 'contractor')


# class CoProjectRecordSerializer(serializers.ModelSerializer):
#     end_user = UnitSerializer()
#     object_code = ObjectCodeSerializer()
#     status = CoStatusSerializer()

#     class Meta:
#         model = models.CoProjectRecord
#         fields = ('id', 'project_name', 'end_user', 'original_cost', 'approved_budget', 'bid_amount', 'object_code',
#                   'status', 'contractor', 'start_construction', 'target_completion', 'actual_completion')


# class CoProjectRecordCUSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.CoProjectRecord
#         fields = ('id', 'project_name', 'end_user', 'original_cost', 'approved_budget', 'bid_amount', 'object_code',
#                   'status', 'contractor', 'start_construction', 'target_completion', 'actual_completion')


# ============== NEW PALMIS SERIALIZERS

class HeavyEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HeavyEquipment
        fields = '__all__'

class LightEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LightEquipment
        fields = '__all__'

class LightRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LightRecord
        fields = '__all__'

class WaterRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WaterRecord
        fields = '__all__'

class InsuranceOfBuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InsuranceOfBuilding
        fields = '__all__'

class SurveyTitlingFencingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SurveyTitlingFencing
        fields = '__all__'

class LotRentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LotRental
        fields = '__all__'

class DetailedArchitecturalAndEngineeringDesignSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DetailedArchitecturalAndEngineeringDesign
        fields = '__all__'

class ComprehensiveMasterDevelopmentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ComprehensiveMasterDevelopmentPlan
        fields = '__all__'

class CapitalOutlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CapitalOutlay
        fields = '__all__'

class InteragencyTransferFundSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InteragencyTransferFund
        fields = '__all__'

class BasesConversionAndDevelopmentAuthoritySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BasesConversionAndDevelopmentAuthority
        fields = '__all__'

class IncomingCommunicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IncomingCommunication
        fields = '__all__'

class OutgoingCommunicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OutgoingCommunication
        fields = '__all__'
        

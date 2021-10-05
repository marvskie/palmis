from rest_framework import serializers


from commons.models import Pamu, Fssu, Unit, Serviceability, AcquisitionMode, Region, ProcurementMode, Organization, \
    Role, Account, Sprs, Branch
from commons import consts


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ('id', 'name', 'code')


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name', 'code')


class OrganizationSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True)

    class Meta:
        model = Organization
        fields = ('id', 'name', 'code', 'roles')


class AccountSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    role = serializers.SerializerMethodField()
    division = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ('id', 'username', 'role', 'first_name', 'last_name', 'email', 'mobile_no', 'active', 'bypass_otp',
                  'division')

    def get_role(self, instance):
        role = instance.role
        return {
            'id': role.id,
            'name': role.name,
            'organization': role.organization.name
        }

    def get_division(self, instance):
        org_code = instance.role.organization.code

        if org_code == consts.FSSU:
            return {
                'id': instance.fssu_id,
                'name': instance.fssu.name
            }
        elif org_code == consts.PAMU:
            return {
                'id': instance.fssu_id,
                'name': instance.fssu.name
            }

        return None


class PamuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pamu
        fields = ('id', 'name', )


class FssuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fssu
        fields = ('id', 'name', 'code', )


class UnitSerializer(serializers.ModelSerializer):
    pamu = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = ('id', 'name', 'pamu')

    def get_pamu(self, instance):
        return {'id': instance.pamu_id, 'name': instance.pamu.name}


class SprsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprs
        fields = ('id', 'pamu', 'address')


class ServiceabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Serviceability
        fields = ('id', 'name', 'code', )


class AcquisitionModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcquisitionMode
        fields = ('id', 'name', 'code', )


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ('id', 'name', 'designation', 'island_group')


class ProcurementModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcurementMode
        fields = ('id', 'name', 'code', 'full_name')

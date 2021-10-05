from django.db.models import Sum, Q, F
from django.db import transaction
from rest_framework import serializers

from commons.serializers import ProcurementModeSerializer, UnitSerializer, PamuSerializer
from commons import consts
from ppb.models import ExpenseClass, ObjectCode, MissionArea, Dpg, ProgramObjective, Kma, MajorPap, SubPap, \
    SuggestedPap, Pawaf, PawafItem, StrategicObjective, PbdgObjective, StrategicProgram, PawafItemView, Status, \
    PawafItemEndUser, PawafItemBudgetBreakdown, FundRelease, FundReleaseItem, FundReleaseRecipient, FundReleaseSource, \
    FundReleaseAsa, FundReleaseAsaItem, KeyProgram
from ppb import consts as ppb_consts


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('id', 'code', 'name')


class ExpenseClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseClass
        fields = ('id', 'code', 'name', )


class ObjectCodeSerializer(serializers.ModelSerializer):
    expense_class = ExpenseClassSerializer(many=False, required=True)

    class Meta:
        model = ObjectCode
        fields = ('id', 'code', 'name', 'description', 'expense_class')


class MissionAreaSerializer(serializers.ModelSerializer):
    mission_area_group = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = MissionArea
        fields = ('id', 'mission_area_group', 'name', 'code', )

    def get_name(self, instance):
        return f'{instance.get_mission_area_group_display()}: {instance.name}'

    def get_mission_area_group(self, instance):
        return {
            'code': instance.mission_area_group,
            'name': instance.get_mission_area_group_display()
        }


class KeyProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyProgram
        fields = ('id', 'name')


class ProgramObjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramObjective
        fields = ('id', 'description')


class DpgSerializer(serializers.ModelSerializer):
    mission_area = MissionAreaSerializer(many=False, required=True)
    program_objectives = ProgramObjectiveSerializer(many=True, required=False)

    class Meta:
        model = Dpg
        fields = ('id', 'mission_area', 'description', 'program_objectives')


class PbdgObjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = PbdgObjective
        fields = ('id', 'description')


class StrategicObjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrategicObjective
        fields = ('id', 'description', )


class StrategicProgramSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()

    class Meta:
        model = StrategicProgram
        fields = ('id', 'description')

    def get_description(self, instance):
        return f'{instance.code}: {instance.description}'


class KmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kma
        fields = ('id', 'code', 'name', )


class MajorPapSerializer(serializers.ModelSerializer):
    kma = KmaSerializer(many=False, required=True)

    class Meta:
        model = MajorPap
        fields = ('id', 'name', 'kma', 'fixed_cost', )


class SubPapSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubPap
        fields = ('id', 'name', )


class SuggestedPapSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuggestedPap
        fields = ('id', 'name',)


class PawafItemEndUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PawafItemEndUser
        fields = ('id', 'name',)


class PawafItemBudgetBreakdownSerializer(serializers.ModelSerializer):
    object_code = ObjectCodeSerializer()
    available_balance = serializers.SerializerMethodField()
    procurement_mode = ProcurementModeSerializer()

    class Meta:
        model = PawafItemBudgetBreakdown
        fields = ('id', 'object_code', 'amount_q1', 'amount_q2', 'amount_q3', 'amount_q4', 'amount',
                  'physical_target_q1', 'physical_target_q2', 'physical_target_q3', 'physical_target_q4',
                  'physical_target', 'available_balance', 'procurement_mode')

    def get_available_balance(self, instance):
        bal_q = ~Q(
            fund_release_item__fund_release__status__code=ppb_consts.RRF_CANCELLED)
        sums = (Sum('charged_q1', filter=bal_q) + Sum('charged_q2', filter=bal_q) +
                Sum('charged_q3', filter=bal_q) + Sum('charged_q4', filter=bal_q))
        charged = instance.release_sources.all().annotate(
            x=sums).aggregate(v=Sum('x'))['v'] or 0.0
        return round(instance.amount - charged, 2)


class PawafItemSerializer(serializers.ModelSerializer):
    major_pap = serializers.SerializerMethodField()
    sub_pap = serializers.SerializerMethodField()
    suggested_pap = SuggestedPapSerializer(required=True)
    expense_class = ExpenseClassSerializer(many=False, required=True)
    mission_area = MissionAreaSerializer(required=True)

    pbdg_objective = PbdgObjectiveSerializer(required=True)
    strategic_objective = serializers.SerializerMethodField()
    strategic_program = serializers.SerializerMethodField()
    key_program = KeyProgramSerializer()
    end_user = PawafItemEndUserSerializer()
    budget_breakdown = PawafItemBudgetBreakdownSerializer(many=True)
    available_balance = serializers.SerializerMethodField()

    class Meta:
        model = PawafItem
        fields = ('id', 'major_pap', 'sub_pap', 'suggested_pap', 'mission_area', 'is_mandatory', 'expense_class',
                  'pbdg_objective', 'strategic_objective', 'amount', 'physical_target',
                  'amount_q1', 'physical_target_q1', 'amount_q2', 'physical_target_q2', 'amount_q3',
                  'physical_target_q3', 'amount_q4', 'physical_target_q4', 'pawaf', 'specific_pap', 'strategic_program',
                  'branch', 'end_user', 'budget_breakdown', 'available_balance', 'key_program')

    def get_strategic_program(self, instance):
        return {
            'id': instance.strategic_program_id,
            'description': f'{instance.strategic_program.code}: {instance.strategic_program.description}',
        }

    def get_strategic_objective(self, instance):
        if instance.pbdg_objective_id:
            return {
                'id': instance.pbdg_objective.strategic_objective_id,
                'description': instance.pbdg_objective.strategic_objective.description
            }
        return None

    def get_major_pap(self, instance):
        return {
            'id': instance.suggested_pap.sub_pap.major_pap_id,
            'name': instance.suggested_pap.sub_pap.major_pap.name
        }

    def get_sub_pap(self, instance):
        return {
            'id': instance.suggested_pap.sub_pap_id,
            'name': instance.suggested_pap.sub_pap.name
        }

    def get_available_balance(self, instance):
        bal_q = ~Q(
            release_sources__fund_release_item__fund_release__status__code=ppb_consts.RRF_CANCELLED)
        sums = (Sum('release_sources__charged_q1', filter=bal_q) + Sum('release_sources__charged_q2', filter=bal_q) +
                Sum('release_sources__charged_q3', filter=bal_q) + Sum('release_sources__charged_q4', filter=bal_q))
        charged = instance.budget_breakdown.all().annotate(
            x=sums).aggregate(v=Sum('x'))['v'] or 0.0
        return round(instance.amount - charged, 2)


class PawafSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()
    full_description = serializers.SerializerMethodField()
    available_balance = serializers.SerializerMethodField()

    class Meta:
        model = Pawaf
        fields = ('id', 'year', 'ceiling', 'description', 'amount', 'full_description', 'available_balance')

    def get_full_description(self, instance):
        return f'{instance.year} - {instance.description}'

    def get_amount(self, instance):
        user = self.context['request'].user
        account = user.account.account_dict()
        if account['organization'] == consts.PPB:
            return round(instance.pawaf_items.aggregate(t=Sum('amount'))['t'] or 0.0, 2)
        return round(instance.pawaf_items.filter(branch__iexact=account['organization']).aggregate(t=Sum('amount'))['t'] or 0.0, 2)

    def get_available_balance(self, instance):
        user = self.context['request'].user
        account = user.account.account_dict()

        bal_q = ~Q(
            budget_breakdown__release_sources__fund_release_item__fund_release__status__code=ppb_consts.RRF_CANCELLED)
        sums = (Sum('budget_breakdown__release_sources__charged_q1', filter=bal_q) +
                Sum('budget_breakdown__release_sources__charged_q2', filter=bal_q) +
                Sum('budget_breakdown__release_sources__charged_q3', filter=bal_q) +
                Sum('budget_breakdown__release_sources__charged_q4', filter=bal_q))

        if account['organization'] == consts.PPB:
            total = round(instance.pawaf_items.aggregate(t=Sum('amount'))['t'] or 0.0, 2)
            charged = instance.pawaf_items.all().aggregate(total=sums)

            return round(total - (charged['total'] or 0.0), 2)

        total = round(instance.pawaf_items.filter(branch__iexact=account['organization']).
                      aggregate(t=Sum('amount'))['t'] or 0.0, 2)
        charged = instance.pawaf_items.filter(branch__iexact=account['organization']).aggregate(
            total=sums)

        return round(total - (charged['total'] or 0.0), 2)


class PawafItemCUSerializer(serializers.ModelSerializer):
    pawaf = serializers.PrimaryKeyRelatedField(queryset=Pawaf.objects.all(), required=False)
    breakdown = serializers.DictField(write_only=True)

    class Meta:
        model = PawafItem
        fields = ('id', 'suggested_pap', 'mission_area',
                  'is_mandatory', 'notes', 'pbdg_objective', 'specific_pap', 'strategic_program', 'branch',
                  'amount_q1', 'amount_q2', 'amount_q3', 'amount_q4', 'physical_target_q1', 'physical_target_q2',
                  'physical_target_q3', 'physical_target_q4', 'end_user', 'pawaf', 'breakdown', 'expense_class',
                  'key_program')

    def update_budget_breakdowns(self, instance, breakdown_items):
        if instance.budget_breakdown.filter(pk__in=[o['id'] for o in breakdown_items]).count() != len(breakdown_items):
            raise serializers.ValidationError(
                {'breakdown': 'Some budget breakdown items do not belong to this pawaf item'})
        for breakdown in breakdown_items:
            pk = breakdown.pop('id')
            breakdown_item = PawafItemBudgetBreakdown.objects.filter(
                pk=pk
            )
            breakdown_item.update(**breakdown)
            breakdown_item[0].save()

    def delete_budget_breakdowns(self, instance, breakdown_items):
        if instance.budget_breakdown.filter(pk__in=[o['id'] for o in breakdown_items]).count() == len(breakdown_items):
            instance.budget_breakdown.filter(pk__in=[o['id'] for o in breakdown_items]).delete()
        else:
            raise serializers.ValidationError(
                {'breakdown': 'Some budget breakdown items do not belong to this pawaf item'})

    def create_budget_breakdowns(self, instance, breakdown_items):
        for breakdown in breakdown_items:
            serialized_obj = PawafItemBudgetBreakdownCUSerializer(
                data={**breakdown, 'pawaf_item': instance.id})
            serialized_obj.is_valid(raise_exception=True)
            _ = serialized_obj.save()

    def create(self, validated_data):
        budget_breakdown = validated_data.pop('breakdown', None) or {}
        instance = super().create(validated_data)
        self.create_budget_breakdowns(instance, budget_breakdown.get('to_add') or [])
        instance.save()
        return instance

    def update(self, instance, validated_data):
        budget_breakdown = validated_data.pop('breakdown', None) or {}
        self.delete_budget_breakdowns(instance, budget_breakdown.get('to_delete') or [])
        self.update_budget_breakdowns(instance, budget_breakdown.get('to_update') or [])
        self.create_budget_breakdowns(instance, budget_breakdown.get('to_add') or [])
        return super().update(instance, validated_data)


class PawafItemBudgetBreakdownCUSerializer(serializers.ModelSerializer):
    class Meta:
        model = PawafItemBudgetBreakdown
        fields = ('id', 'object_code', 'amount_q1', 'amount_q2', 'amount_q3', 'amount_q4', 'amount',
                  'physical_target_q1', 'physical_target_q2', 'physical_target_q3', 'physical_target_q4',
                  'physical_target', 'pawaf_item', 'procurement_mode')


class PawafCUSerializer(serializers.ModelSerializer):
    pawaf_items = PawafItemCUSerializer(many=True, required=False)

    class Meta:
        model = Pawaf
        fields = ('id', 'year', 'ceiling', 'description', 'pawaf_items')

    def create(self, validated_data):
        items = validated_data.pop('pawaf_items', None) or []
        instance = super().create(validated_data)

        for item in items:
            serialized_obj = PawafItemCUSerializer(
                data={
                    **item,
                    'suggested_pap': item['suggested_pap'].id,
                    'mission_area': item['mission_area'].id,
                    'object_code': item['object_code'].id,
                    'pbdg_objective': item['pbdg_objective'].id,
                    'strategic_program': item['strategic_program'].id,
                    'strategic_objective': item['strategic_objective'].id,
                    'pawaf': instance.id
                }
            )
            serialized_obj.is_valid(raise_exception=True)
            _ = serialized_obj.save()
        return instance

    def update(self, instance, validated_data):
        to_delete = self.context['pawaf_items']['to_delete']
        to_update = self.context['pawaf_items']['to_update']

        if to_delete:
            if instance.pawaf_items.filter(pk__in=to_delete).count() == len(to_delete):
                instance.pawaf_items.filter(pk__in=to_delete).delete()
            else:
                raise serializers.ValidationError(
                    {'pawaf_items': 'Some pawaf items do not belong to this pawaf'})

        if to_update:
            if instance.pawaf_items.filter(pk__in=[o['id'] for o in to_update]).count() != len(to_update):
                raise serializers.ValidationError(
                    {'pawaf_items': 'Some pawaf items do not belong to this pawaf'})
            for item in to_update:
                pk = item.pop('id')
                pawaf_item = PawafItem.objects.get(pk=pk)
                serialized_obj = PawafItemCUSerializer(instance=pawaf_item, data=item)
                serialized_obj.is_valid(raise_exception=True)
                _ = serialized_obj.save()

        to_add = validated_data.pop('pawaf_items', None) or []

        for item in to_add:
            serialized_obj = PawafItemCUSerializer(
                data={
                    **item,
                    'suggested_pap': item['suggested_pap'].id,
                    'mission_area': item['mission_area'].id,
                    'object_code': item['object_code'].id,
                    'pbdg_objective': item['pbdg_objective'].id,
                    'pawaf': instance.id
                }
            )
            serialized_obj.is_valid(raise_exception=True)
            _ = serialized_obj.save()

        return super().update(instance, validated_data)


class PawafItemViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PawafItemView
        fields = ('id', 'description', 'header_label')


class PawafItemBudgetBreakdownForRrfSelectionSerializer(serializers.ModelSerializer):
    object_code = serializers.ReadOnlyField(source='object_code.code')
    specific_pap = serializers.ReadOnlyField(source='pawaf_item.specific_pap')
    available_balance = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    q1_available_balance = serializers.SerializerMethodField()
    q2_available_balance = serializers.SerializerMethodField()
    q3_available_balance = serializers.SerializerMethodField()
    q4_available_balance = serializers.SerializerMethodField()

    class Meta:
        model = PawafItemBudgetBreakdown
        fields = ('id', 'object_code', 'specific_pap', 'amount', 'amount_q1', 'amount_q2', 'amount_q3', 'amount_q4',
                  'available_balance', 'name', 'q1_available_balance', 'q2_available_balance', 'q3_available_balance',
                  'q4_available_balance')

    def get_name(self, instance):
        proc = instance.procurement_mode.name if instance.procurement_mode else 'None'
        return f'{instance.pawaf_item.specific_pap} / {instance.object_code.code} / {proc}'

    def get_q1_available_balance(self, instance):
        bal_q = ~Q(fund_release_item__fund_release__status__code=ppb_consts.RRF_CANCELLED)
        charged = instance.release_sources.all().annotate(
            x=Sum('charged_q1', filter=bal_q)).aggregate(v=Sum('x'))['v'] or 0.0
        return round(instance.amount_q1 - charged, 2)

    def get_q2_available_balance(self, instance):
        bal_q = ~Q(fund_release_item__fund_release__status__code=ppb_consts.RRF_CANCELLED)
        charged = instance.release_sources.all().annotate(
            x=Sum('charged_q2', filter=bal_q)).aggregate(v=Sum('x'))['v'] or 0.0
        return round(instance.amount_q2 - charged, 2)

    def get_q3_available_balance(self, instance):
        bal_q = ~Q(fund_release_item__fund_release__status__code=ppb_consts.RRF_CANCELLED)
        charged = instance.release_sources.all().annotate(
            x=Sum('charged_q3', filter=bal_q)).aggregate(v=Sum('x'))['v'] or 0.0
        return round(instance.amount_q3 - charged, 2)

    def get_q4_available_balance(self, instance):
        bal_q = ~Q(fund_release_item__fund_release__status__code=ppb_consts.RRF_CANCELLED)
        charged = instance.release_sources.all().annotate(
            x=Sum('charged_q4', filter=bal_q)).aggregate(v=Sum('x'))['v'] or 0.0
        return round(instance.amount_q4 - charged, 2)

    def get_available_balance(self, instance):
        bal_q = ~Q(fund_release_item__fund_release__status__code=ppb_consts.RRF_CANCELLED)
        sums = (Sum('charged_q1', filter=bal_q) + Sum('charged_q2', filter=bal_q) +
                Sum('charged_q3', filter=bal_q) + Sum('charged_q4', filter=bal_q))
        charged = instance.release_sources.all().annotate(
            x=sums).aggregate(v=Sum('x'))['v'] or 0.0
        return round(instance.amount - charged, 2)


class FundReleaseSourceRetrieveSerializer(serializers.ModelSerializer):
    fund_source = PawafItemBudgetBreakdownForRrfSelectionSerializer()

    class Meta:
        # FIXME remove charged_amount upon correction of records
        model = FundReleaseSource
        fields = ('id', 'fund_source', 'charged_amount', 'charged_q1', 'charged_q2', 'charged_q3', 'charged_q4')


class FundReleaseRecipientRetrieveSerializer(serializers.ModelSerializer):
    servicing_mfo = PamuSerializer()
    unit = UnitSerializer()

    class Meta:
        model = FundReleaseRecipient
        fields = ('id', 'servicing_mfo', 'unit', 'amount')


class FundReleaseItemListSerializer(serializers.ModelSerializer):
    rrf_no = serializers.ReadOnlyField(source='fund_release.rrf_no')
    object_code = serializers.ReadOnlyField(source='object_code.code')
    program = serializers.ReadOnlyField(source='get_program_display')
    mission_area = serializers.ReadOnlyField(source='mission_area.mission_area_group')
    name = serializers.SerializerMethodField()

    class Meta:
        model = FundReleaseItem
        fields = ('id', 'rrf_no', 'object_code', 'program', 'mission_area', 'specific_purpose',
                  'amount', 'balance', 'released', 'name')

    def get_name(self, instance):
        return f'{instance.specific_purpose} / {instance.object_code.code}'


class FundReleaseItemRetrieveSerializer(serializers.ModelSerializer):
    release_recipients = FundReleaseRecipientRetrieveSerializer(many=True)
    release_sources = FundReleaseSourceRetrieveSerializer(many=True)
    object_code = serializers.SerializerMethodField()
    program = serializers.SerializerMethodField()
    mission_area = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = FundReleaseItem
        fields = ('id', 'release_recipients', 'release_sources', 'object_code', 'program', 'mission_area',
                  'specific_purpose', 'q1', 'q2', 'q3', 'q4', 'amount', 'chargeability', 'realignment_level1',
                  'realignment_level2', 'balance', 'released', 'name')

    def get_name(self, instance):
        return f'{instance.specific_purpose} / {instance.object_code.code}'

    def get_object_code(self, instance):
        return {
            'id': instance.object_code_id,
            'code': instance.object_code.code
        }

    def get_program(self, instance):
        return {
            'code': instance.program,
            'display': instance.get_program_display()
        }

    def get_mission_area(self, instance):
        return {
            'id': instance.mission_area_id,
            'name': instance.mission_area.mission_area_group
        }


class FundReleaseListSerializer(serializers.ModelSerializer):
    budget = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = FundRelease
        fields = ('id', 'year', 'rrf_no', 'budget', 'amount', 'released', 'balance', 'status')

    def get_budget(self, instance):
        if instance.budget_id:
            return f'{instance.budget.description}'
        return instance.other_budget

    def get_status(self, instance):
        if instance.status_id:
            return instance.status.name
        return 'Unknown'


class FundReleaseRetrieveSerializer(serializers.ModelSerializer):
    budget = serializers.SerializerMethodField()
    specific_paps = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    status = StatusSerializer()
    audit = serializers.SerializerMethodField()

    class Meta:
        model = FundRelease
        fields = ('id', 'date', 'rrf_no', 'reference', 'footer_control', 'budget', 'specific_paps', 'amount',
                  'serial', 'other_budget', 'cmd', 'author', 'status', 'released', 'balance', 'audit')

    def get_author(self, instance):
        return instance.created_by.account.name

    def get_audit(self, instance):
        return {
            'created_by': instance.created_by.account.name,
            'created_at': instance.created_at,
            'updated_by': instance.updated_by.account.name,
            'updated_at': instance.updated_at
        }

    def get_specific_paps(self, instance):
        items = []
        for pap in instance.specific_paps.all():  # PawafItem
            items.append({
                'id': pap.id,
                'specific_pap': pap.specific_pap
            })
        return items

    def get_budget(self, instance):
        if instance.budget_id:
            return {
                'id': instance.budget_id,
                'description': instance.budget.description
            }


class FundReleaseCUSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundRelease
        fields = ('id', 'date', 'serial', 'rrf_no', 'reference', 'footer_control', 'budget', 'specific_paps',
                  'other_budget', 'cmd', 'status')

    def calculate_recipients_chargeability_dist(self, instance):
        if instance.status.code == ppb_consts.RRF_CANCELLED:
            for item in instance.release_items.all():
                for source in item.release_sources:
                    budget_item = source.fund_source.pawaf_item
                    budget_item.chargeability_distribution = None
                    budget_item.save()
                return

    def validate(self, attrs):
        if attrs.get('budget') and not attrs.get('specific_paps'):
            raise serializers.ValidationError({'specific_paps': 'Must not be empty'})
        return attrs

    def create(self, validated_data):
        year = validated_data['date'].year
        serial = validated_data['serial']
        validated_data['rrf_no'] = f'OG4-{year}-{serial:03}'
        specific_paps = validated_data.pop('specific_paps', []) or []

        if validated_data.get('budget'):
            validated_data['other_budget'] = None
        else:
            specific_paps = []

        instance = super().create(validated_data)

        for specific_pap in specific_paps:
            _ = instance.specific_paps.add(specific_pap)

        self.calculate_recipients_chargeability_dist(instance)

        return instance

    def update(self, instance, validated_data):
        specific_paps = validated_data.pop('specific_paps', []) or []

        year = (validated_data.get('date') or instance.date).year
        serial = validated_data['serial']
        validated_data['rrf_no'] = f'OG4-{year}-{serial:03}'

        if validated_data.get('budget'):
            validated_data['other_budget'] = None
        else:
            specific_paps = []

        instance = super().update(instance, validated_data)

        instance.specific_paps.clear()
        if specific_paps:
            instance.specific_paps.set(specific_paps)

        self.calculate_recipients_chargeability_dist(instance)

        return instance


class FundReleaseRecipientCUSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundReleaseRecipient
        fields = ('id', 'servicing_mfo', 'unit', 'amount', 'fund_release_item')


class FundReleaseSourceCUSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundReleaseSource
        fields = ('id', 'fund_source', 'fund_release_item',
                  'charged_q1', 'charged_q2', 'charged_q3', 'charged_q4')


class FundReleaseItemCUSerializer(serializers.ModelSerializer):
    fund_release = serializers.PrimaryKeyRelatedField(queryset=FundRelease.objects.all(), required=False)
    recipients = serializers.DictField(write_only=True)
    sources = serializers.DictField(write_only=True)

    class Meta:
        model = FundReleaseItem
        fields = ('id', 'recipients', 'sources', 'fund_release', 'object_code', 'program', 'mission_area',
                  'specific_purpose', 'q1', 'q2', 'q3', 'q4')

    def calculate_recipients_chargeability_dist(self, instance):
        qs = ['q1', 'q2', 'q3', 'q4']
        if instance.fund_release.status_id and instance.fund_release.status.code == ppb_consts.RRF_CANCELLED:
            for source in instance.release_sources:
                budget_item = source.fund_source.pawaf_item
                budget_item.chargeability_distribution = None
                budget_item.save()
            return
        max_limit = 100  # Max per recipient
        rrf = instance.fund_release_id
        activity_charged = {}
        release_sources = instance.release_sources.distinct().order_by('id')
        release_recipients = instance.release_recipients. \
            values('servicing_mfo'). \
            annotate(total=Sum('amount')). \
            values('total', mfo=F('servicing_mfo_id')).order_by('mfo')
        fund_balances = {}
        for release_source in release_sources:
            fund_balances[release_source.id] = {'q1': release_source.charged_q1,
                                                'q2': release_source.charged_q2,
                                                'q3': release_source.charged_q3,
                                                'q4': release_source.charged_q4,
                                                'pawaf_item': release_source.fund_source.pawaf_item
                                                }
        recipient_balances = {}
        for release_recipient in release_recipients:
            mfo = release_recipient['mfo']
            if mfo not in recipient_balances:
                recipient_balances[mfo] = round(release_recipient['total'] or 0., 2)
            iterations = 0
            while recipient_balances[mfo] > 0 and iterations < max_limit:
                iterations += 1
                for release_source, values in fund_balances.items():
                    if not recipient_balances[mfo]:
                        break
                    budget_item = values['pawaf_item']
                    if budget_item not in activity_charged:
                        activity_charged[budget_item] = {}
                    if rrf not in activity_charged[budget_item]:
                        activity_charged[budget_item][rrf] = {}
                    if instance.id not in activity_charged[budget_item][rrf]:
                        activity_charged[budget_item][rrf][instance.id] = {}
                    if mfo not in activity_charged[budget_item][rrf][instance.id]:
                        activity_charged[budget_item][rrf][instance.id][mfo] = {
                            'q1': 0.0, 'q2': 0.0, 'q3': 0.0, 'q4': 0.0}
                    for quarter in qs:
                        if recipient_balances[mfo] == 0.:
                            break
                        if values[quarter]:
                            to_charge = min(values[quarter], recipient_balances[mfo])
                            values[quarter] -= round(to_charge, 2)
                            values[quarter] = round(values[quarter], 2)
                            recipient_balances[mfo] -= round(to_charge, 2)
                            activity_charged[budget_item][rrf][instance.id][mfo][quarter] += to_charge
        for budget_item, rrfs in activity_charged.items():
            dist = budget_item.chargeability_distribution
            if not dist:
                dist = rrfs
            else:
                for rrf, items in rrfs.items():
                    rrf_s = f'{rrf}'
                    if rrf_s not in dist:
                        dist[rrf_s] = items
                    else:
                        for item, mfos in items.items():
                            dist[rrf_s][f'{item}'] = mfos
            budget_item.chargeability_distribution = dist
            budget_item.save()

    def update_release_recipients(self, instance, release_recipients):
        count = instance.release_recipients.filter(pk__in=[o['id'] for o in release_recipients]).count()
        if count != len(release_recipients):
            raise serializers.ValidationError(
                {'release_recipients': 'Some release recipients do not belong to this fund release'})
        for release_recipient in release_recipients:
            pk = release_recipient.pop('id')
            recipient_obj = FundReleaseRecipient.objects.filter(pk=pk)
            recipient_obj.update(**release_recipient)

    def delete_release_recipients(self, instance, release_recipients):
        count = instance.release_recipients.filter(pk__in=[o['id'] for o in release_recipients]).count()
        if count == len(release_recipients):
            instance.release_recipients.filter(pk__in=[o['id'] for o in release_recipients]).delete()
        else:
            raise serializers.ValidationError(
                {'release_recipients': 'Some release recipients do not belong to this fund release'})

    def create_release_recipients(self, instance, recipients):
        for recipient in recipients:
            serialized_obj = FundReleaseRecipientCUSerializer(
                data={**recipient, 'fund_release_item': instance.id})
            serialized_obj.is_valid(raise_exception=True)
            _ = serialized_obj.save()

    def update_release_source(self, instance, sources):
        count = instance.release_sources.filter(pk__in=[o['id'] for o in sources]).count()
        if count != len(sources):
            raise serializers.ValidationError(
                {'release_recipients': 'Some release recipients do not belong to this fund release'})
        for release_source in sources:
            pk = release_source.pop('id')
            source_obj = FundReleaseSource.objects.filter(pk=pk)
            source_obj.update(**release_source)

    def delete_release_source(self, instance, sources):
        count = instance.release_sources.filter(pk__in=[o['id'] for o in sources]).count()
        if count == len(sources):
            instance.release_sources.filter(pk__in=[o['id'] for o in sources]).delete()
        else:
            raise serializers.ValidationError(
                {'release_recipients': 'Some release sources do not belong to this fund release'})

    def create_release_source(self, instance, sources):
        for source in sources:
            serialized_obj = FundReleaseSourceCUSerializer(data={**source, 'fund_release_item': instance.id})
            serialized_obj.is_valid(raise_exception=True)
            _ = serialized_obj.save()

    def check_if_balance(self, instance):
        total_charged = round(instance.release_sources.aggregate(
            x=Sum('charged_q1') + Sum('charged_q2') + Sum('charged_q3') + Sum('charged_q4'))['x'] or 0, 2)
        return instance.amount != total_charged

    def infer_realignment(self, instance):
        if not instance.fund_release.budget_id:
            instance.realignment_level1 = True
            instance.realignment_level2 = False
            instance.save()
            return

        if not instance.fund_release.specific_paps.filter(
                budget_breakdown__object_code_id=instance.object_code_id).exists():
            instance.realignment_level1 = True
        elif not instance.fund_release.specific_paps.filter(
                mission_area_id=instance.mission_area_id).exists():
            instance.realignment_level1 = True
        elif not instance.fund_release.specific_paps.filter(
                suggested_pap__sub_pap__major_pap__pa_sub_program=instance.program).exists():
            instance.realignment_level1 = True
        else:
            instance.realignment_level1 = False

        sources = instance.release_sources.values_list('fund_source', flat=True)
        instance.realignment_level2 = not instance.fund_release.specific_paps.filter(
            budget_breakdown__in=sources).exists()

        instance.save()

    def create(self, validated_data):
        recipients = validated_data.pop('recipients', None) or {}
        sources = validated_data.pop('sources', None) or {}

        with transaction.atomic():
            instance = super().create(validated_data)

            self.create_release_recipients(instance, recipients.get('to_add') or [])
            self.create_release_source(instance, sources.get('to_add') or [])

            if instance.fund_release.budget_id:
                if self.check_if_balance(instance):
                    raise serializers.ValidationError('Amount charged is not equal to the amount released.')
            self.infer_realignment(instance)
            self.calculate_recipients_chargeability_dist(instance)

            return instance

    def update(self, instance, validated_data):
        recipients = validated_data.pop('recipients', None) or {}
        sources = validated_data.pop('sources', None) or {}

        with transaction.atomic():
            self.delete_release_recipients(instance, recipients.get('to_delete') or [])
            self.update_release_recipients(instance, recipients.get('to_update') or [])
            self.create_release_recipients(instance, recipients.get('to_add') or [])

            self.delete_release_source(instance, sources.get('to_delete') or [])
            self.update_release_source(instance, sources.get('to_update') or [])
            self.create_release_source(instance, sources.get('to_add') or [])

            instance = super().update(instance, validated_data)

            if instance.fund_release.budget_id:
                if self.check_if_balance(instance):
                    raise serializers.ValidationError('Amount charged is not equal to the amount released.')
            self.infer_realignment(instance)
            self.calculate_recipients_chargeability_dist(instance)

            return instance


class FundReleaseAsaItemRetrieveSerializer(serializers.ModelSerializer):
    release_item = FundReleaseItemListSerializer()

    class Meta:
        model = FundReleaseAsaItem
        fields = ('id', 'release_item', 'amount')


class FundReleaseAsaListSerializer(serializers.ModelSerializer):
    unit = serializers.ReadOnlyField(source='unit.name')
    servicing_mfo = serializers.ReadOnlyField(source='servicing_mfo.name')

    class Meta:
        model = FundReleaseAsa
        fields = ('id', 'advice_no', 'date_released', 'servicing_mfo', 'unit', 'amount', 'purpose', 'is_withdrawal')


class FundReleaseAsaRetrieveSerializer(serializers.ModelSerializer):
    unit = UnitSerializer()
    servicing_mfo = PamuSerializer()
    asa_items = FundReleaseAsaItemRetrieveSerializer(many=True)
    fund_releases = serializers.SerializerMethodField()

    class Meta:
        model = FundReleaseAsa
        fields = ('id', 'advice_no', 'date_released', 'servicing_mfo', 'unit', 'amount', 'purpose',
                  'is_withdrawal', 'fund_releases', 'asa_items')

    def get_fund_releases(self, instance):
        ret = []
        for item in instance.fund_releases.all():
            ret.append({'id': item.id,
                        'rrf_no': item.rrf_no,
                        'amount': item.amount,
                        'released': item.released,
                        'balance': item.balance})
        return ret


class FundReleaseAsaItemCUSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundReleaseAsaItem
        fields = ('id', 'asa', 'release_item', 'amount')


class FundReleaseAsaCUSerializer(serializers.ModelSerializer):
    asa_items = serializers.DictField(write_only=True)

    class Meta:
        model = FundReleaseAsa
        fields = ('id', 'advice_no', 'date_released', 'servicing_mfo', 'unit', 'purpose',
                  'is_withdrawal', 'fund_releases', 'asa_items')

    def update_asa_items(self, instance, items):
        count = instance.asa_items.filter(pk__in=[o['id'] for o in items]).count()
        if count != len(items):
            raise serializers.ValidationError(
                {'asa_items': 'Some ASA items do not belong to this ASA'})
        for item in items:
            pk = item.pop('id')
            obj = FundReleaseAsaItem.objects.filter(pk=pk)
            obj.update(**item)

    def delete_asa_items(self, instance, items):
        count = instance.asa_items.filter(pk__in=[o['id'] for o in items]).count()
        if count == len(items):
            instance.asa_items.filter(pk__in=[o['id'] for o in items]).delete()
        else:
            raise serializers.ValidationError(
                {'asa_items': 'Some ASA items do not belong to this ASA'})

    def create_asa_items(self, instance, items):
        for item in items:
            serialized_obj = FundReleaseAsaItemCUSerializer(
                data={**item, 'asa': instance.id})
            serialized_obj.is_valid(raise_exception=True)
            _ = serialized_obj.save()

    def create(self, validated_data):
        asa_items = validated_data.pop('asa_items', None) or {}
        fund_releases = validated_data.pop('fund_releases', []) or []

        with transaction.atomic():
            instance = super().create(validated_data)

            if fund_releases:
                instance.fund_releases.set(fund_releases)

            self.create_asa_items(instance, asa_items.get('to_add') or [])

            if not self.check_items_consistency(instance):
                raise serializers.ValidationError('Inconsistent ASA items.')

            return instance

    def check_items_consistency(self, instance):
        fund_releases = instance.fund_releases.all()
        return not instance.asa_items.exclude(release_item__fund_release_id__in=fund_releases).exists()

    def update(self, instance, validated_data):
        asa_items = validated_data.pop('asa_items', None) or {}
        fund_releases = validated_data.pop('fund_releases', []) or []

        with transaction.atomic():
            self.delete_asa_items(instance, asa_items.get('to_delete') or [])
            self.update_asa_items(instance, asa_items.get('to_update') or [])
            self.create_asa_items(instance, asa_items.get('to_add') or [])

            instance.fund_releases.clear()
            if fund_releases:
                instance.fund_releases.set(fund_releases)

            if not self.check_items_consistency(instance):
                raise serializers.ValidationError('Inconsistent ASA items.')

            instance = super().update(instance, validated_data)

            return instance

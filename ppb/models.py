import datetime
import random
import string

from django.db import models
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

from commons.models import Unit, ProcurementMode, Pamu
from ppb import consts
import utils


class ExpenseClass(models.Model):
    code = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=64)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Expense classes'

    def __str__(self):
        return self.name


class ObjectCode(models.Model):
    code = models.CharField(max_length=20)
    description = models.CharField(max_length=255)
    name = models.CharField(max_length=255, null=True)
    expense_class = models.ForeignKey(ExpenseClass, models.DO_NOTHING, related_name='object_codes')

    def __str__(self):
        return self.description


class MissionArea(models.Model):
    MISSION_AREA_GROUP_CHOICES = (
        ('EDM', 'External Defense Mission'),
        ('IDM', 'Internal Defense Mission')
    )
    mission_area_group = models.CharField(max_length=4, choices=MISSION_AREA_GROUP_CHOICES)
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=8)

    @property
    def mission_code(self):
        return self.mission_area_group

    def __str__(self):
        return self.name


class Dpg(models.Model):
    mission_area = models.ForeignKey(MissionArea, models.DO_NOTHING, related_name='+')
    description = models.TextField()
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'DPG'

    def __str__(self):
        return self.description


class ProgramObjective(models.Model):
    dpg = models.ForeignKey(Dpg, models.DO_NOTHING, related_name='program_objectives')
    description = models.TextField()

    def __str__(self):
        return self.description


class Kma(models.Model):
    name = models.CharField(max_length=32)
    code = models.CharField(max_length=8)

    class Meta:
        verbose_name = 'KMA'

    def __str__(self):
        return self.name


class MajorPap(models.Model):
    PROGRAM_CHOICES = (
        ('OPS', 'OPERATIONS'),
        ('GAS', 'GAS'),
    )
    PA_PROGRAM_CHOICES = (
        ('LFP', 'Land Forces Program'),
        ('GAS', 'General Administration & Support'),
    )
    PA_SUB_PROGRAM_CHOICES = (
        ('FS', 'Force Sustainment'),
        ('FD', 'Force Development'),
        ('FLSS', 'Force Level Support Services'),
        ('GAS', 'General Administration & Support'),
    )
    PA_FUNCTION_CHOICES = (
        ('DEV', 'Develop'),
        ('ORG', 'Organize'),
        ('TRN', 'Train'),
        ('EQP', 'Equip'),
        ('SUP', 'Support Service'),
        ('SUS', 'Sustain'),
        ('GMS', 'General Management & Supervision'),
    )

    name = models.CharField(max_length=128)
    expenditure_program = models.CharField(max_length=8, choices=PROGRAM_CHOICES)
    pa_program = models.CharField('PA Program (1L)', max_length=8, choices=PA_PROGRAM_CHOICES)
    pa_sub_program = models.CharField('PA Sub-program (2L)', max_length=8, choices=PA_SUB_PROGRAM_CHOICES)
    pa_function = models.CharField('PA Function (3L)', max_length=8, choices=PA_FUNCTION_CHOICES)
    kma = models.ForeignKey(Kma, models.DO_NOTHING, related_name='+')
    fixed_cost = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'PAP - 4L Major'
        verbose_name_plural = 'PAP - 4L Major'

    def description(self):
        if self.name.startswith('MP'):
            return self.name.split(' ', 1)[1]
        return self.name

    @property
    def program(self):
        return self.pa_sub_program

    def __str__(self):
        return self.name


class SubPap(models.Model):
    major_pap = models.ForeignKey(MajorPap, models.DO_NOTHING)
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name = 'PAP - 5L Sub'
        verbose_name_plural = 'PAP - 5L Sub'

    def description(self):
        if self.name.startswith('SP'):
            return self.name.split(' ', 1)[1]
        return self.name

    def __str__(self):
        return self.name


class SuggestedPap(models.Model):
    sub_pap = models.ForeignKey(SubPap, models.DO_NOTHING)
    name = models.CharField(max_length=128)

    def major_pap_description(self):
        return self.sub_pap.major_pap.name.split(' ', 1)[1]

    def description(self):
        if self.name.startswith('SP'):
            return self.name.split(' ', 1)[1]
        return self.name

    class Meta:
        verbose_name = 'PAP - 6L Suggested'
        verbose_name_plural = 'PAP - 6L Suggested'

    def __str__(self):
        return self.name


class StrategicProgram(models.Model):
    description = models.TextField()
    code = models.CharField(max_length=8)

    def __str__(self):
        return self.code


class StrategicObjective(models.Model):
    description = models.TextField()

    def __str__(self):
        return self.description


class PbdgObjective(models.Model):
    strategic_objective = models.ForeignKey(StrategicObjective, models.CASCADE, related_name='pbdg_objectives')
    description = models.TextField()

    class Meta:
        verbose_name = 'PBDG objective'

    def __str__(self):
        return self.description


class PawafItemEndUser(models.Model):
    name = models.CharField(max_length=32)
    servicing_mfo = models.ForeignKey(Pamu, models.DO_NOTHING, null=True, blank=True, related_name='+')

    def __str__(self):
        return self.name


class FundSource(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class KeyProgram(models.Model):
    code = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=256)
    order = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.name


class Pawaf(models.Model):
    year = models.PositiveIntegerField()
    ceiling = models.FloatField()
    description = models.TextField()

    class Meta:
        verbose_name = 'Budget Record'

    def __str__(self):
        return f'Budget Record {self.year} - {self.description}'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.ceiling = round(self.ceiling, 2)
        super().save(force_insert, force_update, using, update_fields)


class PawafItem(models.Model):
    pawaf = models.ForeignKey(Pawaf, models.CASCADE, related_name='pawaf_items')
    suggested_pap = models.ForeignKey(SuggestedPap, models.DO_NOTHING, related_name='+')
    specific_pap = models.CharField(max_length=256)
    end_user = models.ForeignKey(PawafItemEndUser, models.DO_NOTHING, related_name='+')
    branch = models.CharField(max_length=8)
    mission_area = models.ForeignKey(MissionArea, models.DO_NOTHING, related_name='+')
    is_mandatory = models.BooleanField(default=False)
    expense_class = models.ForeignKey(ExpenseClass, models.DO_NOTHING, related_name='+')

    key_program = models.ForeignKey(KeyProgram, models.DO_NOTHING, related_name='+', null=True)
    strategic_program = models.ForeignKey(StrategicProgram, models.DO_NOTHING, related_name='+')
    program_objective = models.ForeignKey(ProgramObjective, models.DO_NOTHING, related_name='pawaf_items', null=True,
                                          blank=True)
    pbdg_objective = models.ForeignKey(PbdgObjective, models.DO_NOTHING, related_name='+')
    notes = models.TextField(null=True, blank=True)

    amount_q1 = models.FloatField(default=0.0)
    amount_q2 = models.FloatField(default=0.0)
    amount_q3 = models.FloatField(default=0.0)
    amount_q4 = models.FloatField(default=0.0)
    amount = models.FloatField(default=0.0)
    physical_target_q1 = models.PositiveIntegerField(default=0)
    physical_target_q2 = models.PositiveIntegerField(default=0)
    physical_target_q3 = models.PositiveIntegerField(default=0)
    physical_target_q4 = models.PositiveIntegerField(default=0)
    physical_target = models.PositiveIntegerField(default=0)

    chargeability_distribution = JSONField(null=True, blank=True)

    @property
    def parsed_distribution(self):
        if self.chargeability_distribution is None:
            return None
        dist = {}
        for rrf_id, rrf_item_ids in self.chargeability_distribution.items():
            rrf = FundRelease.objects.get(pk=rrf_id)
            dist[rrf] = {}
            for rrf_item_id, mfo_ids in rrf_item_ids.items():
                rrf_item = rrf.release_items.get(pk=rrf_item_id)
                dist[rrf][rrf_item] = {}

                for mfo_id, quarters in mfo_ids.items():
                    mfo = Pamu.objects.get(pk=mfo_id)
                    dist[rrf][rrf_item][mfo] = quarters
        return dist

    @property
    def charged_q1(self):
        charged = self.budget_breakdown.aggregate(
            x=models.Sum('release_sources__charged_q1'))['x'] or 0.0

        return round(charged, 2)

    @property
    def charged_q2(self):
        charged = self.budget_breakdown.aggregate(
            x=models.Sum('release_sources__charged_q2'))['x'] or 0.0

        return round(charged, 2)

    @property
    def charged_q3(self):
        charged = self.budget_breakdown.aggregate(
            x=models.Sum('release_sources__charged_q3'))['x'] or 0.0

        return round(charged, 2)

    @property
    def charged_q4(self):
        charged = self.budget_breakdown.aggregate(
            x=models.Sum('release_sources__charged_q4'))['x'] or 0.0

        return round(charged, 2)

    @property
    def charged_amount(self):
        charged = self.budget_breakdown.aggregate(
            x=(models.Sum('release_sources__charged_q1') + models.Sum('release_sources__charged_q2') +
               models.Sum('release_sources__charged_q3') + models.Sum('release_sources__charged_q4')))['x'] or 0.0

        return round(charged, 2)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        fs_total = self.budget_breakdown.aggregate(amount_q1=models.Sum('amount_q1'), amount_q2=models.Sum('amount_q2'),
                                                   amount_q3=models.Sum('amount_q3'), amount_q4=models.Sum('amount_q4'),
                                                   target_q1=models.Sum('physical_target_q1'),
                                                   target_q2=models.Sum('physical_target_q2'),
                                                   target_q3=models.Sum('physical_target_q3'),
                                                   target_q4=models.Sum('physical_target_q4'))
        self.amount_q1 = round(fs_total['amount_q1'] or 0.0, 2)
        self.amount_q2 = round(fs_total['amount_q2'] or 0.0, 2)
        self.amount_q3 = round(fs_total['amount_q3'] or 0.0, 2)
        self.amount_q4 = round(fs_total['amount_q4'] or 0.0, 2)
        self.amount = round(self.amount_q1 + self.amount_q2 + self.amount_q3 + self.amount_q4, 2)

        self.physical_target_q1 = fs_total['target_q1'] or 0
        self.physical_target_q2 = fs_total['target_q2'] or 0
        self.physical_target_q3 = fs_total['target_q3'] or 0
        self.physical_target_q4 = fs_total['target_q4'] or 0
        self.physical_target = (self.physical_target_q1 + self.physical_target_q2 + self.physical_target_q3 +
                                self.physical_target_q4)

        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = 'PAWAF Item'

    def __str__(self):
        return self.specific_pap


class PawafItemView(models.Model):
    description = models.CharField(max_length=64)
    order = models.PositiveIntegerField(default=100)
    field_ref = models.CharField(max_length=128)
    field_label = models.CharField(max_length=128)
    header_label = models.CharField(max_length=128)
    boolean_label = models.CharField(max_length=128, blank=True, null=True)
    exclude_empty = models.BooleanField(default=True)

    def get_view(self, queryset):
        bal_q = ~models.Q(
            budget_breakdown__release_sources__fund_release_item__fund_release__status__code=consts.RRF_CANCELLED)
        sums = (models.Sum('budget_breakdown__release_sources__charged_q1', filter=bal_q) +
                models.Sum('budget_breakdown__release_sources__charged_q2', filter=bal_q) +
                models.Sum('budget_breakdown__release_sources__charged_q3', filter=bal_q) +
                models.Sum('budget_breakdown__release_sources__charged_q4', filter=bal_q))
        if self.boolean_label:
            true_label, false_label = self.boolean_label.split('$')
            condition = {self.field_label: True}
            ret = queryset.values(self.field_ref).order_by(f'-{self.field_ref}').annotate(
                label=models.Case(
                    models.When(**condition, then=models.Value(true_label)),
                    default=models.Value(false_label), output_field=models.CharField(max_length=16)
                ),
                available_balance=models.Sum('amount') - Coalesce(sums, 0.0),
                amount=models.Sum('amount'),
                physical_target=models.Sum('physical_target'),
            )
        else:
            ret = queryset.values(self.field_ref).order_by(self.field_label).annotate(
                label=models.F(self.field_label),
                available_balance=models.Sum('amount') - Coalesce(sums, 0.0),
                amount=models.Sum('amount'),
                physical_target=models.Sum('physical_target'),
            )

        if self.exclude_empty:
            condition = {self.field_ref: None}
            ret = ret.exclude(**condition)
        return ret.order_by(self.field_label)

    def __str__(self):
        return self.description


class PawafItemBudgetBreakdown(models.Model):
    pawaf_item = models.ForeignKey(PawafItem, models.CASCADE, related_name='budget_breakdown')
    object_code = models.ForeignKey(ObjectCode, models.DO_NOTHING, related_name='+', null=True, blank=True)
    procurement_mode = models.ForeignKey(ProcurementMode, models.DO_NOTHING, related_name='+', null=True)
    amount_q1 = models.FloatField(default=0.0)
    amount_q2 = models.FloatField(default=0.0)
    amount_q3 = models.FloatField(default=0.0)
    amount_q4 = models.FloatField(default=0.0)
    physical_target_q1 = models.PositiveIntegerField(default=0)
    physical_target_q2 = models.PositiveIntegerField(default=0)
    physical_target_q3 = models.PositiveIntegerField(default=0)
    physical_target_q4 = models.PositiveIntegerField(default=0)

    amount = models.FloatField(default=0.0)
    physical_target = models.PositiveIntegerField(default=0)

    @property
    def charged_q1(self):
        charged = self.release_sources.aggregate(
            x=models.Sum('charged_q1'))['x'] or 0.0

        return round(charged, 2)

    @property
    def charged_q2(self):
        charged = self.release_sources.aggregate(
            x=models.Sum('charged_q2'))['x'] or 0.0

        return round(charged, 2)

    @property
    def charged_q3(self):
        charged = self.release_sources.aggregate(
            x=models.Sum('charged_q3'))['x'] or 0.0

        return round(charged, 2)

    @property
    def charged_q4(self):
        charged = self.release_sources.aggregate(
            x=models.Sum('charged_q4'))['x'] or 0.0

        return round(charged, 2)

    @property
    def charged_amount(self):
        charged = self.release_sources.aggregate(
            x=(Coalesce(models.Sum('charged_q1'), 0.) + Coalesce(models.Sum('charged_q2'), 0.) +
               Coalesce(models.Sum('charged_q3'), 0.) + Coalesce(models.Sum('charged_q4'), 0.)))['x'] or 0.0

        return round(charged, 2)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.amount_q1 = round(self.amount_q1, 2)
        self.amount_q2 = round(self.amount_q2, 2)
        self.amount_q3 = round(self.amount_q3, 2)
        self.amount_q4 = round(self.amount_q4, 2)

        self.amount = round(self.amount_q1 + self.amount_q2 + self.amount_q3 + self.amount_q4, 2)
        self.physical_target = (self.physical_target_q1 + self.physical_target_q2 + self.physical_target_q3 +
                                self.physical_target_q4)
        super().save(force_insert, force_update, using, update_fields)


def random_init():
    seq = string.ascii_lowercase + string.digits
    return ''.join(random.choices(seq, k=32))


class Status(models.Model):
    code = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=64)
    order = models.PositiveIntegerField(default=100)

    class Meta:
        verbose_name_plural = 'Statuses'

    def __str__(self):
        return self.name


class FundRelease(models.Model):
    date = models.DateField(default=datetime.date.today)
    rrf_no = models.CharField(max_length=32, default=random_init, unique=True)
    status = models.ForeignKey(Status, models.DO_NOTHING, null=True)  # TODO Fix after migration
    serial = models.PositiveIntegerField(default=0)
    reference = models.TextField(null=True)
    footer_control = models.CharField(max_length=16)

    budget = models.ForeignKey(Pawaf, models.DO_NOTHING, related_name='+', null=True, blank=True)
    other_budget = models.CharField(max_length=128, blank=True, null=True)
    specific_paps = models.ManyToManyField(PawafItem, blank=True)

    cmd = models.BooleanField(default=False)

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def year(self):
        return self.date.year

    @classmethod
    def get_next_serial(cls, year):
        try:
            last = cls.objects.filter(date__year=year).only('serial').latest('serial')
            last = last.serial
        except cls.DoesNotExist:
            last = 0
        return last + 1

    @property
    def major_paps_print(self):
        data = list(self.specific_paps.distinct('suggested_pap__sub_pap__major_pap__name').
                    values_list('suggested_pap__sub_pap__major_pap__name', flat=True))
        for i, e in enumerate(data):
            if e.startswith('MP'):
                data[i] = e.split(' ', 1)[1]
        return ' / '.join(data)

    @property
    def suggested_paps_print(self):
        data = list(self.specific_paps.distinct('suggested_pap__name').
                    values_list('suggested_pap__name', flat=True))
        for i, e in enumerate(data):
            if e.startswith('SP'):
                data[i] = e.split(' ', 1)[1]
        return ' / '.join(data)

    @property
    def specific_paps_print(self):
        return ' / '.join(self.specific_paps.values_list('specific_pap', flat=True))

    def assign_rrf_no(self, pref_serial=None):
        self.serial = pref_serial or self.get_next_serial(self.date.year)
        self.rrf_no = f'OG4-{self.date.year}-{self.serial:03}'

    @property
    def footer(self):
        return f'HPAG4/PPB/RRF/{self.footer_control}'

    @property
    def amount(self):
        return round(self.release_items.aggregate(x=models.Sum('release_recipients__amount'))['x'] or 0.0, 2)

    @property
    def released(self):
        val = self.release_items.aggregate(x=models.Sum('asa_items__amount'))['x'] or 0.0
        return round(val, 2)

    @property
    def balance(self):
        amount = self.release_items.aggregate(x=models.Sum('release_recipients__amount'))['x'] or 0.0
        released = self.release_items.aggregate(x=models.Sum('asa_items__amount'))['x'] or 0.0

        return round(amount - released, 2)

    def __str__(self):
        return self.rrf_no

    class Meta:
        verbose_name = 'Fund Release (RRF)'
        verbose_name_plural = 'Fund Releases (RRF)'


class FundReleaseItem(models.Model):
    fund_release = models.ForeignKey(FundRelease, models.DO_NOTHING, related_name='release_items')

    object_code = models.ForeignKey(ObjectCode, models.DO_NOTHING, related_name='+')
    program = models.CharField(max_length=8, choices=MajorPap.PA_SUB_PROGRAM_CHOICES)
    mission_area = models.ForeignKey(MissionArea, models.DO_NOTHING, related_name='+')

    q1 = models.BooleanField(default=False)  # FIXME deprecated. remove upon correction of records
    q2 = models.BooleanField(default=False)  # FIXME deprecated. remove upon correction of records
    q3 = models.BooleanField(default=False)  # FIXME deprecated. remove upon correction of records
    q4 = models.BooleanField(default=False)  # FIXME deprecated. remove upon correction of records

    specific_purpose = models.TextField()

    realignment_level1 = models.BooleanField(default=False)
    realignment_level2 = models.BooleanField(default=False)

    @property
    def chargeability(self):
        # FIXME deprecated. change upon correction of records
        quarters = utils.quarter_formatting(self.q1, self.q2, self.q3, self.q4)

        if self.fund_release.budget_id:
            return f'{quarters} {self.fund_release.budget.description}'
        return f'{quarters} {self.fund_release.other_budget}'

    @property
    def amount(self):
        return round(self.release_recipients.aggregate(x=models.Sum('amount'))['x'] or 0.0, 2)

    @property
    def released(self):
        return round(self.asa_items.aggregate(x=models.Sum('amount'))['x'] or 0.0, 2)

    @property
    def balance(self):
        return round(self.amount - self.released, 2)


class FundReleaseSource(models.Model):
    fund_release_item = models.ForeignKey(FundReleaseItem, models.CASCADE, related_name='release_sources')
    fund_source = models.ForeignKey(PawafItemBudgetBreakdown, models.DO_NOTHING, related_name='release_sources')
    charged_q1 = models.FloatField(default=0.0)
    charged_q2 = models.FloatField(default=0.0)
    charged_q3 = models.FloatField(default=0.0)
    charged_q4 = models.FloatField(default=0.0)
    charged_amount = models.FloatField(default=0.0)  # FIXME deprecated

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.charged_q1 = round(self.charged_q1, 2)
        self.charged_q2 = round(self.charged_q2, 2)
        self.charged_q3 = round(self.charged_q3, 2)
        self.charged_q4 = round(self.charged_q4, 2)
        self.charged_amount = round(self.charged_amount, 2)
        super().save(force_insert, force_update, using, update_fields)


class FundReleaseRecipient(models.Model):
    fund_release_item = models.ForeignKey(FundReleaseItem, models.CASCADE, related_name='release_recipients')
    servicing_mfo = models.ForeignKey(Pamu, models.DO_NOTHING, related_name='+')
    unit = models.ForeignKey(Unit, models.DO_NOTHING, related_name='+')
    amount = models.FloatField(default=0.0)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.amount = round(self.amount, 2)
        super().save(force_insert, force_update, using, update_fields)


class FundReleaseAsa(models.Model):
    advice_no = models.CharField(max_length=32)
    date_released = models.DateField()
    unit = models.ForeignKey(Unit, models.DO_NOTHING, related_name='+', null=True, blank=True)
    servicing_mfo = models.ForeignKey(Pamu, models.DO_NOTHING, related_name='+')
    purpose = models.TextField()
    fund_releases = models.ManyToManyField(FundRelease, blank=True)
    is_withdrawal = models.BooleanField(default=False)

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def amount(self):
        return round(self.asa_items.aggregate(x=models.Sum('amount'))['x'] or 0.0, 2)

    def __str__(self):
        return self.advice_no

    class Meta:
        verbose_name = 'ASA'
        verbose_name_plural = 'ASA'


class FundReleaseAsaItem(models.Model):
    asa = models.ForeignKey(FundReleaseAsa, models.CASCADE, related_name='asa_items')
    release_item = models.ForeignKey(FundReleaseItem, models.DO_NOTHING, related_name='asa_items')
    amount = models.FloatField(default=0)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if self.asa.is_withdrawal:
            self.amount = -abs(self.amount)

        self.amount = round(self.amount, 2)
        super().save(force_insert, force_update, using, update_fields)

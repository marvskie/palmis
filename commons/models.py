from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

from commons import consts

MAJOR_ISLANDS = (
    ('Luzon', 'Luzon'),
    ('Visayas', 'Visayas'),
    ('Mindanao', 'Mindanao')
)

QUARTER_CHOICES = (
    ('Q1', '1st Qtr'),
    ('Q2', '2nd Qtr'),
    ('Q3', '3rd Qtr'),
    ('Q4', '4th Qtr')
)


EVAL_FORMAT = '<span style="color:#FFFFFF;background-color:{color};' \
                  'line-height:1;text-align:center;border-radius:0.25rem;' \
                  'padding:.3em .5em; display:inline-block">{evaluation}</span>'


class Pamu(models.Model):
    code = models.CharField(max_length=32, unique=True, null=True)
    name = models.CharField(max_length=32, unique=True)

    class Meta:
        verbose_name = 'PAMU'

    def __str__(self):
        return self.name


class Fssu(models.Model):
    name = models.CharField(max_length=32, unique=True)
    code = models.CharField(max_length=32, unique=True, null=True)

    class Meta:
        verbose_name = 'FSSU'

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=32)
    mother_unit = models.ForeignKey(Pamu, models.DO_NOTHING, related_name='+')
    pamu = models.ForeignKey(Pamu, models.DO_NOTHING, related_name='sub_units', null=True)
    alt_pamu = models.ForeignKey(Pamu, models.DO_NOTHING, related_name='alt_sub_units', null=True, blank=True)

    def __str__(self):
        return f'{self.name} ({self.mother_unit})'


class Branch(models.Model):
    name = models.CharField(max_length=32)
    code = models.CharField(max_length=8, unique=True)
    order = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.name


class Sprs(models.Model):
    pamu = models.ForeignKey(Pamu, models.DO_NOTHING)
    address = models.TextField()

    def __str__(self):
        return f'{self.pamu.name} SPRS'


class Organization(models.Model):
    name = models.CharField(max_length=32, unique=True)
    code = models.CharField(max_length=8, unique=True)
    fullname = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    def natural_key(self):
        return str(self.name)
        
class Role(models.Model):
    organization = models.ForeignKey(Organization, models.CASCADE, related_name='roles')
    name = models.CharField(max_length=32)
    code = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return f'{self.name}, {self.organization.name}'


class Account(models.Model):
    user = models.OneToOneField(User, models.DO_NOTHING, null=False, blank=False )
    role = models.ForeignKey(Role, models.DO_NOTHING, related_name='accounts', null=False, blank=False)

    name = models.CharField(max_length=128)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(null=True, blank=True)
    mobile_no = models.CharField(max_length=12, null=True, blank=True)
    initials = models.CharField(max_length=8, default='')

    active = models.BooleanField(default=False)
    require_change_pw = models.BooleanField(default=True)
    bypass_otp = models.BooleanField(default=False)

    pamu = models.ForeignKey(Pamu, models.DO_NOTHING, null=True, blank=True)
    fssu = models.ForeignKey(Fssu, models.DO_NOTHING, null=True, blank=True)

    special_permissions = JSONField(null=True, blank=True)

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.first_name = self.first_name.title()
        self.last_name = self.last_name.title()
        self.name = f'{self.first_name} {self.last_name}'
        super().save(force_insert, force_update, using, update_fields)

    def is_cmd(self):
        return self.special_permissions and 'can_rrf_cmd' in self.special_permissions.get('ppb', [])

    def account_dict(self):
        user_account = {
            'active': self.active,
            'organization': self.role.organization.code,
            'division': self.division(),
            'role': self.role.code if self.role_id else None
        }
        return user_account

    def division_name(self):
        org_code = self.role.organization.code

        if consts.is_hpa(org_code):
            return None
        elif org_code == consts.PAMU:
            return self.pamu.name
        elif org_code == consts.FSSU:
            return self.fssu.name
    division_name.short_description = 'Division'

    def division(self):
        org_code = self.role.organization.code

        if consts.is_hpa(org_code):
            return None
        elif org_code == consts.PAMU:
            return self.pamu_id
        elif org_code == consts.FSSU:
            return self.fssu_id

    def __str__(self):
        return self.user.username
    
    def natural_key(self):
        return str(self.role)


class Serviceability(models.Model):
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=4, unique=True)

    class Meta:
        verbose_name_plural = 'Serviceabilities'

    def __str__(self):
        return f'{self.name}'


class AcquisitionMode(models.Model):
    name = models.CharField(max_length=16)
    code = models.CharField(max_length=16, unique=True)

    class Meta:
        verbose_name_plural = 'Modes of acquisition'

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=64)
    designation = models.CharField(max_length=128)
    island_group = models.CharField(max_length=8, choices=MAJOR_ISLANDS)

    def __str__(self):
        return self.name


class ProcurementMode(models.Model):
    code = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=64)
    full_name = models.CharField(max_length=256)
    order = models.PositiveIntegerField(default=100)

    class Meta:
        verbose_name = 'Mode of procurement'
        verbose_name_plural = 'Modes of procurement'

    def __str__(self):
        return self.full_name


class ForceStructure(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name
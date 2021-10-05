from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import related
from django.db.models.query_utils import select_related_descend
from django.forms.widgets import ChoiceWidget
import utils
from famis.constants import *
import random
from django.utils.html import format_html
# ============== NEW FAMIS MODELS 

# def number_default_function():
#     return random.randint(111111,699999)

class Inventory(models.Model):
    #facility
    pamu = models.CharField(max_length=512, null=True, choices=PAMU_LIST)
    sub_unit = models.CharField(max_length=512, unique=True, choices=SUB_UNIT_LIST)
    location = models.CharField(max_length=512, null=True)

    pamu_profile = models.ImageField(upload_to=utils.PathAndRename('uploads/famis/%Y/%m/'))

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ''
        verbose_name_plural = 'Inventory'
    def __str__(self):
        return self.sub_unit

class FacilityInfo(models.Model):
    sub_unit = models.ForeignKey(Inventory, to_field="sub_unit", on_delete=models.CASCADE, related_name="facility_info")
    name_of_facility = models.CharField(max_length=512, null=True, unique=True)
    facility_classification = models.CharField(max_length=512, null=True, choices=Facility_Classification)
    area_or_inm_or_width = models.CharField(max_length=512, null=True)
    bldg_or_utility_code = models.CharField(max_length=512, null=True)
    building_administrator = models.CharField(max_length=512, null=True)
    mode_of_acquisition = models.CharField(max_length=512, null=True, choices=Mode_OF_ACQUISITION)
    year_acquired = models.CharField(max_length=512, null=True)
    master_developmental_plan_alignment = models.CharField(max_length=512, null=True)
    building_insurance_nr  = models.CharField(max_length=512, null=True)
    amount_of_insurance  = models.CharField(max_length=512, null=True)
    original_amount = models.CharField(max_length=512, null=True)
    appraised_value = models.CharField(max_length=512, null=True)
    date_of_appraised_value = models.DateField(null=True)
    class Meta:
        verbose_name = 'Facility'
        verbose_name_plural = 'Facility'
    
    def __str__(self):
        return self.name_of_facility

        # return format_html('<br>{}</br><tr><td><label>{}</label></td><td><label>{}</label></td><td><label>{}</label></td><td><label>{}</label></td><td><label>{}</label></td><td><label>{}</label></td><td><label>{}</label></td><td><label>{}</label></td><td><label>{}</label></td><td><label>{}</label></td><td><label>{}</label></td><td><label>{}</label></td><td><label>{}</label></td></tr>'.format(self.name_of_facility,self.name_of_facility,
        #         self.facility_classification,
        #         self.area_or_inm_or_width,
        #         self.bldg_or_utility_code,
        #         self.building_administrator,
        #         self.mode_of_acquisition,
        #         self.year_acquired,
        #         self.master_developmental_plan_alignment,
        #         self.building_insurance_nr,
        #         self.amount_of_insurance,
        #         self.original_amount,
        #         self.appraised_value,
        #         self.date_of_appraised_value
        #     )
        # )

class FacilityMaintenance(models.Model):
    name_of_facility = models.ForeignKey(FacilityInfo,to_field='name_of_facility', on_delete=models.CASCADE, related_name="+")
    amount_enhanced_or_repair = models.CharField(max_length=512, null=True)
    date_or_year_of_enhanced_or_repair = models.DateField(null=True)
    fund  = models.CharField(max_length=512, null=True)
    date_requested = models.DateField(null=True) 
    date_of_repair_or_enhancement = models.DateField(null=True)
    amount_of_repair_or_enhancement = models.CharField(max_length=512, null=True)
    qualitative_scale   = models.CharField(max_length=512, null=True)

    repair_images = models.ImageField(upload_to=utils.PathAndRename('uploads/famis/%Y/%m/'))

    class Meta:
        verbose_name = 'Facility Maintenance'
        verbose_name_plural = 'Facility Maintenance'
    def __str__(self):
        return self.amount_enhanced_or_repair

class RealStateInfo(models.Model):
    sub_unit = models.ForeignKey(Inventory, to_field="sub_unit", on_delete=models.CASCADE, related_name="real_state")
    camp_code = models.CharField(max_length=512, null=True)
    name_of_Camp  = models.CharField(max_length=512, null=True)
    region = models.CharField(max_length=512, null=True)
    total_area_or_hectares  = models.CharField(max_length=512, null=True)
    total_perimeter_or_meter    = models.CharField(max_length=512, null=True)
    topography = models.CharField(max_length=512, null=True)  
    basis_of_development = models.CharField(max_length=512, null=True)
    perimeter_with_fence_or_meter = models.CharField(max_length=512, null=True)
    type_of_fence = models.CharField(max_length=512, null=True)
    development_year_acquired = models.DateField(null=True)
    unit_code_administrator = models.CharField(max_length=512, null=True)
    tenant_unit_or_lgu_or_civ   = models.CharField(max_length=512, null=True)
    total_area_occupied_developed  = models.CharField(max_length=512, null=True)
    nr_of_facility_established = models.CharField(max_length=512, null=True)
    type_of_ownership = models.CharField(max_length=512, null=True)
    authority_of_ownership = models.CharField(max_length=512, null=True) 
    date_acquired = models.DateTimeField(auto_now_add=False, null=True)
    date_of_renewal = models.DateField(null=True)
    progress_of_titling = models.CharField(max_length=512, null=True) 
    date_of_progress_titling = models.DateField(null=True)
    unit_in_charge_of_titling = models.CharField(max_length=512, null=True)   
    amount_programmed_for_titling = models.CharField(max_length=512, null=True)
    amount_downloaded_for_titling = models.CharField(max_length=512, null=True)
    area_of_idle_land  = models.CharField(max_length=512, null=True)
    area_of_land_leased = models.CharField(max_length=512, null=True)
    year_leased = models.CharField(max_length=512, null=True)
    date_of_expiration = models.DateField(null=True)
    economic_zone_classification = models.CharField(max_length=512, null=True)
    class Meta:
        verbose_name = 'RealtState'
        verbose_name_plural = 'Real State'
    def __str__(self):
        return self.camp_code
        #     return self.sub_unit, format_html('<tr><td><label>{}</label><td><label>{}</label></td><td><label>{}</label></td><td><label>{}</label></td><td><label>{}</label></td><td><label>{}</label></td><td><label>{}</label></td><td><label>{}</label></td><td><label>{}</label></td><td><label>{}</label></td><td><label>{}</label></td><td><label>{}</label></td><td><label>{}</label></td><td><label>{}</label></td><td><label>{}</label></td><td><label>{}</label></td><td><label>{}</label></td><td><label>{}</label></td><td><label>{}</label></td><td><label>{}</label></td><td><label>{}</label></td><td><label>{}</label></td><td><label>{}</label></td><td><label>{}</label></td><td><label>{}</label></td><td><label>{}</label></td><td><label>{}</label></td><td><label>{}</label></td></td></tr>'.format(self.camp_code,
        #         self.name_of_Camp,
        #         self.region,
        #         self.total_area_or_hectares,
        #         self.total_perimeter_or_meter,
        #         self.topography,
        #         self.basis_of_development,
        #         self.perimeter_with_fence_or_meter,
        #         self.type_of_fence,
        #         self.development_year_acquired,
        #         self.unit_code_administrator,
        #         self.tenant_unit_or_lgu_or_civ,
        #         self.total_area_occupied_developed,
        #         self.nr_of_facility_established,
        #         self.type_of_ownership,
        #         self.authority_of_ownership,
        #         self.date_acquired,
        #         self.date_of_renewal,
        #         self.progress_of_titling,
        #         self.date_of_progress_titling,
        #         self.unit_in_charge_of_titling,
        #         self.amount_programmed_for_titling,
        #         self.amount_downloaded_for_titling,
        #         self.area_of_idle_land,
        #         self.area_of_land_leased,
        #         self.year_leased,
        #         self.date_of_expiration,
        #         self.economic_zone_classification,
        #     )
        # )

class Reports(models.Model):
    report_name = models.CharField(max_length=512, null=True)
    real_state = models.ForeignKey(RealStateInfo, on_delete=models.CASCADE, related_name="realstate_d")
    facility = models.ForeignKey(FacilityInfo, on_delete=models.CASCADE, related_name="facility_d")

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ''
        verbose_name_plural = 'Reports'
    def __str__(self):
        return self.report_name
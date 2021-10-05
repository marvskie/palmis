from typing import List
from django.contrib import admin
from django.db.models import Count
from django.contrib.admin.views.main import ChangeList
from django.db.models.fields.related import ForeignKey
from django.utils import safestring
from django.utils.safestring import SafeString
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.utils.html import format_html

from famis import models

import utils

class FacilityInfoInline(admin.TabularInline):
    model = models.FacilityInfo
    extra = 0

class RealStateInline(admin.TabularInline):
    model = models.RealStateInfo
    extra = 0

class FacilityMaintenanceInline(admin.TabularInline):
    model = models.FacilityMaintenance
    extra = 0

class FacilityInfoResource(resources.ModelResource):
    class Meta:
        model = models.FacilityInfo
        exclude = ('date','created_by','updated_by', 'created_at', 'updated_at')

class FacilityMaintenanceResource(resources.ModelResource):
    class Meta:
        model = models.FacilityMaintenance
        exclude = ('date','created_by','updated_by', 'created_at', 'updated_at')

class InventoryResource(resources.ModelResource):
    class Meta:
        model = models.Inventory
        exclude = ('date','created_by','updated_by', 'created_at', 'updated_at')

class InventoryAdmin(ImportExportModelAdmin):
    resource_class = InventoryResource
    list_display = ('pamu', 'sub_unit','location','image_tag','facility_info','real_state',)
    list_filter = ('pamu', 'sub_unit','location',)
    search_fields = ('pamu', 'sub_unit','location',)
    list_per_page = 10000

    inlines = [FacilityInfoInline, RealStateInline]

    exclude = ('created_by','updated_by', 'created_at', 'updated_at',)

    def image_tag(self, obj):
        return format_html('<a href="{}"><img src="{}" style="width:70px;height:50px;" /></a>'.format(obj.pamu_profile.url,obj.pamu_profile.url))
    
    image_tag.short_description = "Profile"
    image_tag.allow_tags = True
    image_tag.admin_order_field = "pamu"

    def real_state(self, obj):
         data_list = []
         cards_from_set = obj.real_state.all()
         for card in cards_from_set:
            data_list.append(format_html('{}'.format(card)))
         return format_html(
                '<table class="tb-facility-name h-line"><tr style="display: none;"><th>Camp Code</th><th>Name of Camp</th><th>Region</th><th>Total Area (Hectares)</th><th>Total Perimeter (Meter)</th><th>Topography</th><th>Basis of Development</th><th>Perimeter with Fence (Meter)</th><th>Type of Fence</th><th>Year Acquired</th><th>Unit Code/ Administrator</th><th>Tenant Unit/ LGU/ CIV</th><th>Total Area Occupied/ Developed</th><th>Nr of facility established</th><th>Type of Ownership</th><th>Authority of Ownership</th><th>Date Acquired</th><th>Date of renewal(if acquired through MOA, Reso, etc)</th><th>Progress of land titling</th><th>Date of progress titling</th><th>Unit In Charge of Titling</th><th>Amount Programmed For Titling</th><th>Amount Downloaded For Titling</th><th>Area of idle land</th><th>Area of Land Leased</th><th>Year Leased</th><th>Date of Expiration</th><th>Economic Zone Classification</th></tr>{}</table>'
                .format(data_list)
            )
    
    real_state.short_description = format_html('{}</br><table class="tb-facility-name"><tr style="display:none;"><th>Camp Code</th><th>Name of Camp</th><th>Region</th><th>Total Area (Hectares)</th><th>Total Perimeter (Meter)</th><th>Topography</th><th>Basis of Development</th><th>Perimeter with Fence (Meter)</th><th>Type of Fence</th><th>Year Acquired</th><th>Unit Code/ Administrator</th><th>Tenant Unit/ LGU/ CIV</th><th>Total Area Occupied/ Developed</th><th>Nr of facility established</th><th>Type of Ownership</th><th>Authority of Ownership</th><th>Date Acquired</th><th>Date of renewal(if acquired through MOA, Reso, etc)</th><th>Progress of land titling</th><th>Date of progress titling</th><th>Unit In Charge of Titling</th><th>Amount Programmed For Titling</th><th>Amount Downloaded For Titling</th><th>Area of idle land</th><th>Area of Land Leased</th><th>Year Leased</th><th>Date of Expiration</th><th>Economic Zone Classification</th></tr><tr><td><label>Camp Code</label></td><td><label>Name of Camp</label></td><td><label>Region</label></td><td><label>Total Area (Hectares)</label></td><td><label>Total Perimeter (Meter)</label></td><td><label>Topography</label></td><td><label>Basis of Development</label></td><td><label>Perimeter with Fence (Meter)</label></td><td><label>Type of Fence</label></td><td><label>Year Acquired</label></td><td><label>Unit Code/ Administrator</label></td><td><label>Tenant Unit/ LGU/ CIV</label></td><td><label>Total Area Occupied/ Developed</label></td><td><label>Nr of facility established</label></td><td><label>Type of Ownership</label></td><td><label>Authority of Ownership</label></td><td><label>Date Acquired</label></td><td><label>Date of renewal(if acquired through MOA, Reso, etc)</label></td><td><label>Progress of land titling</label></td><td><label>Date of progress titling</label></td><td><label>Unit In Charge of Titling</label></td><td><label>Amount Programmed For Titling</label></td><td><label>Amount Downloaded For Titling</label></td><td><label>Area of idle land</label></td><td><label>Area of Land Leased</label></td><td><label>Year Leased</label></td><td><label>Date of Expiration</label></td><td><label>Economic Zone Classification</label></td></tr></table>'.format("Real State")) 
    real_state.admin_order_field = "real_state"

    def facility_info(self, obj):
        data_list = []
        cards_from_set = obj.facility_info.all()
        for card in cards_from_set:
            data_list.append(format_html('{}'.format(card)))
        return format_html(
                '<table class="tb-facility-name h-line"><tr style="display: none;"><th>Name of Facility</th><th>Facility Classification</th><th>Area/ lnM/ Width</th><th>Bldg/ Utility Code</th><th>Building Administrator</th><th>Mode of Acquisition</th><th>Year Acquired</th><th>Master Developmental Plan Alignment</th><th>Building insurance Nr</th><th>Amount of insurance</th><th>Original Amount</th><th>Appraised Value</th><th>Date of Appraised Value</th></tr>{}</table>'
                .format(data_list)
            )

    facility_info.short_description = format_html('{}</br><table class="tb-facility-name"><tr style="display:none;"><th>Name of Facility</th><th>Facility Classification</th><th>Area/ lnM/ Width</th><th>Bldg/ Utility Code</th><th>Building Administrator</th><th>Mode of Acquisition</th><th>Year Acquired</th><th>Master Developmental Plan Alignment</th><th>Building insurance Nr</th><th>Amount of insurance</th><th>Original Amount</th><th>Appraised Value</th><th>Date of Appraised Value</th></tr><tr><td><label>Name of Facility</label></td><td><label>Facility Classification</label></td><td><label>Area/ lnM/ Width</label></td><td><label>Bldg/ Utility Code</label></td><td><label>Building Administrator</label></td><td><label>Mode of Acquisition</label></td><td><label>Building insurance Nr</label></td><td><label>Amount of insurance</label></td><td><label>Original Amount</label></td><td><label>Appraised Value</label></td><td><label>Date of Appraised Value</label></td><td><label>Year Acquired</label></td><td><label>Master Developmental Plan Alignment</label></td></tr></table>'.format("Facility")) 
    facility_info.admin_order_field = "facility_info"

    def save_model(self, request, obj, form, change):
        if not obj.id:  
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class FacilityAdmin(ImportExportModelAdmin):
    resource_class = FacilityInfoResource
    list_display = ('sub_unit', 'name_of_facility','facility_classification','area_or_inm_or_width','bldg_or_utility_code','building_administrator','mode_of_acquisition','year_acquired','master_developmental_plan_alignment','building_insurance_nr','amount_of_insurance','original_amount','appraised_value','date_of_appraised_value',)
    list_filter = ('sub_unit', 'name_of_facility','facility_classification','bldg_or_utility_code')
    search_fields = ('sub_unit','name_of_facility','facility_classification','bldg_or_utility_code')
    list_per_page = 10000

    inlines = [FacilityMaintenanceInline]

    exclude = ('created_by','updated_by', 'created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class FacilityMaintenanceAdmin(ImportExportModelAdmin):
    resource_class = FacilityMaintenanceResource
    list_display = ('name_of_facility','amount_enhanced_or_repair','date_or_year_of_enhanced_or_repair','fund','date_requested','date_of_repair_or_enhancement','amount_of_repair_or_enhancement','qualitative_scale','image_tag',)
    list_filter = ('name_of_facility',)
    search_fields = ('name_of_facility',)
    list_per_page = 10000

    exclude = ('created_by','updated_by', 'created_at', 'updated_at')
    
    def image_tag(self, obj):
        return format_html('<a href="{}"><img src="{}" style="width:70px;height:50px;" /></a>'.format(obj.repair_images.url,obj.repair_images.url))
    
    image_tag.short_description = "Images"
    image_tag.allow_tags = True
    image_tag.admin_order_field = "name_of_facility"

    def save_model(self, request, obj, form, change):
        if not obj.id:  
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class ReportsAdmin(ImportExportModelAdmin):
    resource_class = InventoryResource
    list_display = ('real_state',)
    list_per_page = 10000
    exclude = ('created_by','updated_by', 'created_at', 'updated_at')
    
    def save_model(self, request, obj, form, change):
        if not obj.id:  
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

admin.site.register(models.Inventory, InventoryAdmin)
admin.site.register(models.FacilityInfo, FacilityAdmin)
admin.site.register(models.Reports, ReportsAdmin)
admin.site.register(models.FacilityMaintenance, FacilityMaintenanceAdmin)




from django import forms
from famis import models
from django.core import validators

SELECT_PAMU = (
    ('', ''),
    ('51EBDE', '51EBDE'),
    ('1ID', '1ID'),
    ('2ID', '2ID'),
)
class FacilityInformation(forms.ModelForm):
    class Meta:
        model = models.Facility
        fields = ['pamu', 'sub_unit', 'location','name_of_facility','facility_classification','area_or_inm_or_width','bldg_or_utility_code','building_administrator','mode_of_acquisition','year_acquired','master_developmental_plan_alignment']
        widgets = {
            'pamu': forms.Select(attrs={'class':'form-control'},choices=SELECT_PAMU),
            'sub_unit': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'name_of_facility': forms.TextInput(attrs={'class': 'form-control'}),
            'facility_classification': forms.TextInput(attrs={'class': 'form-control'}),
            'area_or_inm_or_width': forms.TextInput(attrs={'class': 'form-control'}),
            'bldg_or_utility_code': forms.TextInput(attrs={'class': 'form-control'}),
            'building_administrator': forms.TextInput(attrs={'class': 'form-control'}),
            'mode_of_acquisition': forms.TextInput(attrs={'class': 'form-control'}),
            'year_acquired': forms.TextInput(attrs={'class': 'form-control'}),
            'master_developmental_plan_alignment': forms.TextInput(attrs={'class': 'form-control'}),
        }
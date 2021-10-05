from django.db import models
from django.contrib.auth.models import User
from commons.models import Unit, Pamu, Fssu, Serviceability
from samb.constants import * 
import utils

# ============== NEW PALMIS MODELS 

class PAProject(models.Model):
    fund_source = models.CharField(max_length=50, choices=FUND_SOURCES, null=True, blank=True)
    year = models.IntegerField()
    type_of_commodity = models.CharField(max_length=512) 
    project_title = models.CharField(max_length=512)
    unit_procurement_request_number = models.CharField(max_length=512)
    solicitation_number = models.CharField(max_length=512)
    mode_of_procurement = models.CharField(max_length=512)
    approved_budget_contract = models.FloatField()
    supplier = models.CharField(max_length=512)
    bid_amount = models.FloatField()
    current_status = models.CharField(max_length=512)
    action = models.CharField(max_length=512)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/samb/%Y/%m/'), null=True, blank=True)

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'PA Project'

    def __str__(self):
        return self.project_title

class PITCProject(models.Model):
    fund_source = models.CharField(max_length=50, choices=FUND_SOURCES, null=True, blank=True)
    year = models.IntegerField()
    type_of_commodity = models.CharField(max_length=512)
    project_title = models.CharField(max_length=512)
    unit_procurement_request_number = models.CharField(max_length=512)
    solicitation_number = models.CharField(max_length=512)
    mode_of_procurement = models.CharField(max_length=512)
    approved_budget_contract = models.FloatField()
    supplier = models.CharField(max_length=512)
    bid_amount = models.FloatField()
    current_status = models.CharField(max_length=512)
    action = models.CharField(max_length=512)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/samb/%Y/%m/'), null=True, blank=True)

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'PITC Project'

    def __str__(self):
        return self.project_title

class ProcurementActivityPAProject(models.Model):
    pa_project = models.ForeignKey(PAProject, models.DO_NOTHING, related_name='procurement_activity')
    activity_name = models.CharField(max_length=512)
    details = models.TextField()
    date = models.DateField()
    
    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

class ProcurementActivityPITCProject(models.Model):
    pitc_project = models.ForeignKey(PITCProject, models.DO_NOTHING, related_name='procurement_activity')
    activity_name = models.CharField(max_length=512)
    details = models.TextField()
    date = models.DateField()
    
    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

class BACRecord(models.Model):
    unit = models.CharField(max_length=50)
    name = models.CharField(max_length=512)
    bac_designation = models.CharField(max_length=512)
    unit_description = models.CharField(max_length=512)
    contact_number = models.CharField(max_length=512)
    remarks = models.TextField()
    action = models.CharField(max_length=512)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/samb/%Y/%m/'), null=True, blank=True)

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Bids And Awards Committee'
        verbose_name_plural = 'Bids And Awards Committee'

    def __str__(self):
        return self.name

class TWGRecord(models.Model):
    unit = models.CharField(max_length=50)
    name = models.CharField(max_length=512)
    bac_designation = models.CharField(max_length=512)
    unit_description = models.CharField(max_length=512)
    contact_number = models.CharField(max_length=512)
    remarks = models.TextField()
    action = models.CharField(max_length=512)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/samb/%Y/%m/'), null=True, blank=True)

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Technical Working Group'
        verbose_name_plural = 'Technical Working Group'

    def __str__(self):
        return self.name

class IncomingCommunication(models.Model):
    from_branch = models.CharField(max_length=512)
    commo_type = models.CharField(max_length=512)
    number = models.CharField(max_length=512)
    control_number = models.CharField(max_length=512)
    date_received = models.DateTimeField(auto_now_add=False)
    unit_office = models.CharField(max_length=512)
    subject = models.CharField(max_length=512)
    remarks = models.CharField(max_length=512)
    received_by = models.CharField(max_length=512)
    action = models.CharField(max_length=512)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/samb/%Y/%m/'), null=True, blank=True)


    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Incoming Communication'

    def __str__(self):
        return self.subject

class OutgoingCommunication(models.Model):
    commo_type = models.CharField(max_length=512)
    number = models.CharField(max_length=512)
    control_number = models.CharField(max_length=512)
    origin_branch_office_unit = models.CharField(max_length=512)
    subject = models.CharField(max_length=512)
    recepient_unit = models.CharField(max_length=512)
    date_received = models.DateTimeField(auto_now_add=False)
    remarks = models.CharField(max_length=512)
    received_by = models.CharField(max_length=512)
    action = models.CharField(max_length=512)

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/samb/%Y/%m/'), null=True, blank=True)


    class Meta:
        verbose_name = 'Outgoing Communication'
        
    def __str__(self):
        return self.subject
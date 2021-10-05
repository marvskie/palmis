from django.db import models
from django.contrib.auth.models import User
from commons.models import Unit, Pamu, Fssu, Serviceability

from lob.contants import *
import utils

# ============== NEW PALMIS MODELS 


class AccomplishmentReport(models.Model):
    pamu = models.CharField(max_length=512)  
    number = models.CharField(max_length=512)
    subject = models.CharField(max_length=512)
    title = models.CharField(max_length=512)
   
    quarter = models.CharField(max_length=100, choices=QUARTER_LIST, null=True, blank=True)
    month = models.CharField(max_length=100, choices=MONTH_LIST, null=True, blank=True)
    date_received = models.DateField()
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/lob/%Y/%m/'))
    
    action = models.CharField(max_length=512)
    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Accomplishment Report'
        verbose_name_plural = 'Accomplishment Reports'

    def __str__(self):
        return self.title

class StatusAccomplishmentReport(models.Model):
    date_received = models.DateField() 
    control_number = models.CharField(max_length=512)
    subject = models.CharField(max_length=512)
    origin_office_unit = models.CharField(max_length=512)
    accomplishment_report = models.ForeignKey(AccomplishmentReport, models.DO_NOTHING, related_name='status_accomplishment_reports')

    out_for_action_date = models.DateField(null=True, blank=True)
    target_date = models.DateField(null=True, blank=True)
    remarks = models.TextField()
    in_with_action = models.CharField(max_length=512, null=True, blank=True)
    out_for_approval = models.CharField(max_length=512, null=True, blank=True)
    branch = models.CharField(max_length=100, null=True, blank=True)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/lob/%Y/%m/'))
    
    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Status/Accomplishment Reports'
        verbose_name_plural = 'Status/Accomplishment Reports'

    def __str__(self):
        return self.subject

class IssuesAndConcerns(models.Model):
    pamu = models.CharField(max_length=512)  
    sub_unit = models.CharField(max_length=512)
    date = models.DateField()
    concerned_branch = models.CharField(max_length=512)
    issues_and_concerns = models.TextField()
    action_taken = models.TextField()
    remarks = models.TextField()
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/lob/%Y/%m/'))

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Issues and Concerns'
        verbose_name_plural = 'Issues and Concerns'

    def __str__(self):
        return self.pamu

class CommandDirectedActivities(models.Model):
    number = models.CharField(max_length=512)
    date = models.DateField()
    activity = models.CharField(max_length=512)
    description = models.TextField()
    requirements = models.TextField()
    status = models.CharField(max_length=512)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/lob/%Y/%m/'))  

    action = models.CharField(max_length=512)
    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Command Directed Activities (CAD)'
        verbose_name_plural = 'Command Directed Activities (CAD)'

    def __str__(self):
        return self.activity

class PCHT(models.Model):
    program_status = models.CharField(max_length=50, choices=PROG_UNPROG, null=True, blank=True)
    number = models.CharField(max_length=512)
    unit = models.CharField(max_length=512)
    purpose = models.TextField()
    description = models.TextField()
    requirements = models.TextField()
    amount = models.FloatField()
    status = models.CharField(max_length=512)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/lob/%Y/%m/'))
    
    action = models.CharField(max_length=512)
    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'PCHT'

    def __str__(self):
        return self.activity

class LogisticsSupportPlan(models.Model):
    plan_type = models.CharField(max_length=50, choices=PLAN_TYPE, null=True, blank=True)
    number = models.CharField(max_length=512)
    subject = models.CharField(max_length=512)
    status = models.CharField(max_length=512)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/lob/%Y/%m/'))

    
    action = models.CharField(max_length=512)
    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Logistics Support Plan'

    def __str__(self):
        return self.subject

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
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/lob/%Y/%m/'))


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
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/lob/%Y/%m/'))


    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Outgoing Communication'
        
    def __str__(self):
        return self.subject
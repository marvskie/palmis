from django.db import models
from django.contrib.auth.models import User
from commons.models import Unit, Pamu, Fssu, Serviceability
import utils

# ============== NEW PALMIS MODELS 
class RosterOfTroops(models.Model):
    name = models.CharField(max_length=512)
    last_name = models.CharField(max_length=512)
    first_name = models.CharField(max_length=512)
    middle_name = models.CharField(max_length=512)
    serial_number = models.CharField(max_length=512)
    
    unit = models.CharField(max_length=512)
    title_position = models.CharField(max_length=512)
    branch = models.CharField(max_length=512)
    type_of_employment = models.CharField(max_length=512)
    soi = models.FileField(upload_to=utils.PathAndRename('uploads/admin/%Y/%m/'))
    phs = models.FileField(upload_to=utils.PathAndRename('uploads/admin/%Y/%m/'))
    saln = models.FileField(upload_to=utils.PathAndRename('uploads/admin/%Y/%m/'))
    per = models.FileField(upload_to=utils.PathAndRename('uploads/admin/%Y/%m/'))

    action = models.CharField(max_length=512)
    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Roster of Troops'
        verbose_name_plural = 'Roster of Troops'

    def __str__(self):
        return self.name

class AdminMooe(models.Model):
    number = models.CharField(max_length=512)
    asa_number = models.CharField(max_length=512)
    title_of_document = models.CharField(max_length=512)
    quarter = models.CharField(max_length=512)
    status = models.CharField(max_length=512)
    year = models.IntegerField()
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/admin/%Y/%m/'))


    action = models.CharField(max_length=512)
    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'MOOE'
        verbose_name_plural = 'MOOE'

    def __str__(self):
        return self.name

class AdminEquipment(models.Model):
    number = models.CharField(max_length=512)
    type_of_equipment = models.CharField(max_length=512)
    modal_name = models.CharField(max_length=512)
    purpose = models.CharField(max_length=512)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/admin/%Y/%m/'))

    
    action = models.CharField(max_length=512)
    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Equipment'
        verbose_name_plural = 'Equipment'

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
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/admin/%Y/%m/'))


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
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/admin/%Y/%m/'))

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Outgoing Communication'
        
    def __str__(self):
        return self.subject
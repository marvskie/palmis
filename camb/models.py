from django.db import models
from django.contrib.auth.models import User
from commons.models import Unit, Pamu, Fssu, Serviceability
from camb.constants import *
import utils

# ============== NEW PALMIS MODELS 
class FMSProjects(models.Model):
    project_name = models.CharField(max_length=512)
    fms_case = models.CharField(max_length=512)
    quality = models.FloatField()
    date_loa_accepted = models.DateTimeField(auto_now=False)
    status = models.CharField(max_length=512)
    summary = models.TextField()

    action = models.CharField(max_length=512)
    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'FMS Project'

    def __str__(self):
        return self.project_name

class SRDPProjects(models.Model):
    project_name = models.CharField(max_length=512)
    abc = models.FloatField()
    quality = models.FloatField()
    supplier = models.TextField()
    contract_price = models.FloatField()
    twg_name = models.CharField(max_length=512)
    contact_details = models.TextField()
    status = models.CharField(max_length=512)
    summary_file = models.FileField(upload_to=utils.PathAndRename('uploads/camb/%Y/%m/'))
    
    action = models.CharField(max_length=512)
    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'SRDP Project'

    def __str__(self):
        return self.project_name

class DASProjects(models.Model):
    project_name = models.CharField(max_length=512)
    abc = models.FloatField()
    quality = models.FloatField()
    supplier = models.TextField()
    contract_price = models.FloatField()
    twg_name = models.CharField(max_length=512)
    contact_details = models.TextField()
    summary_file = models.FileField(upload_to=utils.PathAndRename('uploads/camb/%Y/%m/'))
    
    action = models.CharField(max_length=512)
    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'DAS Project'

    def __str__(self):
        return self.project_name


class DASPhoto(models.Model):
    activity = models.CharField(max_length=512)
    remarks = models.TextField()
    project = models.ForeignKey(DASProjects, models.DO_NOTHING, related_name='das_project_photos')
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/camb/%Y/%m/'))

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'DAS Photo'
        verbose_name_plural = 'DAS Photos'

    def __str__(self):
        return self.activity
        
class DASProjectFile(models.Model):
    title = models.CharField(max_length=512)
    das_project = models.ForeignKey(DASProjects, models.DO_NOTHING, related_name='das_project_files')
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/camb/%Y/%m/'))

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'DAS Related Files'
        verbose_name_plural = 'DAS Related Files'

    def __str__(self):
        return self.title





class DASProjectStatus(models.Model):
    das_project = models.ForeignKey(DASProjects, models.DO_NOTHING, related_name='+')
    quantity = models.IntegerField()
    abc = models.FloatField()
    twg = models.CharField(max_length=512)

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'DAS Project Status'
        verbose_name_plural = 'DAS Project Status'

    def __str__(self):
        return ''


class FMSPhoto(models.Model):
    activity = models.CharField(max_length=512)
    remarks = models.TextField()
    project = models.ForeignKey(FMSProjects, models.DO_NOTHING, related_name='fms_project_photos')
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/camb/%Y/%m/'))

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'FMS Photo'
        verbose_name_plural = 'FMS Photos'

    def __str__(self):
        return self.activity


# ========= DAS Status 

class DASProjectStatusAcquisition(models.Model):
    project_phase = models.CharField(max_length=512, choices=PROJECT_PHASE)
    project_name = models.CharField(max_length=512)
    first_pass_assessment = models.CharField(max_length=512)
    first_pass_pa_cdb = models.CharField(max_length=512)
    first_pass_afpseo = models.CharField(max_length=512)
    first_pass_das_adhoc_committee = models.CharField(max_length=512)
    first_pass_afp_cdb = models.CharField(max_length=512)
    first_pass_slrtd_approval = models.CharField(max_length=512)
    first_pass_apm = models.CharField(max_length=512)

    second_pass_assessment = models.CharField(max_length=512)
    second_pass_pa_cdb = models.CharField(max_length=512)
    second_pass_afpseo = models.CharField(max_length=512)
    second_pass_das_adhoc_committee = models.CharField(max_length=512)
    second_pass_afp_cdb = models.CharField(max_length=512)
    second_pass_slrtd_approval = models.CharField(max_length=512)
    second_pass_submission_of_decision_package = models.CharField(max_length=512)
    second_pass_apm = models.CharField(max_length=512)

    das_project_status = models.OneToOneField(DASProjectStatus, models.DO_NOTHING, related_name='das_project_acquisition_phase')

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Acquisition Phase'
        verbose_name_plural = 'Acquisition Phase'

    def __str__(self):
        return '{}:{}'.format(self.project_name, self.project_phase) 

class DASProjectStatusProcurement(models.Model):
    project_phase = models.CharField(max_length=512, choices=PROJECT_PHASE)
    project_name = models.CharField(max_length=512)
    
    preliminary_discussion = models.CharField(max_length=512)
    pre_proc = models.CharField(max_length=512)
    invitation_to_bid = models.CharField(max_length=512)
    pre_bid = models.CharField(max_length=512)
    sobe = models.CharField(max_length=512)
    post_qualification = models.CharField(max_length=512)
    noa = models.CharField(max_length=512)

    das_project_status = models.OneToOneField(DASProjectStatus, models.DO_NOTHING, related_name='das_project_procurement_phase')

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Procurement Phase'
        verbose_name_plural = 'Procurement Phase'

    def __str__(self):
        return '{}:{}'.format(self.project_name, self.project_phase) 

class DASProjectStatusContractFinalization(models.Model):
    project_phase = models.CharField(max_length=512, choices=PROJECT_PHASE)
    project_name = models.CharField(max_length=512)
    
    contract_preparation = models.CharField(max_length=512)
    atr = models.CharField(max_length=512)
    aa = models.CharField(max_length=512)
    obr = models.CharField(max_length=512)
    caf = models.CharField(max_length=512)
    tjag_opinion = models.CharField(max_length=512)
    csafp_approval = models.CharField(max_length=512)
    snd_approval = models.CharField(max_length=512)
    ntp = models.CharField(max_length=512)

    das_project_status = models.OneToOneField(DASProjectStatus, models.DO_NOTHING, related_name='das_project_contract_finalization_phase')

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Contract Finalization Phase'
        verbose_name_plural = 'Contract Finalization Phase'

    def __str__(self):
        return '{}:{}'.format(self.project_name, self.project_phase)

class DASProjectStatusContractImplementation(models.Model):
    project_phase = models.CharField(max_length=512, choices=PROJECT_PHASE)
    project_name = models.CharField(max_length=512)
    
    issuance_of_nca = models.CharField(max_length=512)
    opening_of_lc_fund_transfer = models.CharField(max_length=512)
    conduct_of_pdi = models.CharField(max_length=512)
    delivery = models.CharField(max_length=512)
    tiac = models.CharField(max_length=512)
    completed = models.CharField(max_length=512)
    
    das_project_status = models.OneToOneField(DASProjectStatus, models.DO_NOTHING, related_name='das_project_contract_implementation_phase')

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Contract Implementation Phase'
        verbose_name_plural = 'Contract Implementation Phase'
    def __str__(self):
        return '{}:{}'.format(self.project_name, self.project_phase)

# ========= END

class SRDPPhoto(models.Model):
    activity = models.CharField(max_length=512)
    remarks = models.TextField()
    project = models.ForeignKey(SRDPProjects, models.DO_NOTHING, related_name='srdp_project_photos')
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/camb/%Y/%m/'))

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'SRDP Photo'
        verbose_name_plural = 'SRDP Photos'

    def __str__(self):
        return self.activity

class SRDPProjectFile(models.Model):
    title = models.CharField(max_length=512)
    srdp_project = models.ForeignKey(SRDPProjects, models.DO_NOTHING, related_name='srdp_project_files')
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/camb/%Y/%m/'))

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'SRDP Related Files'
        verbose_name_plural = 'SRDP Related Files'

    def __str__(self):
        return self.title


class InternationalLogisticsActivities(models.Model):
    activity = models.CharField(max_length=512)
    date = models.DateField(auto_now_add=False)
    description = models.TextField()
    status = models.CharField(max_length=512)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/camb/%Y/%m/'))

    action = models.CharField(max_length=512)
    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'International Logistics Activity'
        verbose_name_plural = 'International Logistics Activities'

    def __str__(self):
        return self.activity

class DraftDocuments(models.Model):
    title = models.CharField(max_length=512)
    filesize = models.FloatField()
    file_type = models.CharField(max_length=512)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/camb/%Y/%m/'))

    action = models.CharField(max_length=512)
    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Draft Document'

    def __str__(self):
        return self.title

class ReferencesHelpfulLinks(models.Model):
    name = models.CharField(max_length=512)
    url = models.CharField(max_length=512)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/camb/%Y/%m/'))


    action = models.CharField(max_length=512)
    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Helpful Link'

    def __str__(self):
        return self.name

class ReferencesDefenseExhibits(models.Model):
    name = models.CharField(max_length=512)
    url = models.CharField(max_length=512)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/camb/%Y/%m/'))


    action = models.CharField(max_length=512)
    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Defence Exhibit'

    def __str__(self):
        return self.name

class ReferencesPolicies(models.Model):
    subject = models.CharField(max_length=512)
    origin = models.CharField(max_length=512)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/camb/%Y/%m/'))

    action = models.CharField(max_length=512)
    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Policies Reference'

    def __str__(self):
        return self.subject

class ReferencesBrochures(models.Model):
    subject = models.CharField(max_length=512)
    type_of_commodity = models.CharField(max_length=512)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/camb/%Y/%m/'))

    action = models.CharField(max_length=512)
    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Brochures Reference'

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
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/camb/%Y/%m/'))


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
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/camb/%Y/%m/'))


    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Outgoing Communication'
        
    def __str__(self):
        return self.subject
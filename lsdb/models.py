from django.db import models
from django.contrib.auth.models import User
from commons.models import Unit, Pamu, Fssu, Serviceability

from lsdb.contants import *
import utils

# ============== NEW PALMIS MODELS 

class InternationalMilitaryAffairsActivity(models.Model):
    activity_type = models.CharField(max_length=512, choices=IMA_ACTIVITY_TYPE)
    activity = models.CharField(max_length=512)
    country = models.CharField(max_length=512)

    venue = models.CharField(max_length=512)
    remarks = models.TextField(null=True, blank=True)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/lsdb/%Y/%m/'))

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'International Military Affairs'
        verbose_name_plural = 'International Military Affairs'


    def __str__(self):
        return self.activity

class InternationalMilitaryAffairsActivityPhoto(models.Model):
    remarks = models.TextField()
    activity = models.ForeignKey(InternationalMilitaryAffairsActivity, models.DO_NOTHING, related_name='ima_photos')
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/lsdb/%Y/%m/'))

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'

class InternationalMilitaryAffairsActivityReport(models.Model):
    title = models.CharField(max_length=512)
    activity = models.ForeignKey(InternationalMilitaryAffairsActivity, models.DO_NOTHING, related_name='ima_activity_reports')
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/lsdb/%Y/%m/'))

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'After Activity Report'
        verbose_name_plural = 'After Activity Reports'

    def __str__(self):
            return self.title

class LogisticsOfficersForumActivity(models.Model):
    activity_type = models.CharField(max_length=512, choices=LOF_ACTIVITY_TYPE)
    activity = models.CharField(max_length=512)
    participants = models.TextField()

    venue = models.CharField(max_length=512)
    requirements = models.TextField()
    remarks = models.TextField(null=True, blank=True)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/lsdb/%Y/%m/'))

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Logistics Officers Forum'
        verbose_name_plural = 'Logistics Officers Forum'

    def __str__(self):
        return self.activity

class LogisticsOfficersForumPhoto(models.Model):
    remarks = models.TextField()
    activity = models.ForeignKey(LogisticsOfficersForumActivity, models.DO_NOTHING, related_name='lof_photos')
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/lsdb/%Y/%m/'))

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'

class LogisticsOfficersForumActivityReport(models.Model):
    title = models.CharField(max_length=512)
    activity = models.ForeignKey(LogisticsOfficersForumActivity, models.DO_NOTHING, related_name='lof_activity_reports')
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/lsdb/%Y/%m/'))

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'After Activity Report'
        verbose_name_plural = 'After Activity Reports'

    def __str__(self):
            return self.title
class LogisticsStaffVisit(models.Model):
    activity = models.CharField(max_length=512)
    venue = models.CharField(max_length=512, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/lsdb/%Y/%m/'))

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Logistics Staff Visit'
        verbose_name_plural = 'Logistics Staff Visits'

    def __str__(self):
        return self.activity

class LogisticsStaffVisitPhoto(models.Model):
    remarks = models.TextField()
    activity = models.ForeignKey(LogisticsStaffVisit, models.DO_NOTHING, related_name='lsv_photos')
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/lsdb/%Y/%m/'))

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'

class LogisticsStaffVisitReport(models.Model):
    title = models.CharField(max_length=512)
    activity = models.ForeignKey(LogisticsOfficersForumActivity, models.DO_NOTHING, related_name='lsv_activity_reports')
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/lsdb/%Y/%m/'))

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'After Activity Report'
        verbose_name_plural = 'After Activity Reports'

    def __str__(self):
            return self.title

class ATRStrategicPrograms(models.Model):
    program_name = models.CharField(max_length=512)
    review_type = models.CharField(max_length=512, choices=ATR_REVIEW_TYPE)
    
    remarks = models.TextField(null=True, blank=True)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/lsdb/%Y/%m/'))

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'ATR Strategic Program'
        verbose_name_plural = 'ATR Strategic Programs'


    def __str__(self):
        return self.program_name

class CourseApplicationProcedure(models.Model):
    course = models.CharField(max_length=512)
    
    remarks = models.TextField(null=True, blank=True)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/lsdb/%Y/%m/'))

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Course Application Procedure'
        verbose_name_plural = 'Course Application Procedures'


    def __str__(self):
        return self.course

class ApprovedResolutionsCourse(models.Model):
    course = models.CharField(max_length=512)
    venue_school = models.CharField(max_length=512)
    rank_requirement = models.CharField(max_length=512)
    slot = models.IntegerField()
    report_date = models.DateField()
    end_date = models.DateField()
    
    remarks = models.TextField(null=True, blank=True)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/lsdb/%Y/%m/'))

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Course Approved Resolution'
        verbose_name_plural = 'Course Approved Resolutions'


    def __str__(self):
        return self.course
        
class LogisticsSchooling(models.Model):
    course = models.CharField(max_length=512)
    category = models.CharField(max_length=50, choices=SCHOOLING_CATEGORY)
    venue_school = models.CharField(max_length=512)
    rank_requirement = models.CharField(max_length=512)
    slot = models.IntegerField()
    report_date = models.DateField()
    end_date = models.DateField()
    
    remarks = models.TextField(null=True, blank=True)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/lsdb/%Y/%m/'))

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Logistics Schooling'
        verbose_name_plural = 'Logistics Schooling'


    def __str__(self):
        return self.course

class ExecomPropertyAccountabilityPersonnel(models.Model):
    first_name = models.CharField(max_length=512)
    last_name = models.CharField(max_length=512)
    middle_name = models.CharField(max_length=512)

    unit = models.CharField(max_length=512, null=True, blank=True)
    
    remarks = models.TextField(null=True, blank=True)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/lsdb/%Y/%m/'))

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'EXECOM For Property Accountability'
        verbose_name_plural = 'EXECOM For Property Accountability'


    def __str__(self):
        return "{},{},{}".format(self.last_name, self.first_name, self.middle_name)

class SurveyBoard(models.Model):
    subject = models.CharField(max_length=512)
    doc_type = models.CharField(max_length=512, choices=SURVEY_BOARD_DOC_TYPE)
    date = models.DateField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/lsdb/%Y/%m/'))

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Survey Board'
        verbose_name_plural = 'Survey Board'


    def __str__(self):
        return self.subject

class LogisticsReference(models.Model):
    title = models.CharField(max_length=512)
    reference_type = models.CharField(max_length=512, choices=REFERENCES_TYPE)
    year = models.PositiveIntegerField()
    branch = models.CharField(max_length=100,null=True, blank=True)
    code = models.CharField(max_length=512, null=True, blank=True)
    date_promulgated = models.DateField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/lsdb/%Y/%m/'))

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Logistics Reference'


    def __str__(self):
        return self.title

class CoaFindingsAOM(models.Model):
    title = models.CharField(max_length=512)
    aom_number = models.CharField(max_length=512)
    date = models.DateField()
    year = models.PositiveIntegerField()   
    remarks = models.TextField(null=True, blank=True)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/lsdb/%Y/%m/'))

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'COA Findings AOM'
        verbose_name_plural = 'COA Findings AOM'

    def __str__(self):
        return self.title

class CoaFindingsCAAR(models.Model):
    title = models.CharField(max_length=512)
    date = models.DateField()
    year = models.PositiveIntegerField()   
    remarks = models.TextField(null=True, blank=True)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/lsdb/%Y/%m/'))

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'COA Findings CAR'
        verbose_name_plural = 'COA Findings CAR'

    def __str__(self):
        return self.title

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
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/lsdb/%Y/%m/'))


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
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/lsdb/%Y/%m/'))


    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Outgoing Communication'
        
    def __str__(self):
        return self.subject
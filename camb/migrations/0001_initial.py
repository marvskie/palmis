# Generated by Django 2.2.3 on 2021-09-28 08:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DASProjects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=512)),
                ('abc', models.FloatField()),
                ('quality', models.FloatField()),
                ('supplier', models.TextField()),
                ('contract_price', models.FloatField()),
                ('twg_name', models.CharField(max_length=512)),
                ('contact_details', models.TextField()),
                ('summary_file', models.FileField(upload_to=utils.PathAndRename('uploads/camb/%Y/%m/'))),
                ('action', models.CharField(max_length=512)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'DAS Project',
            },
        ),
        migrations.CreateModel(
            name='DASProjectStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('abc', models.FloatField()),
                ('twg', models.CharField(max_length=512)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('das_project', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='camb.DASProjects')),
                ('updated_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'DAS Project Status',
                'verbose_name_plural': 'DAS Project Status',
            },
        ),
        migrations.CreateModel(
            name='SRDPProjects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=512)),
                ('abc', models.FloatField()),
                ('quality', models.FloatField()),
                ('supplier', models.TextField()),
                ('contract_price', models.FloatField()),
                ('twg_name', models.CharField(max_length=512)),
                ('contact_details', models.TextField()),
                ('status', models.CharField(max_length=512)),
                ('summary_file', models.FileField(upload_to=utils.PathAndRename('uploads/camb/%Y/%m/'))),
                ('action', models.CharField(max_length=512)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'SRDP Project',
            },
        ),
        migrations.CreateModel(
            name='SRDPProjectFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=512)),
                ('file_attachment', models.FileField(upload_to=utils.PathAndRename('uploads/camb/%Y/%m/'))),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('srdp_project', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='srdp_project_files', to='camb.SRDPProjects')),
                ('updated_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'SRDP Related Files',
                'verbose_name_plural': 'SRDP Related Files',
            },
        ),
        migrations.CreateModel(
            name='SRDPPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity', models.CharField(max_length=512)),
                ('remarks', models.TextField()),
                ('file_attachment', models.FileField(upload_to=utils.PathAndRename('uploads/camb/%Y/%m/'))),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='srdp_project_photos', to='camb.SRDPProjects')),
                ('updated_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'SRDP Photo',
                'verbose_name_plural': 'SRDP Photos',
            },
        ),
        migrations.CreateModel(
            name='ReferencesPolicies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=512)),
                ('origin', models.CharField(max_length=512)),
                ('file_attachment', models.FileField(upload_to=utils.PathAndRename('uploads/camb/%Y/%m/'))),
                ('action', models.CharField(max_length=512)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Policies Reference',
            },
        ),
        migrations.CreateModel(
            name='ReferencesHelpfulLinks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
                ('url', models.CharField(max_length=512)),
                ('file_attachment', models.FileField(upload_to=utils.PathAndRename('uploads/camb/%Y/%m/'))),
                ('action', models.CharField(max_length=512)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Helpful Link',
            },
        ),
        migrations.CreateModel(
            name='ReferencesDefenseExhibits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
                ('url', models.CharField(max_length=512)),
                ('file_attachment', models.FileField(upload_to=utils.PathAndRename('uploads/camb/%Y/%m/'))),
                ('action', models.CharField(max_length=512)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Defence Exhibit',
            },
        ),
        migrations.CreateModel(
            name='ReferencesBrochures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=512)),
                ('type_of_commodity', models.CharField(max_length=512)),
                ('file_attachment', models.FileField(upload_to=utils.PathAndRename('uploads/camb/%Y/%m/'))),
                ('action', models.CharField(max_length=512)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Brochures Reference',
            },
        ),
        migrations.CreateModel(
            name='OutgoingCommunication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commo_type', models.CharField(max_length=512)),
                ('number', models.CharField(max_length=512)),
                ('control_number', models.CharField(max_length=512)),
                ('origin_branch_office_unit', models.CharField(max_length=512)),
                ('subject', models.CharField(max_length=512)),
                ('recepient_unit', models.CharField(max_length=512)),
                ('date_received', models.DateTimeField()),
                ('remarks', models.CharField(max_length=512)),
                ('received_by', models.CharField(max_length=512)),
                ('action', models.CharField(max_length=512)),
                ('file_attachment', models.FileField(upload_to=utils.PathAndRename('uploads/camb/%Y/%m/'))),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Outgoing Communication',
            },
        ),
        migrations.CreateModel(
            name='InternationalLogisticsActivities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity', models.CharField(max_length=512)),
                ('date', models.DateField()),
                ('description', models.TextField()),
                ('status', models.CharField(max_length=512)),
                ('file_attachment', models.FileField(upload_to=utils.PathAndRename('uploads/camb/%Y/%m/'))),
                ('action', models.CharField(max_length=512)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'International Logistics Activity',
                'verbose_name_plural': 'International Logistics Activities',
            },
        ),
        migrations.CreateModel(
            name='IncomingCommunication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_branch', models.CharField(max_length=512)),
                ('commo_type', models.CharField(max_length=512)),
                ('number', models.CharField(max_length=512)),
                ('control_number', models.CharField(max_length=512)),
                ('date_received', models.DateTimeField()),
                ('unit_office', models.CharField(max_length=512)),
                ('subject', models.CharField(max_length=512)),
                ('remarks', models.CharField(max_length=512)),
                ('received_by', models.CharField(max_length=512)),
                ('action', models.CharField(max_length=512)),
                ('file_attachment', models.FileField(upload_to=utils.PathAndRename('uploads/camb/%Y/%m/'))),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Incoming Communication',
            },
        ),
        migrations.CreateModel(
            name='FMSProjects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=512)),
                ('fms_case', models.CharField(max_length=512)),
                ('quality', models.FloatField()),
                ('date_loa_accepted', models.DateTimeField()),
                ('status', models.CharField(max_length=512)),
                ('summary', models.TextField()),
                ('action', models.CharField(max_length=512)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'FMS Project',
            },
        ),
        migrations.CreateModel(
            name='FMSPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity', models.CharField(max_length=512)),
                ('remarks', models.TextField()),
                ('file_attachment', models.FileField(upload_to=utils.PathAndRename('uploads/camb/%Y/%m/'))),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='fms_project_photos', to='camb.FMSProjects')),
                ('updated_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'FMS Photo',
                'verbose_name_plural': 'FMS Photos',
            },
        ),
        migrations.CreateModel(
            name='DraftDocuments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=512)),
                ('filesize', models.FloatField()),
                ('file_type', models.CharField(max_length=512)),
                ('file_attachment', models.FileField(upload_to=utils.PathAndRename('uploads/camb/%Y/%m/'))),
                ('action', models.CharField(max_length=512)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Draft Document',
            },
        ),
        migrations.CreateModel(
            name='DASProjectStatusProcurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_phase', models.CharField(choices=[('Acquisition Planning', 'Acquisition Planning'), ('Procurement', 'Procurement'), ('Contract Finalizing', 'Contract Finalizing'), ('Contract Implementation', 'Contract Implementation')], max_length=512)),
                ('project_name', models.CharField(max_length=512)),
                ('preliminary_discussion', models.CharField(max_length=512)),
                ('pre_proc', models.CharField(max_length=512)),
                ('invitation_to_bid', models.CharField(max_length=512)),
                ('pre_bid', models.CharField(max_length=512)),
                ('sobe', models.CharField(max_length=512)),
                ('post_qualification', models.CharField(max_length=512)),
                ('noa', models.CharField(max_length=512)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('das_project_status', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='das_project_procurement_phase', to='camb.DASProjectStatus')),
                ('updated_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Procurement Phase',
                'verbose_name_plural': 'Procurement Phase',
            },
        ),
        migrations.CreateModel(
            name='DASProjectStatusContractImplementation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_phase', models.CharField(choices=[('Acquisition Planning', 'Acquisition Planning'), ('Procurement', 'Procurement'), ('Contract Finalizing', 'Contract Finalizing'), ('Contract Implementation', 'Contract Implementation')], max_length=512)),
                ('project_name', models.CharField(max_length=512)),
                ('issuance_of_nca', models.CharField(max_length=512)),
                ('opening_of_lc_fund_transfer', models.CharField(max_length=512)),
                ('conduct_of_pdi', models.CharField(max_length=512)),
                ('delivery', models.CharField(max_length=512)),
                ('tiac', models.CharField(max_length=512)),
                ('completed', models.CharField(max_length=512)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('das_project_status', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='das_project_contract_implementation_phase', to='camb.DASProjectStatus')),
                ('updated_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Contract Implementation Phase',
                'verbose_name_plural': 'Contract Implementation Phase',
            },
        ),
        migrations.CreateModel(
            name='DASProjectStatusContractFinalization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_phase', models.CharField(choices=[('Acquisition Planning', 'Acquisition Planning'), ('Procurement', 'Procurement'), ('Contract Finalizing', 'Contract Finalizing'), ('Contract Implementation', 'Contract Implementation')], max_length=512)),
                ('project_name', models.CharField(max_length=512)),
                ('contract_preparation', models.CharField(max_length=512)),
                ('atr', models.CharField(max_length=512)),
                ('aa', models.CharField(max_length=512)),
                ('obr', models.CharField(max_length=512)),
                ('caf', models.CharField(max_length=512)),
                ('tjag_opinion', models.CharField(max_length=512)),
                ('csafp_approval', models.CharField(max_length=512)),
                ('snd_approval', models.CharField(max_length=512)),
                ('ntp', models.CharField(max_length=512)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('das_project_status', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='das_project_contract_finalization_phase', to='camb.DASProjectStatus')),
                ('updated_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Contract Finalization Phase',
                'verbose_name_plural': 'Contract Finalization Phase',
            },
        ),
        migrations.CreateModel(
            name='DASProjectStatusAcquisition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_phase', models.CharField(choices=[('Acquisition Planning', 'Acquisition Planning'), ('Procurement', 'Procurement'), ('Contract Finalizing', 'Contract Finalizing'), ('Contract Implementation', 'Contract Implementation')], max_length=512)),
                ('project_name', models.CharField(max_length=512)),
                ('first_pass_assessment', models.CharField(max_length=512)),
                ('first_pass_pa_cdb', models.CharField(max_length=512)),
                ('first_pass_afpseo', models.CharField(max_length=512)),
                ('first_pass_das_adhoc_committee', models.CharField(max_length=512)),
                ('first_pass_afp_cdb', models.CharField(max_length=512)),
                ('first_pass_slrtd_approval', models.CharField(max_length=512)),
                ('first_pass_apm', models.CharField(max_length=512)),
                ('second_pass_assessment', models.CharField(max_length=512)),
                ('second_pass_pa_cdb', models.CharField(max_length=512)),
                ('second_pass_afpseo', models.CharField(max_length=512)),
                ('second_pass_das_adhoc_committee', models.CharField(max_length=512)),
                ('second_pass_afp_cdb', models.CharField(max_length=512)),
                ('second_pass_slrtd_approval', models.CharField(max_length=512)),
                ('second_pass_submission_of_decision_package', models.CharField(max_length=512)),
                ('second_pass_apm', models.CharField(max_length=512)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('das_project_status', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='das_project_acquisition_phase', to='camb.DASProjectStatus')),
                ('updated_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Acquisition Phase',
                'verbose_name_plural': 'Acquisition Phase',
            },
        ),
        migrations.CreateModel(
            name='DASProjectFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=512)),
                ('file_attachment', models.FileField(upload_to=utils.PathAndRename('uploads/camb/%Y/%m/'))),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('das_project', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='das_project_files', to='camb.DASProjects')),
                ('updated_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'DAS Related Files',
                'verbose_name_plural': 'DAS Related Files',
            },
        ),
        migrations.CreateModel(
            name='DASPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity', models.CharField(max_length=512)),
                ('remarks', models.TextField()),
                ('file_attachment', models.FileField(upload_to=utils.PathAndRename('uploads/camb/%Y/%m/'))),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='das_project_photos', to='camb.DASProjects')),
                ('updated_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'DAS Photo',
                'verbose_name_plural': 'DAS Photos',
            },
        ),
    ]
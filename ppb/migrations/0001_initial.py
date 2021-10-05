# Generated by Django 2.2.3 on 2021-09-07 19:06

import datetime
from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import ppb.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('commons', '0002_auto_20201208_0512'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dpg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'DPG',
            },
        ),
        migrations.CreateModel(
            name='ExpenseClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=4, unique=True)),
                ('name', models.CharField(max_length=64)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Expense classes',
            },
        ),
        migrations.CreateModel(
            name='FundRelease',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('rrf_no', models.CharField(default=ppb.models.random_init, max_length=32, unique=True)),
                ('serial', models.PositiveIntegerField(default=0)),
                ('reference', models.TextField(null=True)),
                ('footer_control', models.CharField(max_length=16)),
                ('other_budget', models.CharField(blank=True, max_length=128, null=True)),
                ('cmd', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Fund Release (RRF)',
                'verbose_name_plural': 'Fund Releases (RRF)',
            },
        ),
        migrations.CreateModel(
            name='FundReleaseAsa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('advice_no', models.CharField(max_length=32)),
                ('date_released', models.DateField()),
                ('purpose', models.TextField()),
                ('is_withdrawal', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('fund_releases', models.ManyToManyField(blank=True, to='ppb.FundRelease')),
                ('servicing_mfo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='commons.Pamu')),
                ('unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='commons.Unit')),
                ('updated_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'ASA',
                'verbose_name_plural': 'ASA',
            },
        ),
        migrations.CreateModel(
            name='FundReleaseItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('program', models.CharField(choices=[('FS', 'Force Sustainment'), ('FD', 'Force Development'), ('FLSS', 'Force Level Support Services'), ('GAS', 'General Administration & Support')], max_length=8)),
                ('q1', models.BooleanField(default=False)),
                ('q2', models.BooleanField(default=False)),
                ('q3', models.BooleanField(default=False)),
                ('q4', models.BooleanField(default=False)),
                ('specific_purpose', models.TextField()),
                ('realignment_level1', models.BooleanField(default=False)),
                ('realignment_level2', models.BooleanField(default=False)),
                ('fund_release', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='release_items', to='ppb.FundRelease')),
            ],
        ),
        migrations.CreateModel(
            name='FundSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='KeyProgram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=64, unique=True)),
                ('name', models.CharField(max_length=256)),
                ('order', models.PositiveIntegerField(default=100)),
            ],
        ),
        migrations.CreateModel(
            name='Kma',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('code', models.CharField(max_length=8)),
            ],
            options={
                'verbose_name': 'KMA',
            },
        ),
        migrations.CreateModel(
            name='MajorPap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('expenditure_program', models.CharField(choices=[('OPS', 'OPERATIONS'), ('GAS', 'GAS')], max_length=8)),
                ('pa_program', models.CharField(choices=[('LFP', 'Land Forces Program'), ('GAS', 'General Administration & Support')], max_length=8, verbose_name='PA Program (1L)')),
                ('pa_sub_program', models.CharField(choices=[('FS', 'Force Sustainment'), ('FD', 'Force Development'), ('FLSS', 'Force Level Support Services'), ('GAS', 'General Administration & Support')], max_length=8, verbose_name='PA Sub-program (2L)')),
                ('pa_function', models.CharField(choices=[('DEV', 'Develop'), ('ORG', 'Organize'), ('TRN', 'Train'), ('EQP', 'Equip'), ('SUP', 'Support Service'), ('SUS', 'Sustain'), ('GMS', 'General Management & Supervision')], max_length=8, verbose_name='PA Function (3L)')),
                ('fixed_cost', models.BooleanField(default=False)),
                ('kma', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ppb.Kma')),
            ],
            options={
                'verbose_name': 'PAP - 4L Major',
                'verbose_name_plural': 'PAP - 4L Major',
            },
        ),
        migrations.CreateModel(
            name='MissionArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mission_area_group', models.CharField(choices=[('EDM', 'External Defense Mission'), ('IDM', 'Internal Defense Mission')], max_length=4)),
                ('name', models.CharField(max_length=64)),
                ('code', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='ObjectCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255, null=True)),
                ('expense_class', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='object_codes', to='ppb.ExpenseClass')),
            ],
        ),
        migrations.CreateModel(
            name='Pawaf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveIntegerField()),
                ('ceiling', models.FloatField()),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Budget Record',
            },
        ),
        migrations.CreateModel(
            name='PawafItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specific_pap', models.CharField(max_length=256)),
                ('branch', models.CharField(max_length=8)),
                ('is_mandatory', models.BooleanField(default=False)),
                ('notes', models.TextField(blank=True, null=True)),
                ('amount_q1', models.FloatField(default=0.0)),
                ('amount_q2', models.FloatField(default=0.0)),
                ('amount_q3', models.FloatField(default=0.0)),
                ('amount_q4', models.FloatField(default=0.0)),
                ('amount', models.FloatField(default=0.0)),
                ('physical_target_q1', models.PositiveIntegerField(default=0)),
                ('physical_target_q2', models.PositiveIntegerField(default=0)),
                ('physical_target_q3', models.PositiveIntegerField(default=0)),
                ('physical_target_q4', models.PositiveIntegerField(default=0)),
                ('physical_target', models.PositiveIntegerField(default=0)),
                ('chargeability_distribution', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'PAWAF Item',
            },
        ),
        migrations.CreateModel(
            name='PawafItemView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=64)),
                ('order', models.PositiveIntegerField(default=100)),
                ('field_ref', models.CharField(max_length=128)),
                ('field_label', models.CharField(max_length=128)),
                ('header_label', models.CharField(max_length=128)),
                ('boolean_label', models.CharField(blank=True, max_length=128, null=True)),
                ('exclude_empty', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=32, unique=True)),
                ('name', models.CharField(max_length=64)),
                ('order', models.PositiveIntegerField(default=100)),
            ],
            options={
                'verbose_name_plural': 'Statuses',
            },
        ),
        migrations.CreateModel(
            name='StrategicObjective',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='StrategicProgram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('code', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='SubPap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('major_pap', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ppb.MajorPap')),
            ],
            options={
                'verbose_name': 'PAP - 5L Sub',
                'verbose_name_plural': 'PAP - 5L Sub',
            },
        ),
        migrations.CreateModel(
            name='SuggestedPap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('sub_pap', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ppb.SubPap')),
            ],
            options={
                'verbose_name': 'PAP - 6L Suggested',
                'verbose_name_plural': 'PAP - 6L Suggested',
            },
        ),
        migrations.CreateModel(
            name='ProgramObjective',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('dpg', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='program_objectives', to='ppb.Dpg')),
            ],
        ),
        migrations.CreateModel(
            name='PbdgObjective',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('strategic_objective', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pbdg_objectives', to='ppb.StrategicObjective')),
            ],
            options={
                'verbose_name': 'PBDG objective',
            },
        ),
        migrations.CreateModel(
            name='PawafItemEndUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('servicing_mfo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='commons.Pamu')),
            ],
        ),
        migrations.CreateModel(
            name='PawafItemBudgetBreakdown',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_q1', models.FloatField(default=0.0)),
                ('amount_q2', models.FloatField(default=0.0)),
                ('amount_q3', models.FloatField(default=0.0)),
                ('amount_q4', models.FloatField(default=0.0)),
                ('physical_target_q1', models.PositiveIntegerField(default=0)),
                ('physical_target_q2', models.PositiveIntegerField(default=0)),
                ('physical_target_q3', models.PositiveIntegerField(default=0)),
                ('physical_target_q4', models.PositiveIntegerField(default=0)),
                ('amount', models.FloatField(default=0.0)),
                ('physical_target', models.PositiveIntegerField(default=0)),
                ('object_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ppb.ObjectCode')),
                ('pawaf_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='budget_breakdown', to='ppb.PawafItem')),
                ('procurement_mode', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='commons.ProcurementMode')),
            ],
        ),
        migrations.AddField(
            model_name='pawafitem',
            name='end_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ppb.PawafItemEndUser'),
        ),
        migrations.AddField(
            model_name='pawafitem',
            name='expense_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ppb.ExpenseClass'),
        ),
        migrations.AddField(
            model_name='pawafitem',
            name='key_program',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ppb.KeyProgram'),
        ),
        migrations.AddField(
            model_name='pawafitem',
            name='mission_area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ppb.MissionArea'),
        ),
        migrations.AddField(
            model_name='pawafitem',
            name='pawaf',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pawaf_items', to='ppb.Pawaf'),
        ),
        migrations.AddField(
            model_name='pawafitem',
            name='pbdg_objective',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ppb.PbdgObjective'),
        ),
        migrations.AddField(
            model_name='pawafitem',
            name='program_objective',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='pawaf_items', to='ppb.ProgramObjective'),
        ),
        migrations.AddField(
            model_name='pawafitem',
            name='strategic_program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ppb.StrategicProgram'),
        ),
        migrations.AddField(
            model_name='pawafitem',
            name='suggested_pap',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ppb.SuggestedPap'),
        ),
        migrations.CreateModel(
            name='FundReleaseSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('charged_q1', models.FloatField(default=0.0)),
                ('charged_q2', models.FloatField(default=0.0)),
                ('charged_q3', models.FloatField(default=0.0)),
                ('charged_q4', models.FloatField(default=0.0)),
                ('charged_amount', models.FloatField(default=0.0)),
                ('fund_release_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='release_sources', to='ppb.FundReleaseItem')),
                ('fund_source', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='release_sources', to='ppb.PawafItemBudgetBreakdown')),
            ],
        ),
        migrations.CreateModel(
            name='FundReleaseRecipient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0.0)),
                ('fund_release_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='release_recipients', to='ppb.FundReleaseItem')),
                ('servicing_mfo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='commons.Pamu')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='commons.Unit')),
            ],
        ),
        migrations.AddField(
            model_name='fundreleaseitem',
            name='mission_area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ppb.MissionArea'),
        ),
        migrations.AddField(
            model_name='fundreleaseitem',
            name='object_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ppb.ObjectCode'),
        ),
        migrations.CreateModel(
            name='FundReleaseAsaItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0)),
                ('asa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asa_items', to='ppb.FundReleaseAsa')),
                ('release_item', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='asa_items', to='ppb.FundReleaseItem')),
            ],
        ),
        migrations.AddField(
            model_name='fundrelease',
            name='budget',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ppb.Pawaf'),
        ),
        migrations.AddField(
            model_name='fundrelease',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='fundrelease',
            name='specific_paps',
            field=models.ManyToManyField(blank=True, to='ppb.PawafItem'),
        ),
        migrations.AddField(
            model_name='fundrelease',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ppb.Status'),
        ),
        migrations.AddField(
            model_name='fundrelease',
            name='updated_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dpg',
            name='mission_area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ppb.MissionArea'),
        ),
    ]

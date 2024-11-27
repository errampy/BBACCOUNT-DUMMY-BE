# Generated by Django 5.0 on 2024-11-26 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LeaveManagementAudit',
            fields=[
                ('code', models.CharField(max_length=50)),
                ('pending_leave_requests', models.PositiveIntegerField()),
                ('total_leave_days_taken', models.PositiveIntegerField()),
                ('average_leave_days_per_staff', models.FloatField()),
                ('highest_leave_days', models.PositiveIntegerField(blank=True, null=True)),
                ('lowest_leave_days', models.PositiveIntegerField(blank=True, null=True)),
                ('reported_date', models.DateField(default='now,')),
                ('leave_trends', models.TextField()),
                ('leave_policy_notes', models.TextField()),
                ('custom_record_id', models.CharField(editable=False, max_length=50, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('created', 'Created'), ('updated', 'Updated'), ('deleted', 'Deleted'), ('in_temp', 'In Temp')], default='in_temp', max_length=7)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LeaveManagementHistory',
            fields=[
                ('code', models.CharField(max_length=50)),
                ('pending_leave_requests', models.PositiveIntegerField()),
                ('total_leave_days_taken', models.PositiveIntegerField()),
                ('average_leave_days_per_staff', models.FloatField()),
                ('highest_leave_days', models.PositiveIntegerField(blank=True, null=True)),
                ('lowest_leave_days', models.PositiveIntegerField(blank=True, null=True)),
                ('reported_date', models.DateField(default='now,')),
                ('leave_trends', models.TextField()),
                ('leave_policy_notes', models.TextField()),
                ('custom_record_id', models.CharField(editable=False, max_length=50, primary_key=True, serialize=False)),
                ('version', models.PositiveIntegerField()),
                ('is_deactivate', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LeaveManagementLive',
            fields=[
                ('pending_leave_requests', models.PositiveIntegerField()),
                ('total_leave_days_taken', models.PositiveIntegerField()),
                ('average_leave_days_per_staff', models.FloatField()),
                ('highest_leave_days', models.PositiveIntegerField(blank=True, null=True)),
                ('lowest_leave_days', models.PositiveIntegerField(blank=True, null=True)),
                ('reported_date', models.DateField(default='now,')),
                ('leave_trends', models.TextField()),
                ('leave_policy_notes', models.TextField()),
                ('code', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('is_deactivate', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LeaveManagementTemp',
            fields=[
                ('pending_leave_requests', models.PositiveIntegerField()),
                ('total_leave_days_taken', models.PositiveIntegerField()),
                ('average_leave_days_per_staff', models.FloatField()),
                ('highest_leave_days', models.PositiveIntegerField(blank=True, null=True)),
                ('lowest_leave_days', models.PositiveIntegerField(blank=True, null=True)),
                ('reported_date', models.DateField(default='now,')),
                ('leave_trends', models.TextField()),
                ('leave_policy_notes', models.TextField()),
                ('code', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('unauthorized', 'Un Authorized'), ('unauthorized_sent', 'Un Authorized Send'), ('unauthorized_return', 'Un Authorized Return')], default='unauthorized', max_length=20)),
                ('notes', models.TextField(blank=True, null=True)),
                ('record_type', models.CharField(choices=[('create', 'Create'), ('update', 'Update'), ('delete', 'Delete')], max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StaffProductivityAudit',
            fields=[
                ('code', models.CharField(max_length=50)),
                ('total_loan_officers', models.PositiveIntegerField()),
                ('loans_per_officer', models.PositiveIntegerField()),
                ('average_portfolio_per_officer', models.FloatField()),
                ('total_loans', models.PositiveIntegerField()),
                ('highest_loans_by_officer', models.PositiveIntegerField(blank=True, null=True)),
                ('reported_date', models.DateField(default='now,')),
                ('lowest_loans_by_officer', models.PositiveIntegerField(blank=True, null=True)),
                ('performance_comments', models.TextField()),
                ('custom_record_id', models.CharField(editable=False, max_length=50, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('created', 'Created'), ('updated', 'Updated'), ('deleted', 'Deleted'), ('in_temp', 'In Temp')], default='in_temp', max_length=7)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StaffProductivityHistory',
            fields=[
                ('code', models.CharField(max_length=50)),
                ('total_loan_officers', models.PositiveIntegerField()),
                ('loans_per_officer', models.PositiveIntegerField()),
                ('average_portfolio_per_officer', models.FloatField()),
                ('total_loans', models.PositiveIntegerField()),
                ('highest_loans_by_officer', models.PositiveIntegerField(blank=True, null=True)),
                ('reported_date', models.DateField(default='now,')),
                ('lowest_loans_by_officer', models.PositiveIntegerField(blank=True, null=True)),
                ('performance_comments', models.TextField()),
                ('custom_record_id', models.CharField(editable=False, max_length=50, primary_key=True, serialize=False)),
                ('version', models.PositiveIntegerField()),
                ('is_deactivate', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StaffProductivityLive',
            fields=[
                ('total_loan_officers', models.PositiveIntegerField()),
                ('loans_per_officer', models.PositiveIntegerField()),
                ('average_portfolio_per_officer', models.FloatField()),
                ('total_loans', models.PositiveIntegerField()),
                ('highest_loans_by_officer', models.PositiveIntegerField(blank=True, null=True)),
                ('reported_date', models.DateField(default='now,')),
                ('lowest_loans_by_officer', models.PositiveIntegerField(blank=True, null=True)),
                ('performance_comments', models.TextField()),
                ('code', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('is_deactivate', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StaffProductivityTemp',
            fields=[
                ('total_loan_officers', models.PositiveIntegerField()),
                ('loans_per_officer', models.PositiveIntegerField()),
                ('average_portfolio_per_officer', models.FloatField()),
                ('total_loans', models.PositiveIntegerField()),
                ('highest_loans_by_officer', models.PositiveIntegerField(blank=True, null=True)),
                ('reported_date', models.DateField(default='now,')),
                ('lowest_loans_by_officer', models.PositiveIntegerField(blank=True, null=True)),
                ('performance_comments', models.TextField()),
                ('code', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('unauthorized', 'Un Authorized'), ('unauthorized_sent', 'Un Authorized Send'), ('unauthorized_return', 'Un Authorized Return')], default='unauthorized', max_length=20)),
                ('notes', models.TextField(blank=True, null=True)),
                ('record_type', models.CharField(choices=[('create', 'Create'), ('update', 'Update'), ('delete', 'Delete')], max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StaffTurnoverAudit',
            fields=[
                ('code', models.CharField(max_length=50)),
                ('total_departures', models.PositiveIntegerField()),
                ('total_new_hires', models.PositiveIntegerField()),
                ('turnover_rate', models.FloatField()),
                ('current_staff_count', models.PositiveIntegerField()),
                ('total_staff_at_start', models.PositiveIntegerField()),
                ('reported_date', models.DateField(default='now,')),
                ('key_departures', models.TextField()),
                ('hiring_notes', models.TextField()),
                ('custom_record_id', models.CharField(editable=False, max_length=50, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('created', 'Created'), ('updated', 'Updated'), ('deleted', 'Deleted'), ('in_temp', 'In Temp')], default='in_temp', max_length=7)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StaffTurnoverHistory',
            fields=[
                ('code', models.CharField(max_length=50)),
                ('total_departures', models.PositiveIntegerField()),
                ('total_new_hires', models.PositiveIntegerField()),
                ('turnover_rate', models.FloatField()),
                ('current_staff_count', models.PositiveIntegerField()),
                ('total_staff_at_start', models.PositiveIntegerField()),
                ('reported_date', models.DateField(default='now,')),
                ('key_departures', models.TextField()),
                ('hiring_notes', models.TextField()),
                ('custom_record_id', models.CharField(editable=False, max_length=50, primary_key=True, serialize=False)),
                ('version', models.PositiveIntegerField()),
                ('is_deactivate', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StaffTurnoverLive',
            fields=[
                ('total_departures', models.PositiveIntegerField()),
                ('total_new_hires', models.PositiveIntegerField()),
                ('turnover_rate', models.FloatField()),
                ('current_staff_count', models.PositiveIntegerField()),
                ('total_staff_at_start', models.PositiveIntegerField()),
                ('reported_date', models.DateField(default='now,')),
                ('key_departures', models.TextField()),
                ('hiring_notes', models.TextField()),
                ('code', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('is_deactivate', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StaffTurnoverTemp',
            fields=[
                ('total_departures', models.PositiveIntegerField()),
                ('total_new_hires', models.PositiveIntegerField()),
                ('turnover_rate', models.FloatField()),
                ('current_staff_count', models.PositiveIntegerField()),
                ('total_staff_at_start', models.PositiveIntegerField()),
                ('reported_date', models.DateField(default='now,')),
                ('key_departures', models.TextField()),
                ('hiring_notes', models.TextField()),
                ('code', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('unauthorized', 'Un Authorized'), ('unauthorized_sent', 'Un Authorized Send'), ('unauthorized_return', 'Un Authorized Return')], default='unauthorized', max_length=20)),
                ('notes', models.TextField(blank=True, null=True)),
                ('record_type', models.CharField(choices=[('create', 'Create'), ('update', 'Update'), ('delete', 'Delete')], max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TrainingDevelopmentAudit',
            fields=[
                ('code', models.CharField(max_length=50)),
                ('training_sessions_conducted', models.PositiveIntegerField()),
                ('staff_trained', models.PositiveIntegerField()),
                ('total_training_costs', models.FloatField()),
                ('average_training_cost_per_person', models.FloatField()),
                ('training_focus_areas', models.TextField(blank=True, null=True)),
                ('reported_date', models.DateField(default='now,')),
                ('training_feedback_summary', models.TextField(blank=True, null=True)),
                ('custom_record_id', models.CharField(editable=False, max_length=50, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('created', 'Created'), ('updated', 'Updated'), ('deleted', 'Deleted'), ('in_temp', 'In Temp')], default='in_temp', max_length=7)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TrainingDevelopmentHistory',
            fields=[
                ('code', models.CharField(max_length=50)),
                ('training_sessions_conducted', models.PositiveIntegerField()),
                ('staff_trained', models.PositiveIntegerField()),
                ('total_training_costs', models.FloatField()),
                ('average_training_cost_per_person', models.FloatField()),
                ('training_focus_areas', models.TextField(blank=True, null=True)),
                ('reported_date', models.DateField(default='now,')),
                ('training_feedback_summary', models.TextField(blank=True, null=True)),
                ('custom_record_id', models.CharField(editable=False, max_length=50, primary_key=True, serialize=False)),
                ('version', models.PositiveIntegerField()),
                ('is_deactivate', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TrainingDevelopmentLive',
            fields=[
                ('training_sessions_conducted', models.PositiveIntegerField()),
                ('staff_trained', models.PositiveIntegerField()),
                ('total_training_costs', models.FloatField()),
                ('average_training_cost_per_person', models.FloatField()),
                ('training_focus_areas', models.TextField(blank=True, null=True)),
                ('reported_date', models.DateField(default='now,')),
                ('training_feedback_summary', models.TextField(blank=True, null=True)),
                ('code', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('is_deactivate', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TrainingDevelopmentTemp',
            fields=[
                ('training_sessions_conducted', models.PositiveIntegerField()),
                ('staff_trained', models.PositiveIntegerField()),
                ('total_training_costs', models.FloatField()),
                ('average_training_cost_per_person', models.FloatField()),
                ('training_focus_areas', models.TextField(blank=True, null=True)),
                ('reported_date', models.DateField(default='now,')),
                ('training_feedback_summary', models.TextField(blank=True, null=True)),
                ('code', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('unauthorized', 'Un Authorized'), ('unauthorized_sent', 'Un Authorized Send'), ('unauthorized_return', 'Un Authorized Return')], default='unauthorized', max_length=20)),
                ('notes', models.TextField(blank=True, null=True)),
                ('record_type', models.CharField(choices=[('create', 'Create'), ('update', 'Update'), ('delete', 'Delete')], max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

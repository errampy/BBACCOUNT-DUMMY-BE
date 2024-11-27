# Generated by Django 5.0 on 2024-11-26 14:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mainapp', '0001_initial'),
        ('workflow', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='approvalrecords',
            name='approval_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approval_records_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='authorizerequest',
            name='approval_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approval_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='authorizerequest',
            name='next_approval_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approval_user_next', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='authorizerequest',
            name='sender_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='delegaterecords',
            name='delegate_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delegate_to', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='idgeneration',
            name='app_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='app_name_ig', to='mainapp.appregistration'),
        ),
        migrations.AddField(
            model_name='idgensetup',
            name='app_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='app_name_registration', to='mainapp.appregistration'),
        ),
        migrations.AddField(
            model_name='modelregistration',
            name='app_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='app_name_model_reg', to='mainapp.appregistration'),
        ),
        migrations.AddField(
            model_name='idgensetup',
            name='model_name',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='model_name_idgsu', to='mainapp.modelregistration'),
        ),
        migrations.AddField(
            model_name='idgeneration',
            name='model_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='model_name_ig', to='mainapp.modelregistration'),
        ),
        migrations.AddField(
            model_name='delegaterecords',
            name='table_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='model_name_mcd', to='mainapp.modelregistration'),
        ),
        migrations.AddField(
            model_name='authorizerequest',
            name='table_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='table_name_approval', to='mainapp.modelregistration'),
        ),
        migrations.AddField(
            model_name='approvalrecords',
            name='model_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='table_name_approval_records', to='mainapp.modelregistration'),
        ),
        migrations.AddField(
            model_name='mstomodulemapping',
            name='module_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='module_id', to='mainapp.moduleregistration'),
        ),
        migrations.AddField(
            model_name='mstomodulemapping',
            name='mservice_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ms_id', to='mainapp.msregistration'),
        ),
        migrations.AddField(
            model_name='workflowmapping',
            name='table_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='table_name_workflow_mapping', to='mainapp.modelregistration'),
        ),
        migrations.AddField(
            model_name='workflowmapping',
            name='update_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='workflow_mapping_update_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='workflowmapping',
            name='workflow',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='workflow_setup_workflow_mapping', to='workflow.workflowsetup'),
        ),
    ]

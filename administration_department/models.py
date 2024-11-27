from django.db import models
# from bb_id_gen_app.models import ModelRegistration
from .validations import *
from user_management.models import User


class OfficeExpense(models.Model):
	code = models.CharField(max_length=50)
	total_office_expenses = models.FloatField()
	top_expenses = models.TextField()
	utilities_expenses = models.FloatField()
	rent_expenses = models.FloatField()
	office_supplies_expenses = models.FloatField()
	reported_date = models.DateField(default="now," )
	employee_welfare_expenses = models.FloatField()
	maintenance_expenses = models.FloatField()
	comments = models.TextField()

	class Meta:
		abstract = True
class OfficeExpenseLive(OfficeExpense):
    code = models.CharField(max_length=50, primary_key=True)
    is_deactivate = models.BooleanField(default=False)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['category_type'], name='unique_category_type'),
    #     ]

    def __str__(self):
        return self.code


class OfficeExpenseTemp(OfficeExpense):
    code = models.CharField(max_length=50, primary_key=True)
    STATUS = (
        ('unauthorized', 'Un Authorized'),
        ('unauthorized_sent', 'Un Authorized Send'),
        ('unauthorized_return', 'Un Authorized Return'),
    )
    WORKFLOW_TYPE = (
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete')
    )
    status = models.CharField(max_length=20, choices=STATUS, default='unauthorized')
    notes = models.TextField(blank=True, null=True)
    record_type=models.CharField(max_length=20, choices=WORKFLOW_TYPE)

    def __str__(self):
        return self.code


class OfficeExpenseHistory(OfficeExpense):
    """
    unauthorized : Un Authorized me record is not moved for authorization.
    unauthorized_return : Un Authorized Return means record moved for authorization, but it is not authorized due to some
                           Reason , that reason will capture into notes fields.
    """
    custom_record_id = models.CharField(max_length=50, primary_key=True, editable=False)
    version = models.PositiveIntegerField()
    is_deactivate = models.BooleanField(default=False)

    # add if any extra fields needed

    def __str__(self):
        return self.custom_record_id


class OfficeExpenseAudit(OfficeExpense):
    # add if any extra fields needed
    custom_record_id = models.CharField(max_length=50, primary_key=True, editable=False)
    STATUS = (
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
        ('in_temp', 'In Temp')
    )
    status = models.CharField(max_length=7, choices=STATUS, default='in_temp')
    created_by = models.ForeignKey(User, related_name='OfficeExpenseAudit_created_by', on_delete=models.SET_NULL,
                                   null=True)
    updated_by = models.ForeignKey(User, related_name='OfficeExpenseAudit_updated_by', on_delete=models.SET_NULL,
                                   null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.custom_record_id

class AssetManagement(models.Model):
	code = models.CharField(max_length=50)
	total_fixed_assets = models.FloatField()
	depreciation = models.FloatField()
	maintenance_costs = models.FloatField()
	asset_utilization_rate = models.FloatField()
	repairs_and_upgrades_cost = models.FloatField()
	reported_date = models.DateField(default="now," )
	new_assets_acquired = models.FloatField()
	comments = models.TextField()

	class Meta:
		abstract = True
class AssetManagementLive(AssetManagement):
    code = models.CharField(max_length=50, primary_key=True)
    is_deactivate = models.BooleanField(default=False)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['category_type'], name='unique_category_type'),
    #     ]

    def __str__(self):
        return self.code


class AssetManagementTemp(AssetManagement):
    code = models.CharField(max_length=50, primary_key=True)
    STATUS = (
        ('unauthorized', 'Un Authorized'),
        ('unauthorized_sent', 'Un Authorized Send'),
        ('unauthorized_return', 'Un Authorized Return'),
    )
    WORKFLOW_TYPE = (
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete')
    )
    status = models.CharField(max_length=20, choices=STATUS, default='unauthorized')
    notes = models.TextField(blank=True, null=True)
    record_type=models.CharField(max_length=20, choices=WORKFLOW_TYPE)

    def __str__(self):
        return self.code


class AssetManagementHistory(AssetManagement):
    """
    unauthorized : Un Authorized me record is not moved for authorization.
    unauthorized_return : Un Authorized Return means record moved for authorization, but it is not authorized due to some
                           Reason , that reason will capture into notes fields.
    """
    custom_record_id = models.CharField(max_length=50, primary_key=True, editable=False)
    version = models.PositiveIntegerField()
    is_deactivate = models.BooleanField(default=False)

    # add if any extra fields needed

    def __str__(self):
        return self.custom_record_id


class AssetManagementAudit(AssetManagement):
    # add if any extra fields needed
    custom_record_id = models.CharField(max_length=50, primary_key=True, editable=False)
    STATUS = (
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
        ('in_temp', 'In Temp')
    )
    status = models.CharField(max_length=7, choices=STATUS, default='in_temp')
    created_by = models.ForeignKey(User, related_name='AssetManagementAudit_created_by', on_delete=models.SET_NULL,
                                   null=True)
    updated_by = models.ForeignKey(User, related_name='AssetManagementAudit_updated_by', on_delete=models.SET_NULL,
                                   null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.custom_record_id

class LogisticsAndFleetManagement(models.Model):
	code = models.CharField(max_length=50)
	total_vehicles = models.PositiveIntegerField()
	vehicles_in_use = models.PositiveIntegerField()
	fuel_costs = models.FloatField()
	maintenance_costs = models.FloatField()
	vehicle_insurance_expenses = models.FloatField()
	reported_date = models.DateField(default="now," )
	vehicle_replacement_value = models.FloatField()
	fleet_utilization_rate = models.FloatField()
	fleet_safety_compliance_rate = models.FloatField()
	vehicle_acquisition_cost = models.FloatField()
	comments = models.TextField()

	class Meta:
		abstract = True
class LogisticsAndFleetManagementLive(LogisticsAndFleetManagement):
    code = models.CharField(max_length=50, primary_key=True)
    is_deactivate = models.BooleanField(default=False)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['category_type'], name='unique_category_type'),
    #     ]

    def __str__(self):
        return self.code


class LogisticsAndFleetManagementTemp(LogisticsAndFleetManagement):
    code = models.CharField(max_length=50, primary_key=True)
    STATUS = (
        ('unauthorized', 'Un Authorized'),
        ('unauthorized_sent', 'Un Authorized Send'),
        ('unauthorized_return', 'Un Authorized Return'),
    )
    WORKFLOW_TYPE = (
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete')
    )
    status = models.CharField(max_length=20, choices=STATUS, default='unauthorized')
    notes = models.TextField(blank=True, null=True)
    record_type=models.CharField(max_length=20, choices=WORKFLOW_TYPE)

    def __str__(self):
        return self.code


class LogisticsAndFleetManagementHistory(LogisticsAndFleetManagement):
    """
    unauthorized : Un Authorized me record is not moved for authorization.
    unauthorized_return : Un Authorized Return means record moved for authorization, but it is not authorized due to some
                           Reason , that reason will capture into notes fields.
    """
    custom_record_id = models.CharField(max_length=50, primary_key=True, editable=False)
    version = models.PositiveIntegerField()
    is_deactivate = models.BooleanField(default=False)

    # add if any extra fields needed

    def __str__(self):
        return self.custom_record_id


class LogisticsAndFleetManagementAudit(LogisticsAndFleetManagement):
    # add if any extra fields needed
    custom_record_id = models.CharField(max_length=50, primary_key=True, editable=False)
    STATUS = (
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
        ('in_temp', 'In Temp')
    )
    status = models.CharField(max_length=7, choices=STATUS, default='in_temp')
    created_by = models.ForeignKey(User, related_name='LogisticsAndFleetManagementAudit_created_by', on_delete=models.SET_NULL,
                                   null=True)
    updated_by = models.ForeignKey(User, related_name='LogisticsAndFleetManagementAudit_updated_by', on_delete=models.SET_NULL,
                                   null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.custom_record_id

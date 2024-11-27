from django.db import models
# from bb_id_gen_app.models import ModelRegistration
from .validations import *
from user_management.models import User


class LeaveManagement(models.Model):
	code = models.CharField(max_length=50)
	pending_leave_requests = models.PositiveIntegerField()
	total_leave_days_taken = models.PositiveIntegerField()
	average_leave_days_per_staff = models.FloatField()
	highest_leave_days = models.PositiveIntegerField(blank=True, null=True,)
	lowest_leave_days = models.PositiveIntegerField(blank=True, null=True,)
	reported_date = models.DateField(default="now," )
	leave_trends = models.TextField()
	leave_policy_notes = models.TextField()

	class Meta:
		abstract = True
class LeaveManagementLive(LeaveManagement):
    code = models.CharField(max_length=50, primary_key=True)
    is_deactivate = models.BooleanField(default=False)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['category_type'], name='unique_category_type'),
    #     ]

    def __str__(self):
        return self.code


class LeaveManagementTemp(LeaveManagement):
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


class LeaveManagementHistory(LeaveManagement):
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


class LeaveManagementAudit(LeaveManagement):
    # add if any extra fields needed
    custom_record_id = models.CharField(max_length=50, primary_key=True, editable=False)
    STATUS = (
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
        ('in_temp', 'In Temp')
    )
    status = models.CharField(max_length=7, choices=STATUS, default='in_temp')
    created_by = models.ForeignKey(User, related_name='LeaveManagementAudit_created_by', on_delete=models.SET_NULL,
                                   null=True)
    updated_by = models.ForeignKey(User, related_name='LeaveManagementAudit_updated_by', on_delete=models.SET_NULL,
                                   null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.custom_record_id

class StaffProductivity(models.Model):
	code = models.CharField(max_length=50)
	total_loan_officers = models.PositiveIntegerField()
	loans_per_officer = models.PositiveIntegerField()
	average_portfolio_per_officer = models.FloatField()
	total_loans = models.PositiveIntegerField()
	highest_loans_by_officer = models.PositiveIntegerField(blank=True, null=True,)
	reported_date = models.DateField(default="now," )
	lowest_loans_by_officer = models.PositiveIntegerField(blank=True, null=True,)
	performance_comments = models.TextField()

	class Meta:
		abstract = True
class StaffProductivityLive(StaffProductivity):
    code = models.CharField(max_length=50, primary_key=True)
    is_deactivate = models.BooleanField(default=False)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['category_type'], name='unique_category_type'),
    #     ]

    def __str__(self):
        return self.code


class StaffProductivityTemp(StaffProductivity):
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


class StaffProductivityHistory(StaffProductivity):
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


class StaffProductivityAudit(StaffProductivity):
    # add if any extra fields needed
    custom_record_id = models.CharField(max_length=50, primary_key=True, editable=False)
    STATUS = (
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
        ('in_temp', 'In Temp')
    )
    status = models.CharField(max_length=7, choices=STATUS, default='in_temp')
    created_by = models.ForeignKey(User, related_name='StaffProductivityAudit_created_by', on_delete=models.SET_NULL,
                                   null=True)
    updated_by = models.ForeignKey(User, related_name='StaffProductivityAudit_updated_by', on_delete=models.SET_NULL,
                                   null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.custom_record_id

class TrainingDevelopment(models.Model):
	code = models.CharField(max_length=50)
	training_sessions_conducted = models.PositiveIntegerField()
	staff_trained = models.PositiveIntegerField()
	total_training_costs = models.FloatField()
	average_training_cost_per_person = models.FloatField()
	training_focus_areas = models.TextField(blank=True, null=True,)
	reported_date = models.DateField(default="now," )
	training_feedback_summary = models.TextField(blank=True, null=True,)

	class Meta:
		abstract = True
class TrainingDevelopmentLive(TrainingDevelopment):
    code = models.CharField(max_length=50, primary_key=True)
    is_deactivate = models.BooleanField(default=False)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['category_type'], name='unique_category_type'),
    #     ]

    def __str__(self):
        return self.code


class TrainingDevelopmentTemp(TrainingDevelopment):
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


class TrainingDevelopmentHistory(TrainingDevelopment):
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


class TrainingDevelopmentAudit(TrainingDevelopment):
    # add if any extra fields needed
    custom_record_id = models.CharField(max_length=50, primary_key=True, editable=False)
    STATUS = (
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
        ('in_temp', 'In Temp')
    )
    status = models.CharField(max_length=7, choices=STATUS, default='in_temp')
    created_by = models.ForeignKey(User, related_name='TrainingDevelopmentAudit_created_by', on_delete=models.SET_NULL,
                                   null=True)
    updated_by = models.ForeignKey(User, related_name='TrainingDevelopmentAudit_updated_by', on_delete=models.SET_NULL,
                                   null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.custom_record_id

class StaffTurnover(models.Model):
	code = models.CharField(max_length=50)
	total_departures = models.PositiveIntegerField()
	total_new_hires = models.PositiveIntegerField()
	turnover_rate = models.FloatField()
	current_staff_count = models.PositiveIntegerField()
	total_staff_at_start = models.PositiveIntegerField()
	reported_date = models.DateField(default="now," )
	key_departures = models.TextField()
	hiring_notes = models.TextField()

	class Meta:
		abstract = True
class StaffTurnoverLive(StaffTurnover):
    code = models.CharField(max_length=50, primary_key=True)
    is_deactivate = models.BooleanField(default=False)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['category_type'], name='unique_category_type'),
    #     ]

    def __str__(self):
        return self.code


class StaffTurnoverTemp(StaffTurnover):
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


class StaffTurnoverHistory(StaffTurnover):
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


class StaffTurnoverAudit(StaffTurnover):
    # add if any extra fields needed
    custom_record_id = models.CharField(max_length=50, primary_key=True, editable=False)
    STATUS = (
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
        ('in_temp', 'In Temp')
    )
    status = models.CharField(max_length=7, choices=STATUS, default='in_temp')
    created_by = models.ForeignKey(User, related_name='StaffTurnoverAudit_created_by', on_delete=models.SET_NULL,
                                   null=True)
    updated_by = models.ForeignKey(User, related_name='StaffTurnoverAudit_updated_by', on_delete=models.SET_NULL,
                                   null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.custom_record_id

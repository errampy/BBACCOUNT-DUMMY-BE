from django.db import models
# from bb_id_gen_app.models import ModelRegistration
from .validations import *
from user_management.models import User


class CustomerSatisfaction(models.Model):
	code = models.CharField(max_length=50)
	surveys_conducted = models.PositiveIntegerField()
	satisfaction_score = models.FloatField()
	top_complaints = models.TextField()
	net_promoter_score = models.FloatField()
	repeat_customer_percentage = models.FloatField()
	reported_date = models.DateField(default="now," )
	survey_response_rate = models.FloatField()
	comments = models.TextField()

	class Meta:
		abstract = True
class CustomerSatisfactionLive(CustomerSatisfaction):
    code = models.CharField(max_length=50, primary_key=True)
    is_deactivate = models.BooleanField(default=False)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['category_type'], name='unique_category_type'),
    #     ]

    def __str__(self):
        return self.code


class CustomerSatisfactionTemp(CustomerSatisfaction):
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


class CustomerSatisfactionHistory(CustomerSatisfaction):
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


class CustomerSatisfactionAudit(CustomerSatisfaction):
    # add if any extra fields needed
    custom_record_id = models.CharField(max_length=50, primary_key=True, editable=False)
    STATUS = (
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
        ('in_temp', 'In Temp')
    )
    status = models.CharField(max_length=7, choices=STATUS, default='in_temp')
    created_by = models.ForeignKey(User, related_name='CustomerSatisfactionAudit_created_by', on_delete=models.SET_NULL,
                                   null=True)
    updated_by = models.ForeignKey(User, related_name='CustomerSatisfactionAudit_updated_by', on_delete=models.SET_NULL,
                                   null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.custom_record_id

class ClientAcquisition(models.Model):
	code = models.CharField(max_length=50)
	new_clients = models.PositiveIntegerField()
	acquisition_cost_per_client = models.FloatField()
	total_acquisition_cost = models.FloatField()
	average_conversion_rate = models.FloatField()
	reported_date = models.DateField(default="now," )
	referral_percentage = models.FloatField()
	comments = models.TextField()

	class Meta:
		abstract = True
class ClientAcquisitionLive(ClientAcquisition):
    code = models.CharField(max_length=50, primary_key=True)
    is_deactivate = models.BooleanField(default=False)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['category_type'], name='unique_category_type'),
    #     ]

    def __str__(self):
        return self.code


class ClientAcquisitionTemp(ClientAcquisition):
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


class ClientAcquisitionHistory(ClientAcquisition):
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


class ClientAcquisitionAudit(ClientAcquisition):
    # add if any extra fields needed
    custom_record_id = models.CharField(max_length=50, primary_key=True, editable=False)
    STATUS = (
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
        ('in_temp', 'In Temp')
    )
    status = models.CharField(max_length=7, choices=STATUS, default='in_temp')
    created_by = models.ForeignKey(User, related_name='ClientAcquisitionAudit_created_by', on_delete=models.SET_NULL,
                                   null=True)
    updated_by = models.ForeignKey(User, related_name='ClientAcquisitionAudit_updated_by', on_delete=models.SET_NULL,
                                   null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.custom_record_id

class FeedbackAndComplaints(models.Model):
	code = models.CharField(max_length=50)
	total_complaints_logged = models.PositiveIntegerField()
	resolved_complaints = models.PositiveIntegerField()
	resolution_rate = models.FloatField()
	feedback_received = models.PositiveIntegerField()
	positive_feedback_percentage = models.FloatField()
	reported_date = models.DateField(default="now," )
	average_resolution_time_hours = models.FloatField()
	unresolved_complaints = models.PositiveIntegerField()
	escalation_rate = models.FloatField()
	comments = models.TextField()

	class Meta:
		abstract = True
class FeedbackAndComplaintsLive(FeedbackAndComplaints):
    code = models.CharField(max_length=50, primary_key=True)
    is_deactivate = models.BooleanField(default=False)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['category_type'], name='unique_category_type'),
    #     ]

    def __str__(self):
        return self.code


class FeedbackAndComplaintsTemp(FeedbackAndComplaints):
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


class FeedbackAndComplaintsHistory(FeedbackAndComplaints):
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


class FeedbackAndComplaintsAudit(FeedbackAndComplaints):
    # add if any extra fields needed
    custom_record_id = models.CharField(max_length=50, primary_key=True, editable=False)
    STATUS = (
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
        ('in_temp', 'In Temp')
    )
    status = models.CharField(max_length=7, choices=STATUS, default='in_temp')
    created_by = models.ForeignKey(User, related_name='FeedbackAndComplaintsAudit_created_by', on_delete=models.SET_NULL,
                                   null=True)
    updated_by = models.ForeignKey(User, related_name='FeedbackAndComplaintsAudit_updated_by', on_delete=models.SET_NULL,
                                   null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.custom_record_id

from django.db import models
# from bb_id_gen_app.models import ModelRegistration
from .validations import *
from user_management.models import User


class Compliance(models.Model):
	code = models.CharField(max_length=50)
	kyc_non_compliance_cases = models.PositiveIntegerField()
	aml_monitoring_alerts = models.PositiveIntegerField()
	penalties_incurred = models.FloatField()
	audits_conducted = models.PositiveIntegerField()
	compliance_violations = models.PositiveIntegerField()
	reported_date = models.DateField(default="now," )
	compliance_training_sessions = models.PositiveIntegerField()
	training_attendees = models.PositiveIntegerField()
	compliance_comments = models.TextField()

	class Meta:
		abstract = True
class ComplianceLive(Compliance):
    code = models.CharField(max_length=50, primary_key=True)
    is_deactivate = models.BooleanField(default=False)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['category_type'], name='unique_category_type'),
    #     ]

    def __str__(self):
        return self.code


class ComplianceTemp(Compliance):
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


class ComplianceHistory(Compliance):
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


class ComplianceAudit(Compliance):
    # add if any extra fields needed
    custom_record_id = models.CharField(max_length=50, primary_key=True, editable=False)
    STATUS = (
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
        ('in_temp', 'In Temp')
    )
    status = models.CharField(max_length=7, choices=STATUS, default='in_temp')
    created_by = models.ForeignKey(User, related_name='ComplianceAudit_created_by', on_delete=models.SET_NULL,
                                   null=True)
    updated_by = models.ForeignKey(User, related_name='ComplianceAudit_updated_by', on_delete=models.SET_NULL,
                                   null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.custom_record_id

class FraudMonitoring(models.Model):
	code = models.CharField(max_length=50)
	detected_fraud_incidents = models.PositiveIntegerField()
	total_amount_involved = models.FloatField()
	resolution_status_percentage = models.FloatField()
	open_fraud_cases = models.PositiveIntegerField()
	fraud_detection_methods = models.TextField()
	reported_date = models.DateField(default="now," )
	fraud_prevention_actions = models.TextField()
	investigation_comments = models.TextField()

	class Meta:
		abstract = True
class FraudMonitoringLive(FraudMonitoring):
    code = models.CharField(max_length=50, primary_key=True)
    is_deactivate = models.BooleanField(default=False)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['category_type'], name='unique_category_type'),
    #     ]

    def __str__(self):
        return self.code


class FraudMonitoringTemp(FraudMonitoring):
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


class FraudMonitoringHistory(FraudMonitoring):
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


class FraudMonitoringAudit(FraudMonitoring):
    # add if any extra fields needed
    custom_record_id = models.CharField(max_length=50, primary_key=True, editable=False)
    STATUS = (
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
        ('in_temp', 'In Temp')
    )
    status = models.CharField(max_length=7, choices=STATUS, default='in_temp')
    created_by = models.ForeignKey(User, related_name='FraudMonitoringAudit_created_by', on_delete=models.SET_NULL,
                                   null=True)
    updated_by = models.ForeignKey(User, related_name='FraudMonitoringAudit_updated_by', on_delete=models.SET_NULL,
                                   null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.custom_record_id

class RiskAssessment(models.Model):
	code = models.CharField(max_length=50)
	top_risks = models.TextField()
	mitigation_actions = models.TextField()
	residual_risk_level = models.FloatField()
	risk_review_frequency = models.CharField(max_length=50,)
	reported_date = models.DateField(default="now," )
	incidents_tracked = models.PositiveIntegerField()
	risk_owner = models.CharField(max_length=100,)
	risk_comments = models.TextField()

	class Meta:
		abstract = True
class RiskAssessmentLive(RiskAssessment):
    code = models.CharField(max_length=50, primary_key=True)
    is_deactivate = models.BooleanField(default=False)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['category_type'], name='unique_category_type'),
    #     ]

    def __str__(self):
        return self.code


class RiskAssessmentTemp(RiskAssessment):
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


class RiskAssessmentHistory(RiskAssessment):
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


class RiskAssessmentAudit(RiskAssessment):
    # add if any extra fields needed
    custom_record_id = models.CharField(max_length=50, primary_key=True, editable=False)
    STATUS = (
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
        ('in_temp', 'In Temp')
    )
    status = models.CharField(max_length=7, choices=STATUS, default='in_temp')
    created_by = models.ForeignKey(User, related_name='RiskAssessmentAudit_created_by', on_delete=models.SET_NULL,
                                   null=True)
    updated_by = models.ForeignKey(User, related_name='RiskAssessmentAudit_updated_by', on_delete=models.SET_NULL,
                                   null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.custom_record_id

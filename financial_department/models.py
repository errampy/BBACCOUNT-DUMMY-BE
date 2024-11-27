from django.db import models
# from bb_id_gen_app.models import ModelRegistration
from .validations import *
from user_management.models import User


class LoanLossProvision(models.Model):
	code = models.CharField(max_length=50)
	loans_at_risk = models.FloatField()
	provision_rate = models.FloatField()
	required_provisions = models.FloatField()
	loan_categories = models.TextField()
	remarks = models.TextField()
	reported_date = models.DateField(default="now," )

	class Meta:
		abstract = True
class LoanLossProvisionLive(LoanLossProvision):
    code = models.CharField(max_length=50, primary_key=True)
    is_deactivate = models.BooleanField(default=False)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['category_type'], name='unique_category_type'),
    #     ]

    def __str__(self):
        return self.code


class LoanLossProvisionTemp(LoanLossProvision):
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


class LoanLossProvisionHistory(LoanLossProvision):
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


class LoanLossProvisionAudit(LoanLossProvision):
    # add if any extra fields needed
    custom_record_id = models.CharField(max_length=50, primary_key=True, editable=False)
    STATUS = (
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
        ('in_temp', 'In Temp')
    )
    status = models.CharField(max_length=7, choices=STATUS, default='in_temp')
    created_by = models.ForeignKey(User, related_name='LoanLossProvisionAudit_created_by', on_delete=models.SET_NULL,
                                   null=True)
    updated_by = models.ForeignKey(User, related_name='LoanLossProvisionAudit_updated_by', on_delete=models.SET_NULL,
                                   null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.custom_record_id

class BalanceSheet(models.Model):
	code = models.CharField(max_length=50)
	assets = models.FloatField()
	liabilities = models.FloatField()
	equity = models.FloatField()
	asset_breakdown = models.TextField()
	liability_breakdown = models.TextField()
	reported_date = models.DateField(default="now," )

	class Meta:
		abstract = True
class BalanceSheetLive(BalanceSheet):
    code = models.CharField(max_length=50, primary_key=True)
    is_deactivate = models.BooleanField(default=False)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['category_type'], name='unique_category_type'),
    #     ]

    def __str__(self):
        return self.code


class BalanceSheetTemp(BalanceSheet):
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


class BalanceSheetHistory(BalanceSheet):
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


class BalanceSheetAudit(BalanceSheet):
    # add if any extra fields needed
    custom_record_id = models.CharField(max_length=50, primary_key=True, editable=False)
    STATUS = (
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
        ('in_temp', 'In Temp')
    )
    status = models.CharField(max_length=7, choices=STATUS, default='in_temp')
    created_by = models.ForeignKey(User, related_name='BalanceSheetAudit_created_by', on_delete=models.SET_NULL,
                                   null=True)
    updated_by = models.ForeignKey(User, related_name='BalanceSheetAudit_updated_by', on_delete=models.SET_NULL,
                                   null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.custom_record_id

class IncomeStatement(models.Model):
	code = models.CharField(max_length=50)
	revenue = models.FloatField()
	operating_expenses = models.FloatField()
	net_income = models.FloatField()
	revenue_sources = models.TextField()
	expense_breakdown = models.TextField()
	reported_date = models.DateField(default="now," )

	class Meta:
		abstract = True
class IncomeStatementLive(IncomeStatement):
    code = models.CharField(max_length=50, primary_key=True)
    is_deactivate = models.BooleanField(default=False)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['category_type'], name='unique_category_type'),
    #     ]

    def __str__(self):
        return self.code


class IncomeStatementTemp(IncomeStatement):
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


class IncomeStatementHistory(IncomeStatement):
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


class IncomeStatementAudit(IncomeStatement):
    # add if any extra fields needed
    custom_record_id = models.CharField(max_length=50, primary_key=True, editable=False)
    STATUS = (
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
        ('in_temp', 'In Temp')
    )
    status = models.CharField(max_length=7, choices=STATUS, default='in_temp')
    created_by = models.ForeignKey(User, related_name='IncomeStatementAudit_created_by', on_delete=models.SET_NULL,
                                   null=True)
    updated_by = models.ForeignKey(User, related_name='IncomeStatementAudit_updated_by', on_delete=models.SET_NULL,
                                   null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.custom_record_id

class CashFlowStatement(models.Model):
	code = models.CharField(max_length=50)
	inflows = models.FloatField()
	outflows = models.FloatField()
	net_cash_flow = models.FloatField()
	inflow_sources = models.TextField()
	outflow_categories = models.TextField()
	reported_date = models.DateField(default="now," )

	class Meta:
		abstract = True
class CashFlowStatementLive(CashFlowStatement):
    code = models.CharField(max_length=50, primary_key=True)
    is_deactivate = models.BooleanField(default=False)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['category_type'], name='unique_category_type'),
    #     ]

    def __str__(self):
        return self.code


class CashFlowStatementTemp(CashFlowStatement):
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


class CashFlowStatementHistory(CashFlowStatement):
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


class CashFlowStatementAudit(CashFlowStatement):
    # add if any extra fields needed
    custom_record_id = models.CharField(max_length=50, primary_key=True, editable=False)
    STATUS = (
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
        ('in_temp', 'In Temp')
    )
    status = models.CharField(max_length=7, choices=STATUS, default='in_temp')
    created_by = models.ForeignKey(User, related_name='CashFlowStatementAudit_created_by', on_delete=models.SET_NULL,
                                   null=True)
    updated_by = models.ForeignKey(User, related_name='CashFlowStatementAudit_updated_by', on_delete=models.SET_NULL,
                                   null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.custom_record_id

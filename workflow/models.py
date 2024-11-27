from django.db import models
from user_management.models import User



class Sequence(models.Model):
    sequence_series = models.PositiveIntegerField()
    description = models.TextField(max_length=100)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(class)s_created_by", null=True, editable=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="%(class)s_update_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.sequence_series)


class WorkflowCategory(models.Model):
    code = models.CharField(primary_key=True, editable=True, max_length=20)
    description = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(class)s_created_by", null=True, editable=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="%(class)s_update_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description
    


class WorkflowGroup(models.Model):
    code = models.CharField(primary_key=True, editable=True, max_length=20)
    description = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(class)s_created_by", null=True, editable=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="%(class)s_update_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description


class WorkflowUserGroupMapping(models.Model):
    workflow_group = models.ForeignKey(WorkflowGroup, on_delete=models.CASCADE, related_name='user_group_mappings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE, related_name='sequence_wfgm')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(class)s_created_by", null=True, editable=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="%(class)s_update_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.workflow_group} - {self.user} "


class WorkflowSetup(models.Model):
    code = models.CharField(primary_key=True, editable=True, max_length=20)
    description = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey(WorkflowCategory, on_delete=models.CASCADE, editable= True, related_name='workflow_setups')
    enabled = models.BooleanField(default=False)
    approver_type_choices = (
        ('Approver', 'Approver'),
        ('Workflow_User_Group', 'Workflow User Group')
    )
    approver_type = models.CharField(max_length=30, choices=approver_type_choices)
    approver_limit_choices = (
        ('Specific_Approver', 'Specific Approver'),
        ('Group_Approver', 'Group Approver')
    )
    approver_limit_type = models.CharField(max_length=30, choices=approver_limit_choices, blank=True, null=True)
    approver_id = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True, related_name='approver_setups')
    user_group_mapping = models.ForeignKey(WorkflowGroup,null=True,blank=True, on_delete=models.CASCADE, related_name='workflow_setups')

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(class)s_created_by", null=True, editable=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="%(class)s_update_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description


class UserApprovalLimit(models.Model):
    approval_limit_code = models.CharField(primary_key=True, editable=True, max_length=20)
    mode_type_choices = (
        ('flat', 'flat'),
        ('percentage', 'percentage')
    )
    mode = models.CharField(max_length=15, choices=mode_type_choices, blank=True, null=True)
    value = models.FloatField()
    limit_mode_choices = (
        ('daily', 'daily'),
        ('weekly', 'weekly'),
        ('monthly', 'monthly'),
    )
    limit_mode = models.CharField(max_length=20, choices=limit_mode_choices)
    limit_value = models.FloatField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='approval_limit')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(class)s_created_by", null=True, editable=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="%(class)s_update_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.approval_limit_code


class ReferenceType(models.Model):
    type_id = models.CharField(max_length=20)
    type_name = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(class)s_created_by", null=True, editable=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="%(class)s_update_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type_id


class TransactionType(models.Model):
    workflow_setup = models.ForeignKey(WorkflowSetup, on_delete=models.CASCADE, related_name='transaction_types')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(class)s_created_by", null=True, editable=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="%(class)s_update_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.workflow_setup)


class Transaction(models.Model):
    total_amount_approved = models.FloatField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(class)s_created_by", null=True, editable=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="%(class)s_update_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TransactionApprovalEntry(models.Model):
    reference_number = models.CharField(max_length=20)
    reference_type = models.ForeignKey(ReferenceType, on_delete=models.CASCADE)
    table_name = models.CharField(max_length=50)
    amount = models.FloatField()
    user_approved = models.ForeignKey(User, on_delete=models.CASCADE)
    approved_limit = models.ForeignKey(UserApprovalLimit, on_delete=models.CASCADE, related_name='approval_entries')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(class)s_created_by", null=True, editable=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="%(class)s_update_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.reference_number


class UserApprovalEntry(models.Model):
    reference_id = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_approval_entries')
    amount = models.ForeignKey(ReferenceType, on_delete=models.CASCADE, related_name='user_approved_amounts')
    approval_datetime = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(class)s_created_by", null=True, editable=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="%(class)s_update_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.reference_id

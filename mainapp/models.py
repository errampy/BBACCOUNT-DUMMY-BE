from django.db import models
#from django.contrib.auth.models import User

from user_management.models import User


# MS setup models
class MSRegistration(models.Model):
    mservice_id = models.CharField(max_length=20,primary_key=True)
    mservice_name = models.CharField(max_length=100)
    arguments = models.JSONField(null=True,blank=True)
    arguments_list = models.TextField(null=True,blank=True)
    required_parameter = models.TextField(null=True,blank=True)
    optional_parameter = models.TextField(null=True,blank=True)
    is_authenticate = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
	
    def formatted_mservice_name(self):
        # Replace underscores with spaces in mservice_name
        return self.mservice_name.replace('_', ' ')
    def __str__(self):
        return str(self.mservice_id)
    
class ModuleRegistration(models.Model):
    module_name = models.CharField(max_length=250,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def str(self):
        return str(self.module_name)

class MsToModuleMapping(models.Model):
    mservice_id = models.OneToOneField(MSRegistration,on_delete=models.CASCADE,related_name='ms_id')
    module_id = models.ForeignKey(ModuleRegistration,on_delete=models.CASCADE,related_name='module_id')

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def str(self):
        return str(self.module_id)	


class AppRegistration(models.Model):
    app_name = models.CharField(max_length=50, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.app_name)


class ModelRegistration(models.Model):
    app_name = models.ForeignKey(AppRegistration, on_delete=models.CASCADE, related_name='app_name_model_reg')
    model_name = models.CharField(max_length=100, )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.model_name)


class IdGenSetUp(models.Model):
    app_name = models.ForeignKey(AppRegistration, on_delete=models.CASCADE, related_name='app_name_registration')
    model_name = models.OneToOneField(ModelRegistration, on_delete=models.CASCADE, related_name='model_name_idgsu')
    prefix = models.CharField(max_length=10, )
    id_padding = models.PositiveIntegerField()
    SUFFIX_TYPE = (
        ('alpha_numeric', 'Alpha Numeric'),
        ('alpha', 'Alpha'),
        ('numeric', 'Numeric')
    )
    suffix_type = models.CharField(max_length=15, choices=SUFFIX_TYPE)
    suffix_length = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.prefix)


class IdGeneration(models.Model):
    app_name = models.ForeignKey(AppRegistration, on_delete=models.CASCADE, related_name='app_name_ig')
    model_name = models.ForeignKey(ModelRegistration, on_delete=models.CASCADE, related_name='model_name_ig')
    next_id = models.CharField(max_length=100, )
    current_id = models.CharField(max_length=100, )
    previous_id = models.CharField(max_length=100, )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Next Id {self.next_id} | Current Id {self.current_id} | Previous Id {self.previous_id}'


class DelegateRecords(models.Model):
    """
    This is common model for all the models to record the delegates details
    """
    # add if any extra fields needed
    custom_record_id = models.CharField(max_length=50, primary_key=True)
    table_name = models.ForeignKey(ModelRegistration, on_delete=models.CASCADE, related_name='model_name_mcd')
    delegate_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="delegate_to")

    def __str__(self):
        return self.custom_record_id


class AuthorizeRequest(models.Model):
    WORKFLOW_TYPE = (
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete')
    )
    table_name = models.ForeignKey(ModelRegistration, on_delete=models.CASCADE, related_name='table_name_approval')
    record_id = models.CharField(max_length=100)
    workflow_type = models.CharField(max_length=15, choices=WORKFLOW_TYPE,null=True,blank=True)
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_user')
    approval_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approval_user')
    next_approval_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='approval_user_next')
    is_authorized = models.BooleanField(default=False)
    is_authorized_return = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class WorkflowMapping(models.Model):
    WORKFLOW_TYPE = (
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete')
    )
    table_name = models.ForeignKey(ModelRegistration, on_delete=models.CASCADE, related_name='table_name_workflow_mapping')
    self_authorized = models.BooleanField(default=False)
    same_user_authorized = models.BooleanField(default=False)
    send_to_authorized = models.BooleanField(default=False)
    workflow = models.ForeignKey('workflow.WorkflowSetup', on_delete=models.CASCADE, related_name='workflow_setup_workflow_mapping',null=True,blank=True)
    workflow_authorize = models.BooleanField(default=False)
    workflow_type = models.CharField(max_length=15, choices=WORKFLOW_TYPE,null=True,blank=True)
    update_by = models.ForeignKey('user_management.User', on_delete=models.CASCADE, blank=True, null=True,related_name="workflow_mapping_update_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class ApprovalRecords(models.Model):
    STATUS_TYPE = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('started processing', 'Started Processing'),
    )
    model_name = models.ForeignKey(ModelRegistration, on_delete=models.CASCADE, related_name='table_name_approval_records')
    record_id = models.CharField(max_length=100)
    approval_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approval_records_user')
    status = models.CharField(max_length=40, choices=STATUS_TYPE,default='pending')
 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

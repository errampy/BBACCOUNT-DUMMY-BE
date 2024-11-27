from django.contrib import admin
from .models import *

admin.site.register(MSRegistration)
admin.site.register(ModuleRegistration)
admin.site.register(MsToModuleMapping)
admin.site.register(ModelRegistration)
admin.site.register(AppRegistration)
admin.site.register(ApprovalRecords)
admin.site.register(WorkflowMapping)
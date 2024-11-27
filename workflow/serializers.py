from rest_framework import serializers

from mainapp.models import *
from .models import *


class UserSerializer(serializers.ModelSerializer):
    roles = serializers.StringRelatedField()
    class Meta:
        model = User
        fields = "__all__"

class SequenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sequence
        fields="__all__"


class WorkflowCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowCategory
        fields = "__all__"


class WorkflowGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowGroup
        fields = "__all__"


class WorkflowUserGroupMappingSerializer(serializers.ModelSerializer):
    workflow_group=WorkflowGroupSerializer()
    user=UserSerializer()
    sequence=SequenceSerializer()
    class Meta:
        model = WorkflowUserGroupMapping
        fields = "__all__"


class WorkflowSetupSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowSetup
        fields = "__all__"


class UserApprovalLimitSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserApprovalLimit
        fields = "__all__"


class ReferenceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenceType
        fields = "__all__"


class ModelRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelRegistration
        fields = "__all__"

class WorkflowMappingSerializer(serializers.ModelSerializer):
    workflow=WorkflowSetupSerializer()
    class Meta:
        model = WorkflowMapping
        fields = "__all__"

    
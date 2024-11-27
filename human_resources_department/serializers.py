from rest_framework import serializers
from .models import *


class LeaveManagementLiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveManagementLive
        fields = "__all__"

class LeaveManagementTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveManagementTemp
        fields = "__all__"
        
class LeaveManagementLiveSerializerView(serializers.ModelSerializer):

    class Meta:
        model = LeaveManagementLive
        fields = "__all__"

class LeaveManagementTempSerializerView(serializers.ModelSerializer):

    class Meta:
        model = LeaveManagementTemp
        fields = "__all__"


class LeaveManagementTempPASerializer(serializers.ModelSerializer):

    class Meta:
        model = LeaveManagementTemp
        fields = "__all__"

class LeaveManagementLiveViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = LeaveManagementLive
        fields = "__all__"

class StaffProductivityLiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffProductivityLive
        fields = "__all__"

class StaffProductivityTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffProductivityTemp
        fields = "__all__"
        
class StaffProductivityLiveSerializerView(serializers.ModelSerializer):

    class Meta:
        model = StaffProductivityLive
        fields = "__all__"

class StaffProductivityTempSerializerView(serializers.ModelSerializer):

    class Meta:
        model = StaffProductivityTemp
        fields = "__all__"


class StaffProductivityTempPASerializer(serializers.ModelSerializer):

    class Meta:
        model = StaffProductivityTemp
        fields = "__all__"

class StaffProductivityLiveViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = StaffProductivityLive
        fields = "__all__"

class TrainingDevelopmentLiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingDevelopmentLive
        fields = "__all__"

class TrainingDevelopmentTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingDevelopmentTemp
        fields = "__all__"
        
class TrainingDevelopmentLiveSerializerView(serializers.ModelSerializer):

    class Meta:
        model = TrainingDevelopmentLive
        fields = "__all__"

class TrainingDevelopmentTempSerializerView(serializers.ModelSerializer):

    class Meta:
        model = TrainingDevelopmentTemp
        fields = "__all__"


class TrainingDevelopmentTempPASerializer(serializers.ModelSerializer):

    class Meta:
        model = TrainingDevelopmentTemp
        fields = "__all__"

class TrainingDevelopmentLiveViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrainingDevelopmentLive
        fields = "__all__"

class StaffTurnoverLiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffTurnoverLive
        fields = "__all__"

class StaffTurnoverTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffTurnoverTemp
        fields = "__all__"
        
class StaffTurnoverLiveSerializerView(serializers.ModelSerializer):

    class Meta:
        model = StaffTurnoverLive
        fields = "__all__"

class StaffTurnoverTempSerializerView(serializers.ModelSerializer):

    class Meta:
        model = StaffTurnoverTemp
        fields = "__all__"


class StaffTurnoverTempPASerializer(serializers.ModelSerializer):

    class Meta:
        model = StaffTurnoverTemp
        fields = "__all__"

class StaffTurnoverLiveViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = StaffTurnoverLive
        fields = "__all__"
from rest_framework import serializers
from .models import *


class ComplianceLiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplianceLive
        fields = "__all__"

class ComplianceTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplianceTemp
        fields = "__all__"
        
class ComplianceLiveSerializerView(serializers.ModelSerializer):

    class Meta:
        model = ComplianceLive
        fields = "__all__"

class ComplianceTempSerializerView(serializers.ModelSerializer):

    class Meta:
        model = ComplianceTemp
        fields = "__all__"


class ComplianceTempPASerializer(serializers.ModelSerializer):

    class Meta:
        model = ComplianceTemp
        fields = "__all__"

class ComplianceLiveViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ComplianceLive
        fields = "__all__"

class FraudMonitoringLiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = FraudMonitoringLive
        fields = "__all__"

class FraudMonitoringTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = FraudMonitoringTemp
        fields = "__all__"
        
class FraudMonitoringLiveSerializerView(serializers.ModelSerializer):

    class Meta:
        model = FraudMonitoringLive
        fields = "__all__"

class FraudMonitoringTempSerializerView(serializers.ModelSerializer):

    class Meta:
        model = FraudMonitoringTemp
        fields = "__all__"


class FraudMonitoringTempPASerializer(serializers.ModelSerializer):

    class Meta:
        model = FraudMonitoringTemp
        fields = "__all__"

class FraudMonitoringLiveViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = FraudMonitoringLive
        fields = "__all__"

class RiskAssessmentLiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskAssessmentLive
        fields = "__all__"

class RiskAssessmentTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskAssessmentTemp
        fields = "__all__"
        
class RiskAssessmentLiveSerializerView(serializers.ModelSerializer):

    class Meta:
        model = RiskAssessmentLive
        fields = "__all__"

class RiskAssessmentTempSerializerView(serializers.ModelSerializer):

    class Meta:
        model = RiskAssessmentTemp
        fields = "__all__"


class RiskAssessmentTempPASerializer(serializers.ModelSerializer):

    class Meta:
        model = RiskAssessmentTemp
        fields = "__all__"

class RiskAssessmentLiveViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = RiskAssessmentLive
        fields = "__all__"
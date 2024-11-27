from rest_framework import serializers
from .models import *


class LoanDisbursementLiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanDisbursementLive
        fields = "__all__"

class LoanDisbursementTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanDisbursementTemp
        fields = "__all__"
        
class LoanDisbursementLiveSerializerView(serializers.ModelSerializer):

    class Meta:
        model = LoanDisbursementLive
        fields = "__all__"

class LoanDisbursementTempSerializerView(serializers.ModelSerializer):

    class Meta:
        model = LoanDisbursementTemp
        fields = "__all__"


class LoanDisbursementTempPASerializer(serializers.ModelSerializer):

    class Meta:
        model = LoanDisbursementTemp
        fields = "__all__"

class LoanDisbursementLiveViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoanDisbursementLive
        fields = "__all__"

class PortfolioQualityLiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioQualityLive
        fields = "__all__"

class PortfolioQualityTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioQualityTemp
        fields = "__all__"
        
class PortfolioQualityLiveSerializerView(serializers.ModelSerializer):

    class Meta:
        model = PortfolioQualityLive
        fields = "__all__"

class PortfolioQualityTempSerializerView(serializers.ModelSerializer):

    class Meta:
        model = PortfolioQualityTemp
        fields = "__all__"


class PortfolioQualityTempPASerializer(serializers.ModelSerializer):

    class Meta:
        model = PortfolioQualityTemp
        fields = "__all__"

class PortfolioQualityLiveViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = PortfolioQualityLive
        fields = "__all__"

class ClientOutreachLiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientOutreachLive
        fields = "__all__"

class ClientOutreachTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientOutreachTemp
        fields = "__all__"
        
class ClientOutreachLiveSerializerView(serializers.ModelSerializer):

    class Meta:
        model = ClientOutreachLive
        fields = "__all__"

class ClientOutreachTempSerializerView(serializers.ModelSerializer):

    class Meta:
        model = ClientOutreachTemp
        fields = "__all__"


class ClientOutreachTempPASerializer(serializers.ModelSerializer):

    class Meta:
        model = ClientOutreachTemp
        fields = "__all__"

class ClientOutreachLiveViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClientOutreachLive
        fields = "__all__"

class BranchPerformanceLiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchPerformanceLive
        fields = "__all__"

class BranchPerformanceTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchPerformanceTemp
        fields = "__all__"
        
class BranchPerformanceLiveSerializerView(serializers.ModelSerializer):

    class Meta:
        model = BranchPerformanceLive
        fields = "__all__"

class BranchPerformanceTempSerializerView(serializers.ModelSerializer):

    class Meta:
        model = BranchPerformanceTemp
        fields = "__all__"


class BranchPerformanceTempPASerializer(serializers.ModelSerializer):

    class Meta:
        model = BranchPerformanceTemp
        fields = "__all__"

class BranchPerformanceLiveViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = BranchPerformanceLive
        fields = "__all__"
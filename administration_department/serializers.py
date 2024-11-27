from rest_framework import serializers
from .models import *


class OfficeExpenseLiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficeExpenseLive
        fields = "__all__"

class OfficeExpenseTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficeExpenseTemp
        fields = "__all__"
        
class OfficeExpenseLiveSerializerView(serializers.ModelSerializer):

    class Meta:
        model = OfficeExpenseLive
        fields = "__all__"

class OfficeExpenseTempSerializerView(serializers.ModelSerializer):

    class Meta:
        model = OfficeExpenseTemp
        fields = "__all__"


class OfficeExpenseTempPASerializer(serializers.ModelSerializer):

    class Meta:
        model = OfficeExpenseTemp
        fields = "__all__"

class OfficeExpenseLiveViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfficeExpenseLive
        fields = "__all__"

class AssetManagementLiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetManagementLive
        fields = "__all__"

class AssetManagementTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetManagementTemp
        fields = "__all__"
        
class AssetManagementLiveSerializerView(serializers.ModelSerializer):

    class Meta:
        model = AssetManagementLive
        fields = "__all__"

class AssetManagementTempSerializerView(serializers.ModelSerializer):

    class Meta:
        model = AssetManagementTemp
        fields = "__all__"


class AssetManagementTempPASerializer(serializers.ModelSerializer):

    class Meta:
        model = AssetManagementTemp
        fields = "__all__"

class AssetManagementLiveViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssetManagementLive
        fields = "__all__"

class LogisticsAndFleetManagementLiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogisticsAndFleetManagementLive
        fields = "__all__"

class LogisticsAndFleetManagementTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogisticsAndFleetManagementTemp
        fields = "__all__"
        
class LogisticsAndFleetManagementLiveSerializerView(serializers.ModelSerializer):

    class Meta:
        model = LogisticsAndFleetManagementLive
        fields = "__all__"

class LogisticsAndFleetManagementTempSerializerView(serializers.ModelSerializer):

    class Meta:
        model = LogisticsAndFleetManagementTemp
        fields = "__all__"


class LogisticsAndFleetManagementTempPASerializer(serializers.ModelSerializer):

    class Meta:
        model = LogisticsAndFleetManagementTemp
        fields = "__all__"

class LogisticsAndFleetManagementLiveViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = LogisticsAndFleetManagementLive
        fields = "__all__"
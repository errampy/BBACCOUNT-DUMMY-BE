from rest_framework import serializers
from .models import *


class DataAccuracyLiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataAccuracyLive
        fields = "__all__"

class DataAccuracyTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataAccuracyTemp
        fields = "__all__"
        
class DataAccuracyLiveSerializerView(serializers.ModelSerializer):

    class Meta:
        model = DataAccuracyLive
        fields = "__all__"

class DataAccuracyTempSerializerView(serializers.ModelSerializer):

    class Meta:
        model = DataAccuracyTemp
        fields = "__all__"


class DataAccuracyTempPASerializer(serializers.ModelSerializer):

    class Meta:
        model = DataAccuracyTemp
        fields = "__all__"

class DataAccuracyLiveViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataAccuracyLive
        fields = "__all__"

class SystemUptimeLiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemUptimeLive
        fields = "__all__"

class SystemUptimeTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemUptimeTemp
        fields = "__all__"
        
class SystemUptimeLiveSerializerView(serializers.ModelSerializer):

    class Meta:
        model = SystemUptimeLive
        fields = "__all__"

class SystemUptimeTempSerializerView(serializers.ModelSerializer):

    class Meta:
        model = SystemUptimeTemp
        fields = "__all__"


class SystemUptimeTempPASerializer(serializers.ModelSerializer):

    class Meta:
        model = SystemUptimeTemp
        fields = "__all__"

class SystemUptimeLiveViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = SystemUptimeLive
        fields = "__all__"

class ITTicketResolutionLiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ITTicketResolutionLive
        fields = "__all__"

class ITTicketResolutionTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = ITTicketResolutionTemp
        fields = "__all__"
        
class ITTicketResolutionLiveSerializerView(serializers.ModelSerializer):

    class Meta:
        model = ITTicketResolutionLive
        fields = "__all__"

class ITTicketResolutionTempSerializerView(serializers.ModelSerializer):

    class Meta:
        model = ITTicketResolutionTemp
        fields = "__all__"


class ITTicketResolutionTempPASerializer(serializers.ModelSerializer):

    class Meta:
        model = ITTicketResolutionTemp
        fields = "__all__"

class ITTicketResolutionLiveViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ITTicketResolutionLive
        fields = "__all__"
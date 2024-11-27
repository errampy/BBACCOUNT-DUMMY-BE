from rest_framework import serializers
from .models import *


class CustomerSatisfactionLiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerSatisfactionLive
        fields = "__all__"

class CustomerSatisfactionTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerSatisfactionTemp
        fields = "__all__"
        
class CustomerSatisfactionLiveSerializerView(serializers.ModelSerializer):

    class Meta:
        model = CustomerSatisfactionLive
        fields = "__all__"

class CustomerSatisfactionTempSerializerView(serializers.ModelSerializer):

    class Meta:
        model = CustomerSatisfactionTemp
        fields = "__all__"


class CustomerSatisfactionTempPASerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerSatisfactionTemp
        fields = "__all__"

class CustomerSatisfactionLiveViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerSatisfactionLive
        fields = "__all__"

class ClientAcquisitionLiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientAcquisitionLive
        fields = "__all__"

class ClientAcquisitionTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientAcquisitionTemp
        fields = "__all__"
        
class ClientAcquisitionLiveSerializerView(serializers.ModelSerializer):

    class Meta:
        model = ClientAcquisitionLive
        fields = "__all__"

class ClientAcquisitionTempSerializerView(serializers.ModelSerializer):

    class Meta:
        model = ClientAcquisitionTemp
        fields = "__all__"


class ClientAcquisitionTempPASerializer(serializers.ModelSerializer):

    class Meta:
        model = ClientAcquisitionTemp
        fields = "__all__"

class ClientAcquisitionLiveViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClientAcquisitionLive
        fields = "__all__"

class FeedbackAndComplaintsLiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackAndComplaintsLive
        fields = "__all__"

class FeedbackAndComplaintsTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackAndComplaintsTemp
        fields = "__all__"
        
class FeedbackAndComplaintsLiveSerializerView(serializers.ModelSerializer):

    class Meta:
        model = FeedbackAndComplaintsLive
        fields = "__all__"

class FeedbackAndComplaintsTempSerializerView(serializers.ModelSerializer):

    class Meta:
        model = FeedbackAndComplaintsTemp
        fields = "__all__"


class FeedbackAndComplaintsTempPASerializer(serializers.ModelSerializer):

    class Meta:
        model = FeedbackAndComplaintsTemp
        fields = "__all__"

class FeedbackAndComplaintsLiveViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeedbackAndComplaintsLive
        fields = "__all__"
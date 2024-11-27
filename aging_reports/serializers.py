from rest_framework import serializers
from .models import *


class LoanAgingLiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanAgingLive
        fields = "__all__"

class LoanAgingTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanAgingTemp
        fields = "__all__"
        
class LoanAgingLiveSerializerView(serializers.ModelSerializer):

    class Meta:
        model = LoanAgingLive
        fields = "__all__"

class LoanAgingTempSerializerView(serializers.ModelSerializer):

    class Meta:
        model = LoanAgingTemp
        fields = "__all__"


class LoanAgingTempPASerializer(serializers.ModelSerializer):

    class Meta:
        model = LoanAgingTemp
        fields = "__all__"

class LoanAgingLiveViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoanAgingLive
        fields = "__all__"

class AccountsReceivableAgingLiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountsReceivableAgingLive
        fields = "__all__"

class AccountsReceivableAgingTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountsReceivableAgingTemp
        fields = "__all__"
        
class AccountsReceivableAgingLiveSerializerView(serializers.ModelSerializer):

    class Meta:
        model = AccountsReceivableAgingLive
        fields = "__all__"

class AccountsReceivableAgingTempSerializerView(serializers.ModelSerializer):

    class Meta:
        model = AccountsReceivableAgingTemp
        fields = "__all__"


class AccountsReceivableAgingTempPASerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountsReceivableAgingTemp
        fields = "__all__"

class AccountsReceivableAgingLiveViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountsReceivableAgingLive
        fields = "__all__"
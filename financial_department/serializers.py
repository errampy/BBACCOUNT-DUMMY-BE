from rest_framework import serializers
from .models import *


class LoanLossProvisionLiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanLossProvisionLive
        fields = "__all__"

class LoanLossProvisionTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanLossProvisionTemp
        fields = "__all__"
        
class LoanLossProvisionLiveSerializerView(serializers.ModelSerializer):

    class Meta:
        model = LoanLossProvisionLive
        fields = "__all__"

class LoanLossProvisionTempSerializerView(serializers.ModelSerializer):

    class Meta:
        model = LoanLossProvisionTemp
        fields = "__all__"


class LoanLossProvisionTempPASerializer(serializers.ModelSerializer):

    class Meta:
        model = LoanLossProvisionTemp
        fields = "__all__"

class LoanLossProvisionLiveViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoanLossProvisionLive
        fields = "__all__"

class BalanceSheetLiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceSheetLive
        fields = "__all__"

class BalanceSheetTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceSheetTemp
        fields = "__all__"
        
class BalanceSheetLiveSerializerView(serializers.ModelSerializer):

    class Meta:
        model = BalanceSheetLive
        fields = "__all__"

class BalanceSheetTempSerializerView(serializers.ModelSerializer):

    class Meta:
        model = BalanceSheetTemp
        fields = "__all__"


class BalanceSheetTempPASerializer(serializers.ModelSerializer):

    class Meta:
        model = BalanceSheetTemp
        fields = "__all__"

class BalanceSheetLiveViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = BalanceSheetLive
        fields = "__all__"

class IncomeStatementLiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeStatementLive
        fields = "__all__"

class IncomeStatementTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeStatementTemp
        fields = "__all__"
        
class IncomeStatementLiveSerializerView(serializers.ModelSerializer):

    class Meta:
        model = IncomeStatementLive
        fields = "__all__"

class IncomeStatementTempSerializerView(serializers.ModelSerializer):

    class Meta:
        model = IncomeStatementTemp
        fields = "__all__"


class IncomeStatementTempPASerializer(serializers.ModelSerializer):

    class Meta:
        model = IncomeStatementTemp
        fields = "__all__"

class IncomeStatementLiveViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = IncomeStatementLive
        fields = "__all__"

class CashFlowStatementLiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashFlowStatementLive
        fields = "__all__"

class CashFlowStatementTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashFlowStatementTemp
        fields = "__all__"
        
class CashFlowStatementLiveSerializerView(serializers.ModelSerializer):

    class Meta:
        model = CashFlowStatementLive
        fields = "__all__"

class CashFlowStatementTempSerializerView(serializers.ModelSerializer):

    class Meta:
        model = CashFlowStatementTemp
        fields = "__all__"


class CashFlowStatementTempPASerializer(serializers.ModelSerializer):

    class Meta:
        model = CashFlowStatementTemp
        fields = "__all__"

class CashFlowStatementLiveViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = CashFlowStatementLive
        fields = "__all__"
from django.contrib import admin
from .models import *

@admin.register(LoanLossProvisionLive)
class LoanLossProvisionLiveAdmin(admin.ModelAdmin):
    list_display = ['loans_at_risk', 'provision_rate', 'required_provisions', 'loan_categories', 'remarks', 'reported_date']

@admin.register(LoanLossProvisionTemp)
class LoanLossProvisionTempAdmin(admin.ModelAdmin):
    list_display=['loans_at_risk', 'provision_rate', 'required_provisions', 'loan_categories', 'remarks', 'reported_date']
        
@admin.register(BalanceSheetLive)
class BalanceSheetLiveAdmin(admin.ModelAdmin):
    list_display = ['assets', 'liabilities', 'equity', 'asset_breakdown', 'liability_breakdown', 'reported_date']

@admin.register(BalanceSheetTemp)
class BalanceSheetTempAdmin(admin.ModelAdmin):
    list_display=['assets', 'liabilities', 'equity', 'asset_breakdown', 'liability_breakdown', 'reported_date']
        
@admin.register(IncomeStatementLive)
class IncomeStatementLiveAdmin(admin.ModelAdmin):
    list_display = ['revenue', 'operating_expenses', 'net_income', 'revenue_sources', 'expense_breakdown', 'reported_date']

@admin.register(IncomeStatementTemp)
class IncomeStatementTempAdmin(admin.ModelAdmin):
    list_display=['revenue', 'operating_expenses', 'net_income', 'revenue_sources', 'expense_breakdown', 'reported_date']
        
@admin.register(CashFlowStatementLive)
class CashFlowStatementLiveAdmin(admin.ModelAdmin):
    list_display = ['inflows', 'outflows', 'net_cash_flow', 'inflow_sources', 'outflow_categories', 'reported_date']

@admin.register(CashFlowStatementTemp)
class CashFlowStatementTempAdmin(admin.ModelAdmin):
    list_display=['inflows', 'outflows', 'net_cash_flow', 'inflow_sources', 'outflow_categories', 'reported_date']
        
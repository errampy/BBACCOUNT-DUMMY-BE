from django.contrib import admin
from .models import *

@admin.register(LoanDisbursementLive)
class LoanDisbursementLiveAdmin(admin.ModelAdmin):
    list_display = ['total_loans_disbursed', 'number_of_loans', 'average_loan_size', 'highest_loan_disbursed', 'lowest_loan_disbursed', 'loan_purpose_distribution', 'disbursement_channels', 'reported_date']

@admin.register(LoanDisbursementTemp)
class LoanDisbursementTempAdmin(admin.ModelAdmin):
    list_display=['total_loans_disbursed', 'number_of_loans', 'average_loan_size', 'highest_loan_disbursed', 'lowest_loan_disbursed', 'loan_purpose_distribution', 'disbursement_channels', 'reported_date']
        
@admin.register(PortfolioQualityLive)
class PortfolioQualityLiveAdmin(admin.ModelAdmin):
    list_display = ['portfolio_at_risk', 'total_outstanding_portfolio', 'amount_overdue', 'loans_at_risk_count', 'risk_categorization', 'recovery_rate', 'average_loan_age', 'reported_date']

@admin.register(PortfolioQualityTemp)
class PortfolioQualityTempAdmin(admin.ModelAdmin):
    list_display=['portfolio_at_risk', 'total_outstanding_portfolio', 'amount_overdue', 'loans_at_risk_count', 'risk_categorization', 'recovery_rate', 'average_loan_age', 'reported_date']
        
@admin.register(ClientOutreachLive)
class ClientOutreachLiveAdmin(admin.ModelAdmin):
    list_display = ['active_clients', 'new_clients_this_quarter', 'client_retention_rate', 'average_client_loan_size', 'inactive_clients', 'reported_date', 'outreach_campaigns', 'client_feedback_summary']

@admin.register(ClientOutreachTemp)
class ClientOutreachTempAdmin(admin.ModelAdmin):
    list_display=['active_clients', 'new_clients_this_quarter', 'client_retention_rate', 'average_client_loan_size', 'inactive_clients', 'reported_date', 'outreach_campaigns', 'client_feedback_summary']
        
@admin.register(BranchPerformanceLive)
class BranchPerformanceLiveAdmin(admin.ModelAdmin):
    list_display = ['branch_name', 'loan_portfolio', 'repayment_rate', 'total_clients', 'new_clients_this_month', 'reported_date', 'branch_location', 'branch_manager']

@admin.register(BranchPerformanceTemp)
class BranchPerformanceTempAdmin(admin.ModelAdmin):
    list_display=['branch_name', 'loan_portfolio', 'repayment_rate', 'total_clients', 'new_clients_this_month', 'reported_date', 'branch_location', 'branch_manager']
        
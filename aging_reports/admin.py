from django.contrib import admin
from .models import *

@admin.register(LoanAgingLive)
class LoanAgingLiveAdmin(admin.ModelAdmin):
    list_display = ['overdue_0_30_days', 'overdue_31_60_days', 'overdue_61_90_days', 'overdue_91_days_plus', 'total_outstanding_loans', 'reported_date', 'comments']

@admin.register(LoanAgingTemp)
class LoanAgingTempAdmin(admin.ModelAdmin):
    list_display=['overdue_0_30_days', 'overdue_31_60_days', 'overdue_61_90_days', 'overdue_91_days_plus', 'total_outstanding_loans', 'reported_date', 'comments']
        
@admin.register(AccountsReceivableAgingLive)
class AccountsReceivableAgingLiveAdmin(admin.ModelAdmin):
    list_display = ['current', 'overdue_30_days', 'overdue_60_days', 'overdue_90_days', 'overdue_90_days_plus', 'reported_date', 'total_receivables', 'comments']

@admin.register(AccountsReceivableAgingTemp)
class AccountsReceivableAgingTempAdmin(admin.ModelAdmin):
    list_display=['current', 'overdue_30_days', 'overdue_60_days', 'overdue_90_days', 'overdue_90_days_plus', 'reported_date', 'total_receivables', 'comments']
        
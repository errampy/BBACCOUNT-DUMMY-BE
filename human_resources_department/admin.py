from django.contrib import admin
from .models import *

@admin.register(LeaveManagementLive)
class LeaveManagementLiveAdmin(admin.ModelAdmin):
    list_display = ['pending_leave_requests', 'total_leave_days_taken', 'average_leave_days_per_staff', 'highest_leave_days', 'lowest_leave_days', 'reported_date', 'leave_trends', 'leave_policy_notes']

@admin.register(LeaveManagementTemp)
class LeaveManagementTempAdmin(admin.ModelAdmin):
    list_display=['pending_leave_requests', 'total_leave_days_taken', 'average_leave_days_per_staff', 'highest_leave_days', 'lowest_leave_days', 'reported_date', 'leave_trends', 'leave_policy_notes']
        
@admin.register(StaffProductivityLive)
class StaffProductivityLiveAdmin(admin.ModelAdmin):
    list_display = ['total_loan_officers', 'loans_per_officer', 'average_portfolio_per_officer', 'total_loans', 'highest_loans_by_officer', 'reported_date', 'lowest_loans_by_officer', 'performance_comments']

@admin.register(StaffProductivityTemp)
class StaffProductivityTempAdmin(admin.ModelAdmin):
    list_display=['total_loan_officers', 'loans_per_officer', 'average_portfolio_per_officer', 'total_loans', 'highest_loans_by_officer', 'reported_date', 'lowest_loans_by_officer', 'performance_comments']
        
@admin.register(TrainingDevelopmentLive)
class TrainingDevelopmentLiveAdmin(admin.ModelAdmin):
    list_display = ['training_sessions_conducted', 'staff_trained', 'total_training_costs', 'average_training_cost_per_person', 'training_focus_areas', 'reported_date', 'training_feedback_summary']

@admin.register(TrainingDevelopmentTemp)
class TrainingDevelopmentTempAdmin(admin.ModelAdmin):
    list_display=['training_sessions_conducted', 'staff_trained', 'total_training_costs', 'average_training_cost_per_person', 'training_focus_areas', 'reported_date', 'training_feedback_summary']
        
@admin.register(StaffTurnoverLive)
class StaffTurnoverLiveAdmin(admin.ModelAdmin):
    list_display = ['total_departures', 'total_new_hires', 'turnover_rate', 'current_staff_count', 'total_staff_at_start', 'reported_date', 'key_departures', 'hiring_notes']

@admin.register(StaffTurnoverTemp)
class StaffTurnoverTempAdmin(admin.ModelAdmin):
    list_display=['total_departures', 'total_new_hires', 'turnover_rate', 'current_staff_count', 'total_staff_at_start', 'reported_date', 'key_departures', 'hiring_notes']
        
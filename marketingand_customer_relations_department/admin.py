from django.contrib import admin
from .models import *

@admin.register(CustomerSatisfactionLive)
class CustomerSatisfactionLiveAdmin(admin.ModelAdmin):
    list_display = ['surveys_conducted', 'satisfaction_score', 'top_complaints', 'net_promoter_score', 'repeat_customer_percentage', 'reported_date', 'survey_response_rate', 'comments']

@admin.register(CustomerSatisfactionTemp)
class CustomerSatisfactionTempAdmin(admin.ModelAdmin):
    list_display=['surveys_conducted', 'satisfaction_score', 'top_complaints', 'net_promoter_score', 'repeat_customer_percentage', 'reported_date', 'survey_response_rate', 'comments']
        
@admin.register(ClientAcquisitionLive)
class ClientAcquisitionLiveAdmin(admin.ModelAdmin):
    list_display = ['new_clients', 'acquisition_cost_per_client', 'total_acquisition_cost', 'average_conversion_rate', 'reported_date', 'referral_percentage', 'comments']

@admin.register(ClientAcquisitionTemp)
class ClientAcquisitionTempAdmin(admin.ModelAdmin):
    list_display=['new_clients', 'acquisition_cost_per_client', 'total_acquisition_cost', 'average_conversion_rate', 'reported_date', 'referral_percentage', 'comments']
        
@admin.register(FeedbackAndComplaintsLive)
class FeedbackAndComplaintsLiveAdmin(admin.ModelAdmin):
    list_display = ['total_complaints_logged', 'resolved_complaints', 'resolution_rate', 'feedback_received', 'positive_feedback_percentage', 'reported_date', 'average_resolution_time_hours', 'unresolved_complaints', 'escalation_rate', 'comments']

@admin.register(FeedbackAndComplaintsTemp)
class FeedbackAndComplaintsTempAdmin(admin.ModelAdmin):
    list_display=['total_complaints_logged', 'resolved_complaints', 'resolution_rate', 'feedback_received', 'positive_feedback_percentage', 'reported_date', 'average_resolution_time_hours', 'unresolved_complaints', 'escalation_rate', 'comments']
        
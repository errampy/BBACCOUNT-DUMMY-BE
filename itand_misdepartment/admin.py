from django.contrib import admin
from .models import *

@admin.register(DataAccuracyLive)
class DataAccuracyLiveAdmin(admin.ModelAdmin):
    list_display = ['errors_detected', 'corrected_entries_percentage', 'audit_frequency', 'system_generated_errors', 'reported_date', 'manual_input_errors', 'critical_errors', 'accuracy_comments']

@admin.register(DataAccuracyTemp)
class DataAccuracyTempAdmin(admin.ModelAdmin):
    list_display=['errors_detected', 'corrected_entries_percentage', 'audit_frequency', 'system_generated_errors', 'reported_date', 'manual_input_errors', 'critical_errors', 'accuracy_comments']
        
@admin.register(SystemUptimeLive)
class SystemUptimeLiveAdmin(admin.ModelAdmin):
    list_display = ['total_downtime_hours', 'uptime_percentage', 'scheduled_maintenance_hours', 'unscheduled_outage_hours', 'critical_systems_affected', 'reported_date', 'system_comments']

@admin.register(SystemUptimeTemp)
class SystemUptimeTempAdmin(admin.ModelAdmin):
    list_display=['total_downtime_hours', 'uptime_percentage', 'scheduled_maintenance_hours', 'unscheduled_outage_hours', 'critical_systems_affected', 'reported_date', 'system_comments']
        
@admin.register(ITTicketResolutionLive)
class ITTicketResolutionLiveAdmin(admin.ModelAdmin):
    list_display = ['tickets_raised', 'tickets_resolved', 'average_resolution_time_hours', 'high_priority_tickets', 'unresolved_tickets', 'reported_date', 'escalation_rate', 'resolution_comments']

@admin.register(ITTicketResolutionTemp)
class ITTicketResolutionTempAdmin(admin.ModelAdmin):
    list_display=['tickets_raised', 'tickets_resolved', 'average_resolution_time_hours', 'high_priority_tickets', 'unresolved_tickets', 'reported_date', 'escalation_rate', 'resolution_comments']
        
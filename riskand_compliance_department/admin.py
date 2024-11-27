from django.contrib import admin
from .models import *

@admin.register(ComplianceLive)
class ComplianceLiveAdmin(admin.ModelAdmin):
    list_display = ['kyc_non_compliance_cases', 'aml_monitoring_alerts', 'penalties_incurred', 'audits_conducted', 'compliance_violations', 'reported_date', 'compliance_training_sessions', 'training_attendees', 'compliance_comments']

@admin.register(ComplianceTemp)
class ComplianceTempAdmin(admin.ModelAdmin):
    list_display=['kyc_non_compliance_cases', 'aml_monitoring_alerts', 'penalties_incurred', 'audits_conducted', 'compliance_violations', 'reported_date', 'compliance_training_sessions', 'training_attendees', 'compliance_comments']
        
@admin.register(FraudMonitoringLive)
class FraudMonitoringLiveAdmin(admin.ModelAdmin):
    list_display = ['detected_fraud_incidents', 'total_amount_involved', 'resolution_status_percentage', 'open_fraud_cases', 'fraud_detection_methods', 'reported_date', 'fraud_prevention_actions', 'investigation_comments']

@admin.register(FraudMonitoringTemp)
class FraudMonitoringTempAdmin(admin.ModelAdmin):
    list_display=['detected_fraud_incidents', 'total_amount_involved', 'resolution_status_percentage', 'open_fraud_cases', 'fraud_detection_methods', 'reported_date', 'fraud_prevention_actions', 'investigation_comments']
        
@admin.register(RiskAssessmentLive)
class RiskAssessmentLiveAdmin(admin.ModelAdmin):
    list_display = ['top_risks', 'mitigation_actions', 'residual_risk_level', 'risk_review_frequency', 'reported_date', 'incidents_tracked', 'risk_owner', 'risk_comments']

@admin.register(RiskAssessmentTemp)
class RiskAssessmentTempAdmin(admin.ModelAdmin):
    list_display=['top_risks', 'mitigation_actions', 'residual_risk_level', 'risk_review_frequency', 'reported_date', 'incidents_tracked', 'risk_owner', 'risk_comments']
        
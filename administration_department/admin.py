from django.contrib import admin
from .models import *

@admin.register(OfficeExpenseLive)
class OfficeExpenseLiveAdmin(admin.ModelAdmin):
    list_display = ['total_office_expenses', 'top_expenses', 'utilities_expenses', 'rent_expenses', 'office_supplies_expenses', 'reported_date', 'employee_welfare_expenses', 'maintenance_expenses', 'comments']

@admin.register(OfficeExpenseTemp)
class OfficeExpenseTempAdmin(admin.ModelAdmin):
    list_display=['total_office_expenses', 'top_expenses', 'utilities_expenses', 'rent_expenses', 'office_supplies_expenses', 'reported_date', 'employee_welfare_expenses', 'maintenance_expenses', 'comments']
        
@admin.register(AssetManagementLive)
class AssetManagementLiveAdmin(admin.ModelAdmin):
    list_display = ['total_fixed_assets', 'depreciation', 'maintenance_costs', 'asset_utilization_rate', 'repairs_and_upgrades_cost', 'reported_date', 'new_assets_acquired', 'comments']

@admin.register(AssetManagementTemp)
class AssetManagementTempAdmin(admin.ModelAdmin):
    list_display=['total_fixed_assets', 'depreciation', 'maintenance_costs', 'asset_utilization_rate', 'repairs_and_upgrades_cost', 'reported_date', 'new_assets_acquired', 'comments']
        
@admin.register(LogisticsAndFleetManagementLive)
class LogisticsAndFleetManagementLiveAdmin(admin.ModelAdmin):
    list_display = ['total_vehicles', 'vehicles_in_use', 'fuel_costs', 'maintenance_costs', 'vehicle_insurance_expenses', 'reported_date', 'vehicle_replacement_value', 'fleet_utilization_rate', 'fleet_safety_compliance_rate', 'vehicle_acquisition_cost', 'comments']

@admin.register(LogisticsAndFleetManagementTemp)
class LogisticsAndFleetManagementTempAdmin(admin.ModelAdmin):
    list_display=['total_vehicles', 'vehicles_in_use', 'fuel_costs', 'maintenance_costs', 'vehicle_insurance_expenses', 'reported_date', 'vehicle_replacement_value', 'fleet_utilization_rate', 'fleet_safety_compliance_rate', 'vehicle_acquisition_cost', 'comments']
        
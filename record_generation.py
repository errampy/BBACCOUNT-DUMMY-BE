from faker import Faker
import random
from datetime import datetime, timedelta
from administration_department.models import *  # Replace with your app and model name
from aging_reports.models import *
from financial_department.models import *
from human_resources_department.models import *
from itand_misdepartment.models import *
from marketingand_customer_relations_department.models import *
from operations_department.models import *
from riskand_compliance_department.models import *
fake = Faker()

# Generate 50 dummy records

def OfficeExpenseLive():
    for _ in range(50):
        OfficeExpenseAudit.objects.create(
            code=fake.bothify(text='??-###-??', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),  # Random pattern code like AB-123-CD
            total_office_expenses=round(random.uniform(1000, 10000), 2),  # Random float between 1000 and 10000
            top_expenses=fake.text(max_nb_chars=200),  # Random text for top expenses
            utilities_expenses=round(random.uniform(100, 2000), 2),  # Random float between 100 and 2000
            rent_expenses=round(random.uniform(500, 5000), 2),  # Random float between 500 and 5000
            office_supplies_expenses=round(random.uniform(50, 1500), 2),  # Random float between 50 and 1500
            reported_date=fake.date_between(start_date='-1y', end_date='today'),  # Random date within the past year
            employee_welfare_expenses=round(random.uniform(200, 3000), 2),  # Random float between 200 and 3000
            maintenance_expenses=round(random.uniform(100, 2500), 2),  # Random float between 100 and 2500
            comments=fake.text(max_nb_chars=300)  # Random comment text
        )

def AssetManagement():
    for _ in range(50):
        AssetManagementAudit.objects.create(
            code=fake.bothify(text='??-###-??', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),  # Random pattern like AB-123-CD
            total_fixed_assets=round(random.uniform(5000, 100000), 2),  # Random float between 5000 and 100000
            depreciation=round(random.uniform(500, 10000), 2),  # Random float between 500 and 10000
            maintenance_costs=round(random.uniform(100, 5000), 2),  # Random float between 100 and 5000
            asset_utilization_rate=round(random.uniform(0, 100), 2),  # Random percentage between 0 and 100
            repairs_and_upgrades_cost=round(random.uniform(200, 7000), 2),  # Random float between 200 and 7000
            reported_date=fake.date_between(start_date='-2y', end_date='today'),  # Random date in the last 2 years
            new_assets_acquired=round(random.uniform(1000, 20000), 2),  # Random float between 1000 and 20000
            comments=fake.text(max_nb_chars=200)  # Random text up to 200 characters
        )

def populate_logistics_and_fleet_management(num_records=50):
    for _ in range(num_records):
        total_vehicles = random.randint(10, 100)  # Random total vehicles between 10 and 100
        vehicles_in_use = random.randint(1,
                                         total_vehicles)  # Random number of vehicles in use (must be <= total_vehicles)

        LogisticsAndFleetManagementAudit.objects.create(
            code=fake.bothify(text='??-###-??', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),  # Random pattern like AB-123-CD
            total_vehicles=total_vehicles,
            vehicles_in_use=vehicles_in_use,
            fuel_costs=round(random.uniform(5000, 100000), 2),  # Random float between 5000 and 100000
            maintenance_costs=round(random.uniform(1000, 20000), 2),  # Random float between 1000 and 20000
            vehicle_insurance_expenses=round(random.uniform(2000, 15000), 2),  # Random float between 2000 and 15000
            reported_date=fake.date_between(start_date='-2y', end_date='today'),  # Random date in the last 2 years
            vehicle_replacement_value=round(random.uniform(10000, 150000), 2),  # Random float between 10000 and 150000
            fleet_utilization_rate=round((vehicles_in_use / total_vehicles) * 100, 2),
            # Utilization rate as a percentage
            fleet_safety_compliance_rate=round(random.uniform(80, 100), 2),
            # Random compliance rate between 80% and 100%
            vehicle_acquisition_cost=round(random.uniform(5000, 75000), 2),  # Random float between 5000 and 75000
            comments=fake.text(max_nb_chars=200)  # Random text up to 200 characters
        )

def populate_loan_aging(num_records=50):
    for _ in range(num_records):
        overdue_0_30_days = round(random.uniform(1000, 50000), 2)
        overdue_31_60_days = round(random.uniform(1000, 50000), 2)
        overdue_61_90_days = round(random.uniform(1000, 50000), 2)
        overdue_91_days_plus = round(random.uniform(1000, 50000), 2)
        total_outstanding_loans = round(overdue_0_30_days + overdue_31_60_days + overdue_61_90_days + overdue_91_days_plus, 2)

        LoanAgingAudit.objects.create(
            code=fake.bothify(text='LA-###-??', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            overdue_0_30_days=overdue_0_30_days,
            overdue_31_60_days=overdue_31_60_days,
            overdue_61_90_days=overdue_61_90_days,
            overdue_91_days_plus=overdue_91_days_plus,
            total_outstanding_loans=total_outstanding_loans,
            reported_date=fake.date_between(start_date='-2y', end_date='today'),
            comments=fake.text(max_nb_chars=200)
        )

    print(f"{num_records} records have been successfully created for LoanAging.")

def populate_accounts_receivable_aging(num_records=50):
    for _ in range(num_records):
        current = round(random.uniform(1000, 30000), 2)
        overdue_30_days = round(random.uniform(500, 15000), 2)
        overdue_60_days = round(random.uniform(500, 15000), 2)
        overdue_90_days = round(random.uniform(500, 15000), 2)
        overdue_90_days_plus = round(random.uniform(500, 15000), 2)
        total_receivables = round(current + overdue_30_days + overdue_60_days + overdue_90_days + overdue_90_days_plus, 2)

        AccountsReceivableAgingAudit.objects.create(
            code=fake.bothify(text='AR-###-??', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            current=current,
            overdue_30_days=overdue_30_days,
            overdue_60_days=overdue_60_days,
            overdue_90_days=overdue_90_days,
            overdue_90_days_plus=overdue_90_days_plus,
            total_receivables=total_receivables,
            reported_date=fake.date_between(start_date='-2y', end_date='today'),
            comments=fake.text(max_nb_chars=200)
        )

    print(f"{num_records} records have been successfully created for AccountsReceivableAging.")

def populate_loan_loss_provision(num_records=50):
    for _ in range(num_records):
        loans_at_risk = round(random.uniform(10000, 200000), 2)
        provision_rate = round(random.uniform(0.01, 0.2), 2)
        required_provisions = round(loans_at_risk * provision_rate, 2)

        LoanLossProvisionAudit.objects.create(
            code=fake.bothify(text='LLP-###-??', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            loans_at_risk=loans_at_risk,
            provision_rate=provision_rate,
            required_provisions=required_provisions,
            loan_categories=fake.text(max_nb_chars=100),
            remarks=fake.text(max_nb_chars=200),
            reported_date=fake.date_between(start_date='-2y', end_date='today'),
        )

    print(f"{num_records} records have been successfully created for LoanLossProvision.")

def populate_balance_sheet(num_records=50):
    for _ in range(num_records):
        assets = round(random.uniform(50000, 500000), 2)
        liabilities = round(random.uniform(10000, 300000), 2)
        equity = round(assets - liabilities, 2)

        BalanceSheetAudit.objects.create(
            code=fake.bothify(text='BS-###-??', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            assets=assets,
            liabilities=liabilities,
            equity=equity,
            asset_breakdown=fake.text(max_nb_chars=150),
            liability_breakdown=fake.text(max_nb_chars=150),
            reported_date=fake.date_between(start_date='-2y', end_date='today'),
        )

    print(f"{num_records} records have been successfully created for BalanceSheet.")

def populate_income_statement(num_records=50):
    for _ in range(num_records):
        revenue = round(random.uniform(100000, 1000000), 2)
        operating_expenses = round(random.uniform(20000, 500000), 2)
        net_income = round(revenue - operating_expenses, 2)

        IncomeStatementAudit.objects.create(
            code=fake.bothify(text='IS-###-??', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            revenue=revenue,
            operating_expenses=operating_expenses,
            net_income=net_income,
            revenue_sources=fake.text(max_nb_chars=150),
            expense_breakdown=fake.text(max_nb_chars=150),
            reported_date=fake.date_between(start_date='-2y', end_date='today'),
        )

    print(f"{num_records} records have been successfully created for IncomeStatement.")

def populate_cash_flow_statement(num_records=50):
    for _ in range(num_records):
        inflows = round(random.uniform(100000, 500000), 2)
        outflows = round(random.uniform(50000, 300000), 2)
        net_cash_flow = round(inflows - outflows, 2)

        CashFlowStatementAudit.objects.create(
            code=fake.bothify(text='CFS-###-??', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            inflows=inflows,
            outflows=outflows,
            net_cash_flow=net_cash_flow,
            inflow_sources=fake.text(max_nb_chars=150),
            outflow_categories=fake.text(max_nb_chars=150),
            reported_date=fake.date_between(start_date='-2y', end_date='today'),
        )

    print(f"{num_records} records have been successfully created for CashFlowStatement.")

def populate_leave_management(num_records=50):
    for _ in range(num_records):
        pending_leave_requests = random.randint(0, 20)
        total_leave_days_taken = random.randint(1, 150)
        average_leave_days_per_staff = round(random.uniform(1.0, 20.0), 2)
        highest_leave_days = random.randint(10, 50)
        lowest_leave_days = random.randint(0, 5)

        LeaveManagementAudit.objects.create(
            code=fake.bothify(text='LM-###-??', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            pending_leave_requests=pending_leave_requests,
            total_leave_days_taken=total_leave_days_taken,
            average_leave_days_per_staff=average_leave_days_per_staff,
            highest_leave_days=highest_leave_days,
            lowest_leave_days=lowest_leave_days,
            reported_date=fake.date_between(start_date='-2y', end_date='today'),
            leave_trends=fake.text(max_nb_chars=150),
            leave_policy_notes=fake.text(max_nb_chars=200),
        )

    print(f"{num_records} records have been successfully created for LeaveManagement.")

def populate_staff_productivity(num_records=50):
    for _ in range(num_records):
        total_loan_officers = random.randint(1, 50)
        loans_per_officer = random.randint(5, 100)
        average_portfolio_per_officer = round(random.uniform(10000.0, 200000.0), 2)
        total_loans = random.randint(100, 5000)
        highest_loans_by_officer = random.randint(50, 200)
        lowest_loans_by_officer = random.randint(0, 30)

        StaffProductivityAudit.objects.create(
            code=fake.bothify(text='SP-###-??', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            total_loan_officers=total_loan_officers,
            loans_per_officer=loans_per_officer,
            average_portfolio_per_officer=average_portfolio_per_officer,
            total_loans=total_loans,
            highest_loans_by_officer=highest_loans_by_officer,
            lowest_loans_by_officer=lowest_loans_by_officer,
            reported_date=fake.date_between(start_date='-2y', end_date='today'),
            performance_comments=fake.text(max_nb_chars=150),
        )

    print(f"{num_records} records have been successfully created for StaffProductivity.")

def populate_training_development(num_records=50):
    for _ in range(num_records):
        training_sessions_conducted = random.randint(1, 20)
        staff_trained = random.randint(5, 200)
        total_training_costs = round(random.uniform(1000.0, 50000.0), 2)
        average_training_cost_per_person = round(total_training_costs / staff_trained, 2)

        TrainingDevelopmentAudit.objects.create(
            code=fake.bothify(text='TD-###-??', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            training_sessions_conducted=training_sessions_conducted,
            staff_trained=staff_trained,
            total_training_costs=total_training_costs,
            average_training_cost_per_person=average_training_cost_per_person,
            training_focus_areas=fake.text(max_nb_chars=100),
            reported_date=fake.date_between(start_date='-2y', end_date='today'),
            training_feedback_summary=fake.text(max_nb_chars=150),
        )

    print(f"{num_records} records have been successfully created for TrainingDevelopment.")

def populate_staff_turnover(num_records=50):
    for _ in range(num_records):
        total_departures = random.randint(0, 50)
        total_new_hires = random.randint(0, 50)
        total_staff_at_start = random.randint(100, 500)
        current_staff_count = total_staff_at_start - total_departures + total_new_hires
        turnover_rate = round((total_departures / total_staff_at_start) * 100, 2)

        StaffTurnoverAudit.objects.create(
            code=fake.bothify(text='ST-###-??', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            total_departures=total_departures,
            total_new_hires=total_new_hires,
            turnover_rate=turnover_rate,
            current_staff_count=current_staff_count,
            total_staff_at_start=total_staff_at_start,
            reported_date=fake.date_between(start_date='-2y', end_date='today'),
            key_departures=fake.text(max_nb_chars=150),
            hiring_notes=fake.text(max_nb_chars=150),
        )

    print(f"{num_records} records have been successfully created for StaffTurnover.")

def populate_data_accuracy(num_records=50):
    for _ in range(num_records):
        errors_detected = random.randint(0, 500)
        corrected_entries_percentage = round(random.uniform(80.0, 99.9), 2)
        audit_frequency = random.choice(['Daily', 'Weekly', 'Monthly', 'Quarterly'])
        system_generated_errors = random.randint(0, 300)
        manual_input_errors = random.randint(0, 200)
        critical_errors = random.randint(0, 50)

        DataAccuracyAudit.objects.create(
            code=fake.bothify(text='DA-###-??', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            errors_detected=errors_detected,
            corrected_entries_percentage=corrected_entries_percentage,
            audit_frequency=audit_frequency,
            system_generated_errors=system_generated_errors,
            reported_date=fake.date_between(start_date='-2y', end_date='today'),
            manual_input_errors=manual_input_errors,
            critical_errors=critical_errors,
            accuracy_comments=fake.text(max_nb_chars=150),
        )

    print(f"{num_records} records have been successfully created for DataAccuracy.")

def populate_system_uptime(num_records=50):
    for _ in range(num_records):
        total_downtime_hours = round(random.uniform(0.0, 100.0), 2)
        uptime_percentage = round(
            100 - (total_downtime_hours / (total_downtime_hours + random.uniform(200.0, 500.0)) * 100), 2)
        scheduled_maintenance_hours = round(random.uniform(0.0, 50.0), 2)
        unscheduled_outage_hours = round(random.uniform(0.0, 20.0), 2)
        critical_systems_affected = random.randint(0, 10)

        SystemUptimeAudit.objects.create(
            code=fake.bothify(text='SU-###-??', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            total_downtime_hours=total_downtime_hours,
            uptime_percentage=uptime_percentage,
            scheduled_maintenance_hours=scheduled_maintenance_hours,
            unscheduled_outage_hours=unscheduled_outage_hours,
            critical_systems_affected=critical_systems_affected,
            reported_date=fake.date_between(start_date='-2y', end_date='today'),
            system_comments=fake.text(max_nb_chars=150),
        )

    print(f"{num_records} records have been successfully created for SystemUptime.")

def populate_it_ticket_resolution(num_records=50):
    for _ in range(num_records):
        tickets_raised = random.randint(10, 300)
        tickets_resolved = random.randint(5, tickets_raised)
        average_resolution_time_hours = round(random.uniform(1.0, 72.0), 2)
        high_priority_tickets = random.randint(0, 50)
        unresolved_tickets = tickets_raised - tickets_resolved
        escalation_rate = round((unresolved_tickets / tickets_raised) * 100, 2) if tickets_raised > 0 else 0.0

        ITTicketResolutionAudit.objects.create(
            code=fake.bothify(text='ITR-###-??', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            tickets_raised=tickets_raised,
            tickets_resolved=tickets_resolved,
            average_resolution_time_hours=average_resolution_time_hours,
            high_priority_tickets=high_priority_tickets,
            unresolved_tickets=unresolved_tickets,
            reported_date=fake.date_between(start_date='-2y', end_date='today'),
            escalation_rate=escalation_rate,
            resolution_comments=fake.text(max_nb_chars=150),
        )

    print(f"{num_records} records have been successfully created for ITTicketResolution.")

def populate_customer_satisfaction(num_records=50):
    for _ in range(num_records):
        surveys_conducted = random.randint(50, 500)
        satisfaction_score = round(random.uniform(1.0, 10.0), 1)  # Score between 1.0 and 10.0
        net_promoter_score = round(random.uniform(-100.0, 100.0), 1)  # NPS can be from -100 to 100
        repeat_customer_percentage = round(random.uniform(20.0, 90.0), 2)
        survey_response_rate = round(random.uniform(50.0, 95.0), 2)

        CustomerSatisfactionAudit.objects.create(
            code=fake.bothify(text='CS-###-??', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            surveys_conducted=surveys_conducted,
            satisfaction_score=satisfaction_score,
            top_complaints=fake.sentence(nb_words=10),
            net_promoter_score=net_promoter_score,
            repeat_customer_percentage=repeat_customer_percentage,
            reported_date=fake.date_between(start_date='-2y', end_date='today'),
            survey_response_rate=survey_response_rate,
            comments=fake.text(max_nb_chars=150),
        )

    print(f"{num_records} records have been successfully created for CustomerSatisfaction.")


def populate_client_acquisition(num_records=50):
    for _ in range(num_records):
        new_clients = random.randint(10, 200)
        acquisition_cost_per_client = round(random.uniform(50.0, 1000.0), 2)
        total_acquisition_cost = round(new_clients * acquisition_cost_per_client, 2)
        average_conversion_rate = round(random.uniform(0.5, 20.0), 2)  # Conversion rate as a percentage
        referral_percentage = round(random.uniform(5.0, 50.0), 2)

        ClientAcquisitionAudit.objects.create(
            code=fake.bothify(text='CA-###-??', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            new_clients=new_clients,
            acquisition_cost_per_client=acquisition_cost_per_client,
            total_acquisition_cost=total_acquisition_cost,
            average_conversion_rate=average_conversion_rate,
            reported_date=fake.date_between(start_date='-2y', end_date='today'),
            referral_percentage=referral_percentage,
            comments=fake.text(max_nb_chars=150),
        )

    print(f"{num_records} records have been successfully created for ClientAcquisition.")


def populate_feedback_and_complaints(num_records=50):
    for _ in range(num_records):
        total_complaints_logged = random.randint(10, 200)
        resolved_complaints = random.randint(5, total_complaints_logged)
        resolution_rate = round((resolved_complaints / total_complaints_logged) * 100,
                                2) if total_complaints_logged > 0 else 0.0
        feedback_received = random.randint(50, 500)
        positive_feedback_percentage = round(random.uniform(40.0, 95.0), 2)
        average_resolution_time_hours = round(random.uniform(1.0, 72.0), 2)
        unresolved_complaints = total_complaints_logged - resolved_complaints
        escalation_rate = round((unresolved_complaints / total_complaints_logged) * 100,
                                2) if total_complaints_logged > 0 else 0.0

        FeedbackAndComplaintsAudit.objects.create(
            code=fake.bothify(text='FC-###-??', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            total_complaints_logged=total_complaints_logged,
            resolved_complaints=resolved_complaints,
            resolution_rate=resolution_rate,
            feedback_received=feedback_received,
            positive_feedback_percentage=positive_feedback_percentage,
            reported_date=fake.date_between(start_date='-2y', end_date='today'),
            average_resolution_time_hours=average_resolution_time_hours,
            unresolved_complaints=unresolved_complaints,
            escalation_rate=escalation_rate,
            comments=fake.text(max_nb_chars=150),
        )

    print(f"{num_records} records have been successfully created for FeedbackAndComplaints.")

# Function to populate LoanDisbursement model
def populate_loan_disbursement(num_records=50):
    for _ in range(num_records):
        total_loans_disbursed = round(random.uniform(10000, 1000000), 2)
        number_of_loans = random.randint(1, 500)
        average_loan_size = total_loans_disbursed / number_of_loans if number_of_loans > 0 else 0
        highest_loan_disbursed = round(random.uniform(1000, 50000), 2)
        lowest_loan_disbursed = round(random.uniform(100, 5000), 2)

        LoanDisbursementAudit.objects.create(
            code=fake.bothify(text='LD-###-??', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            total_loans_disbursed=total_loans_disbursed,
            number_of_loans=number_of_loans,
            average_loan_size=average_loan_size,
            highest_loan_disbursed=highest_loan_disbursed,
            lowest_loan_disbursed=lowest_loan_disbursed,
            loan_purpose_distribution=fake.sentence(nb_words=10),
            disbursement_channels=fake.sentence(nb_words=10),
            reported_date=fake.date_between(start_date='-2y', end_date='today'),
        )

    print(f"{num_records} records have been successfully created for LoanDisbursement.")

# Function to populate PortfolioQuality model
def populate_portfolio_quality(num_records=50):
    for _ in range(num_records):
        portfolio_at_risk = round(random.uniform(1000, 50000), 2)
        total_outstanding_portfolio = round(random.uniform(10000, 500000), 2)
        amount_overdue = round(random.uniform(1000, total_outstanding_portfolio), 2)
        loans_at_risk_count = random.randint(0, 50)
        recovery_rate = round(random.uniform(0.0, 100.0), 2)
        average_loan_age = round(random.uniform(1.0, 10.0), 1)

        PortfolioQualityAudit.objects.create(
            code=fake.bothify(text='PQ-###-??', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            portfolio_at_risk=portfolio_at_risk,
            total_outstanding_portfolio=total_outstanding_portfolio,
            amount_overdue=amount_overdue,
            loans_at_risk_count=loans_at_risk_count,
            risk_categorization=fake.sentence(nb_words=15),
            recovery_rate=recovery_rate,
            average_loan_age=average_loan_age,
            reported_date=fake.date_between(start_date='-2y', end_date='today'),
        )

    print(f"{num_records} records have been successfully created for PortfolioQuality.")


# Function to populate ClientOutreach model
def populate_client_outreach(num_records=50):
    for _ in range(num_records):
        active_clients = random.randint(50, 1000)
        new_clients_this_quarter = random.randint(5, 200)
        client_retention_rate = round(random.uniform(50.0, 100.0), 2)
        average_client_loan_size = round(random.uniform(1000.0, 50000.0), 2)
        inactive_clients = random.randint(0, active_clients)

        ClientOutreachAudit.objects.create(
            code=fake.bothify(text='CO-###-??', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            active_clients=active_clients,
            new_clients_this_quarter=new_clients_this_quarter,
            client_retention_rate=client_retention_rate,
            average_client_loan_size=average_client_loan_size,
            inactive_clients=inactive_clients,
            reported_date=fake.date_between(start_date='-2y', end_date='today'),
            outreach_campaigns=fake.sentence(nb_words=15),
            client_feedback_summary=fake.text(max_nb_chars=150),
        )

    print(f"{num_records} records have been successfully created for ClientOutreach.")

# Function to populate BranchPerformance model
def populate_branch_performance(num_records=50):
    for _ in range(num_records):
        loan_portfolio = round(random.uniform(50000, 1000000), 2)
        repayment_rate = round(random.uniform(50.0, 100.0), 2)
        total_clients = random.randint(100, 500)
        new_clients_this_month = random.randint(10, 100)

        BranchPerformanceAudit.objects.create(
            code=fake.bothify(text='BP-###-??', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            branch_name=fake.company(),
            loan_portfolio=loan_portfolio,
            repayment_rate=repayment_rate,
            total_clients=total_clients,
            new_clients_this_month=new_clients_this_month,
            reported_date=fake.date_between(start_date='-2y', end_date='today'),
            branch_location=fake.address(),
            branch_manager=fake.name(),
        )

    print(f"{num_records} records have been successfully created for BranchPerformance.")

# Function to populate Compliance model
def populate_compliance(num_records=50):
    for _ in range(num_records):
        kyc_non_compliance_cases = random.randint(0, 50)
        aml_monitoring_alerts = random.randint(0, 20)
        penalties_incurred = round(random.uniform(1000, 50000), 2)
        audits_conducted = random.randint(1, 10)
        compliance_violations = random.randint(0, 5)
        compliance_training_sessions = random.randint(1, 10)
        training_attendees = random.randint(10, 200)

        ComplianceAudit.objects.create(
            code=fake.bothify(text='C-###-??', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            kyc_non_compliance_cases=kyc_non_compliance_cases,
            aml_monitoring_alerts=aml_monitoring_alerts,
            penalties_incurred=penalties_incurred,
            audits_conducted=audits_conducted,
            compliance_violations=compliance_violations,
            reported_date=fake.date_between(start_date='-2y', end_date='today'),
            compliance_training_sessions=compliance_training_sessions,
            training_attendees=training_attendees,
            compliance_comments=fake.text(max_nb_chars=200),
        )

    print(f"{num_records} records have been successfully created for Compliance.")


# Function to populate FraudMonitoring model
def populate_fraud_monitoring(num_records=50):
    for _ in range(num_records):
        detected_fraud_incidents = random.randint(0, 20)
        total_amount_involved = round(random.uniform(1000, 50000), 2)
        resolution_status_percentage = round(random.uniform(50.0, 100.0), 2)
        open_fraud_cases = random.randint(0, 10)

        FraudMonitoringAudit.objects.create(
            code=fake.bothify(text='FM-###-??', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            detected_fraud_incidents=detected_fraud_incidents,
            total_amount_involved=total_amount_involved,
            resolution_status_percentage=resolution_status_percentage,
            open_fraud_cases=open_fraud_cases,
            fraud_detection_methods=fake.sentence(nb_words=10),
            reported_date=fake.date_between(start_date='-2y', end_date='today'),
            fraud_prevention_actions=fake.sentence(nb_words=15),
            investigation_comments=fake.text(max_nb_chars=200),
        )

    print(f"{num_records} records have been successfully created for FraudMonitoring.")


# Function to populate RiskAssessment model
def populate_risk_assessment(num_records=50):
    for _ in range(num_records):
        residual_risk_level = round(random.uniform(0.0, 100.0), 2)
        incidents_tracked = random.randint(0, 100)

        RiskAssessmentAudit.objects.create(
            code=fake.bothify(text='RA-###-??', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            top_risks=fake.sentence(nb_words=10),
            mitigation_actions=fake.sentence(nb_words=12),
            residual_risk_level=residual_risk_level,
            risk_review_frequency=fake.word(),
            reported_date=fake.date_between(start_date='-2y', end_date='today'),
            incidents_tracked=incidents_tracked,
            risk_owner=fake.name(),
            risk_comments=fake.text(max_nb_chars=200),
        )

    print(f"{num_records} records have been successfully created for RiskAssessment.")
OfficeExpenseLive()
AssetManagement()
populate_logistics_and_fleet_management()
populate_loan_aging()
populate_accounts_receivable_aging()
populate_loan_loss_provision()
populate_balance_sheet()
populate_income_statement()
populate_cash_flow_statement()
populate_leave_management()
populate_staff_productivity()
populate_training_development()
populate_staff_turnover()
populate_data_accuracy()
populate_system_uptime()
populate_it_ticket_resolution()
populate_customer_satisfaction()
populate_client_acquisition()
populate_feedback_and_complaints()
populate_loan_disbursement()
populate_portfolio_quality()
populate_client_outreach()
populate_branch_performance()
populate_compliance()
populate_fraud_monitoring()
populate_risk_assessment()
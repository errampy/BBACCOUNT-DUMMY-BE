from django.core.exceptions import ValidationError
from django.apps import apps
from .models import *
from .serializers import *
from mainapp.middleware import get_current_request
from mainapp.scripts import *
from mainapp.serializers import *
from django.contrib.auth.hashers import make_password
from mainapp.ms_crud import *
from datetime import datetime

APP_NAME = __name__.split('.')[0]



#add foreign key import model.


def create_compliance(kyc_non_compliance_cases, aml_monitoring_alerts, penalties_incurred, audits_conducted, compliance_violations, reported_date, compliance_training_sessions, training_attendees, compliance_comments):
    """
    Creates a Compliance instance with the provided data.
        Args:
        kyc_non_compliance_cases, aml_monitoring_alerts, penalties_incurred, audits_conducted, compliance_violations, reported_date, compliance_training_sessions, training_attendees, compliance_comments: Keyword arguments for Compliance fields.

    Returns:
        dict: Success or error message.
        APP_NAME = __name__.split('.')[0]

    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        data={'kyc_non_compliance_cases': kyc_non_compliance_cases,
			'aml_monitoring_alerts': aml_monitoring_alerts,
			'penalties_incurred': penalties_incurred,
			'audits_conducted': audits_conducted,
			'compliance_violations': compliance_violations,
			'reported_date': reported_date,
			'compliance_training_sessions': compliance_training_sessions,
			'training_attendees': training_attendees,
			'compliance_comments': compliance_comments,}
        data['code'] = generate_random_id('ABC')
        data_create = data.copy()
        data_create['code'] = generate_random_id('ABC')
        data_create['record_type']='create'
        # Initialize the serializer with the data
        serializer_temp = ComplianceTempSerializer(data=data_create)
        serializer_live=ComplianceLiveSerializer(data=data)
        
        # Validate and save the serializer data
        if serializer_live.is_valid() and serializer_temp.is_valid() :
            temp_instance = serializer_temp.save()
            type=temp_instance.record_type
            # Call auditing and authorization functions if needed
            is_audit = model_audit(request,APP_NAME,'Compliance',temp_instance.pk)
            is_authorization = self_authorization(request,APP_NAME,'Compliance', temp_instance.pk,type)
            
            model_name='Compliance'
            record_id=temp_instance.pk
            # type=temp_instance.record_type
            
            user_ids_resp=get_next_user_from_work_flow(request,model_name,temp_instance=record_id,type=type)
            if user_ids_resp is None:
                return success(f'Successfully created {temp_instance} Temp ')
     
        else:
            errors = {
                'temp_errors': serializer_temp.errors,
                'live_errors': serializer_live.errors,
            }
            return error(f"Error: {errors}")
    except ValidationError as e:
        return error(f"Validation Error: {e}")
    except Exception as e:
        return error(f"An error occurred: {e}")

def update_compliance_temp(code,kyc_non_compliance_cases=None, aml_monitoring_alerts=None, penalties_incurred=None, audits_conducted=None, compliance_violations=None, reported_date=None, compliance_training_sessions=None, training_attendees=None, compliance_comments=None):
    """
    Updates a Compliance instance with the provided data.
    
    Args:
        compliance_id (int): ID of the Compliance to update.
        kyc_non_compliance_cases=None, aml_monitoring_alerts=None, penalties_incurred=None, audits_conducted=None, compliance_violations=None, reported_date=None, compliance_training_sessions=None, training_attendees=None, compliance_comments=None: Keyword arguments for Compliance fields to update.

    Returns:
        dict: Success or error message.
    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if  is_have_permission(request,APP_NAME, 'Compliance',code):

            data={'kyc_non_compliance_cases': kyc_non_compliance_cases,
			'aml_monitoring_alerts': aml_monitoring_alerts,
			'penalties_incurred': penalties_incurred,
			'audits_conducted': audits_conducted,
			'compliance_violations': compliance_violations,
			'reported_date': reported_date,
			'compliance_training_sessions': compliance_training_sessions,
			'training_attendees': training_attendees,
			'compliance_comments': compliance_comments,}
            data['code']=code

            data['record_type']='update'
            # Initialize the serializer with the data
            serializer_temp = ComplianceTempSerializer(data=data)
            #serializer_live=ComplianceLiveSerializer(data=data)
            
            # Validate and save the serializer data
            if serializer_temp.is_valid() :
                temp_instance = serializer_temp.save()
                type=temp_instance.record_type
                # Call auditing and authorization functions if needed
                is_audit = model_audit(request,APP_NAME,'Compliance',temp_instance.pk)
                is_authorization = self_authorization(request,APP_NAME,'Compliance', temp_instance.pk,type)

                model_name='Compliance'
                record_id=temp_instance.pk
                # type=temp_instance.record_type
                user_ids_resp=get_next_user_from_work_flow(request,model_name,temp_instance=record_id,type=type)
 
                return success(f'Successfully updated {temp_instance} Temp ')
            
            else:
                errors = {
                    'temp_errors': serializer_temp.errors,
                    #'live_errors': serializer_live.errors,
                }
                return error(f"Error: {errors}")
        else:
            return error('you have no permission to update the record')
        return success('Successfully stored in the temp table')
    except  ComplianceTemp.DoesNotExist:
        return error('Instance does not exist')
    except ValidationError as e:
        return error(f"Validation Error: {e}")
    except Exception as e:
        return error(f"An error occurred: {e}")



def view_compliance(compliance_id=None):
    """
    Retrieves and serializes a Compliance instance by its ID or all instances if ID is None.
    
    Args:
        Compliance_id (int, optional): ID of the Compliance to retrieve.

    Returns:
        dict: A success response with the serialized data if found,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if compliance_id is not None:
            record = ComplianceTemp.objects.get(pk=compliance_id)
            serializer = ComplianceTempSerializer(record)
        else:
            obj = ComplianceLive.objects.filter(is_deactivate=False)
            obj_pa = get_temp_record(request,APP_NAME,'Compliance').filter(~Q(status='unauthorized_sent'))
            print('object--',obj_pa)
            obj_wait_auth = get_record_for_authorize(str(request.user.pk))
            # records = NoSeriesLinesALive.objects.all()
            live_data = ComplianceLiveSerializer(obj, many=True).data
            temp_data = ComplianceTempSerializer(obj_pa, many=True).data
            auth_request=AuthorizeRequestSerializer(obj_wait_auth,many=True).data
            serializer={
                'obj':live_data,
                'obj_pa':temp_data,
                'auth_request':auth_request
            }
        return success(serializer)
    
    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")


def view_compliance_single(code):
    """
    Retrieves and serializes a NoSeriesLinesA instance by its ID or all instances if ID is None.
    
    Args:
        NoSeriesLinesA_id (int, optional): ID of the NoSeriesLinesA to retrieve.

    Returns:
        dict: A success response with the serialized data if found,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        

        record = ComplianceLive.objects.get(pk=code)
        serializer = ComplianceLiveSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")


def pa_compliance(compliance_id,model_name):
    """
    Retrieves and serializes a NoSeriesLinesA instance by its ID or all instances if ID is None.
    
    Args:
        NoSeriesLinesA_id (int, optional): ID of the NoSeriesLinesA to retrieve.

    Returns:
        dict: A success response with the serialized data if found,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        record = ComplianceTemp.objects.get(pk=compliance_id)
        serializer = ComplianceTempPASerializer(record).data
        
        type=record.record_type
        get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
        serializers=ModelRegistrationSerializer(get_table_name).data

        workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
        serializers_data=WorkflowMappingSerializer(workflow_mapping).data

        data={
            'compliance':serializer,
            'table_data':serializers,
            'workflow_data':serializers_data
        }
        return success(data)
    
    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def delete_compliance(compliance_id,model_name):
    """
    Deletes a Compliance instance with the given ID.
    
    Args:
        compliance_id (int): ID of the Compliance to delete.

    Returns:
        dict: A success response if deletion is successful,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        if  is_have_permission(request,APP_NAME, 'Compliance', compliance_id):
            type='delete'

            is_authorization = self_authorization_for_delete(request,APP_NAME,model_name, compliance_id,type)
            user_ids_resp=get_next_user_from_work_flow(request,model_name,temp_instance=compliance_id,type=type)
 
            sent_auth=WorkflowMapping.objects.get(table_name__model_name__iexact=model_name,workflow_type=type)
            
            record = ComplianceLive.objects.get(pk=compliance_id)
            serializer = ComplianceLiveViewSerializer(record).data

            # get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
            # serializers=ModelRegistrationSerializer(get_table_name).data

            get_table_name = ModelRegistration.objects.get(model_name=model_name)
            serializers=ModelRegistrationSerializer(get_table_name).data

            print('table name of current',get_table_name)
            
            workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
            serializers_data=WorkflowMappingSerializer(workflow_mapping).data

            if user_ids_resp is not None and sent_auth.send_to_authorized == 'False' and sent_auth.same_user_authorized == 'False':

                obj = delete_record(request,APP_NAME, 'Compliance', compliance_id)
                return success("Successfully deleted")
            else:
                data={
                    'Compliance':serializer,
                    'table_data':serializers,
                    'workflow_data':serializers_data
                }
                return success(data)
        else:
            return error('you have no permission to delete the record')
    
    except ComplianceLive.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def view_compliance_tempdata(compliance_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = ComplianceTemp.objects.get(code=compliance_id)
        serializer = ComplianceTempSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")
    

def view_compliance_live(compliance_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = ComplianceLive.objects.get(code=compliance_id)
        serializer = ComplianceLiveViewSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def authorize_request_data_Compliance(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=ComplianceTemp.objects.get(pk=pk)
        work_flow_type=get_instance.record_type
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,work_flow_type)
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()

        return success(req)
    
    except ComplianceTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def authorize_request_data_delete_Compliance(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=ComplianceLive.objects.get(pk=pk)
  
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,type='delete')
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()
        return success(req)
    
    except ComplianceTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")





#add foreign key import model.


def create_fraudmonitoring(detected_fraud_incidents, total_amount_involved, resolution_status_percentage, open_fraud_cases, fraud_detection_methods, reported_date, fraud_prevention_actions, investigation_comments):
    """
    Creates a FraudMonitoring instance with the provided data.
        Args:
        detected_fraud_incidents, total_amount_involved, resolution_status_percentage, open_fraud_cases, fraud_detection_methods, reported_date, fraud_prevention_actions, investigation_comments: Keyword arguments for FraudMonitoring fields.

    Returns:
        dict: Success or error message.
        APP_NAME = __name__.split('.')[0]

    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        data={'detected_fraud_incidents': detected_fraud_incidents,
			'total_amount_involved': total_amount_involved,
			'resolution_status_percentage': resolution_status_percentage,
			'open_fraud_cases': open_fraud_cases,
			'fraud_detection_methods': fraud_detection_methods,
			'reported_date': reported_date,
			'fraud_prevention_actions': fraud_prevention_actions,
			'investigation_comments': investigation_comments,}
        data['code'] = generate_random_id('ABC')
        data_create = data.copy()
        data_create['code'] = generate_random_id('ABC')
        data_create['record_type']='create'
        # Initialize the serializer with the data
        serializer_temp = FraudMonitoringTempSerializer(data=data_create)
        serializer_live=FraudMonitoringLiveSerializer(data=data)
        
        # Validate and save the serializer data
        if serializer_live.is_valid() and serializer_temp.is_valid() :
            temp_instance = serializer_temp.save()
            type=temp_instance.record_type
            # Call auditing and authorization functions if needed
            is_audit = model_audit(request,APP_NAME,'FraudMonitoring',temp_instance.pk)
            is_authorization = self_authorization(request,APP_NAME,'FraudMonitoring', temp_instance.pk,type)
            
            model_name='FraudMonitoring'
            record_id=temp_instance.pk
            # type=temp_instance.record_type
            
            user_ids_resp=get_next_user_from_work_flow(request,model_name,temp_instance=record_id,type=type)
            if user_ids_resp is None:
                return success(f'Successfully created {temp_instance} Temp ')
     
        else:
            errors = {
                'temp_errors': serializer_temp.errors,
                'live_errors': serializer_live.errors,
            }
            return error(f"Error: {errors}")
    except ValidationError as e:
        return error(f"Validation Error: {e}")
    except Exception as e:
        return error(f"An error occurred: {e}")

def update_fraudmonitoring_temp(code,detected_fraud_incidents=None, total_amount_involved=None, resolution_status_percentage=None, open_fraud_cases=None, fraud_detection_methods=None, reported_date=None, fraud_prevention_actions=None, investigation_comments=None):
    """
    Updates a FraudMonitoring instance with the provided data.
    
    Args:
        fraudmonitoring_id (int): ID of the FraudMonitoring to update.
        detected_fraud_incidents=None, total_amount_involved=None, resolution_status_percentage=None, open_fraud_cases=None, fraud_detection_methods=None, reported_date=None, fraud_prevention_actions=None, investigation_comments=None: Keyword arguments for FraudMonitoring fields to update.

    Returns:
        dict: Success or error message.
    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if  is_have_permission(request,APP_NAME, 'FraudMonitoring',code):

            data={'detected_fraud_incidents': detected_fraud_incidents,
			'total_amount_involved': total_amount_involved,
			'resolution_status_percentage': resolution_status_percentage,
			'open_fraud_cases': open_fraud_cases,
			'fraud_detection_methods': fraud_detection_methods,
			'reported_date': reported_date,
			'fraud_prevention_actions': fraud_prevention_actions,
			'investigation_comments': investigation_comments,}
            data['code']=code

            data['record_type']='update'
            # Initialize the serializer with the data
            serializer_temp = FraudMonitoringTempSerializer(data=data)
            #serializer_live=FraudMonitoringLiveSerializer(data=data)
            
            # Validate and save the serializer data
            if serializer_temp.is_valid() :
                temp_instance = serializer_temp.save()
                type=temp_instance.record_type
                # Call auditing and authorization functions if needed
                is_audit = model_audit(request,APP_NAME,'FraudMonitoring',temp_instance.pk)
                is_authorization = self_authorization(request,APP_NAME,'FraudMonitoring', temp_instance.pk,type)

                model_name='FraudMonitoring'
                record_id=temp_instance.pk
                # type=temp_instance.record_type
                user_ids_resp=get_next_user_from_work_flow(request,model_name,temp_instance=record_id,type=type)
 
                return success(f'Successfully updated {temp_instance} Temp ')
            
            else:
                errors = {
                    'temp_errors': serializer_temp.errors,
                    #'live_errors': serializer_live.errors,
                }
                return error(f"Error: {errors}")
        else:
            return error('you have no permission to update the record')
        return success('Successfully stored in the temp table')
    except  FraudMonitoringTemp.DoesNotExist:
        return error('Instance does not exist')
    except ValidationError as e:
        return error(f"Validation Error: {e}")
    except Exception as e:
        return error(f"An error occurred: {e}")



def view_fraudmonitoring(fraudmonitoring_id=None):
    """
    Retrieves and serializes a FraudMonitoring instance by its ID or all instances if ID is None.
    
    Args:
        FraudMonitoring_id (int, optional): ID of the FraudMonitoring to retrieve.

    Returns:
        dict: A success response with the serialized data if found,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if fraudmonitoring_id is not None:
            record = FraudMonitoringTemp.objects.get(pk=fraudmonitoring_id)
            serializer = FraudMonitoringTempSerializer(record)
        else:
            obj = FraudMonitoringLive.objects.filter(is_deactivate=False)
            obj_pa = get_temp_record(request,APP_NAME,'FraudMonitoring').filter(~Q(status='unauthorized_sent'))
            print('object--',obj_pa)
            obj_wait_auth = get_record_for_authorize(str(request.user.pk))
            # records = NoSeriesLinesALive.objects.all()
            live_data = FraudMonitoringLiveSerializer(obj, many=True).data
            temp_data = FraudMonitoringTempSerializer(obj_pa, many=True).data
            auth_request=AuthorizeRequestSerializer(obj_wait_auth,many=True).data
            serializer={
                'obj':live_data,
                'obj_pa':temp_data,
                'auth_request':auth_request
            }
        return success(serializer)
    
    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")


def view_fraudmonitoring_single(code):
    """
    Retrieves and serializes a NoSeriesLinesA instance by its ID or all instances if ID is None.
    
    Args:
        NoSeriesLinesA_id (int, optional): ID of the NoSeriesLinesA to retrieve.

    Returns:
        dict: A success response with the serialized data if found,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        

        record = FraudMonitoringLive.objects.get(pk=code)
        serializer = FraudMonitoringLiveSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")


def pa_fraudmonitoring(fraudmonitoring_id,model_name):
    """
    Retrieves and serializes a NoSeriesLinesA instance by its ID or all instances if ID is None.
    
    Args:
        NoSeriesLinesA_id (int, optional): ID of the NoSeriesLinesA to retrieve.

    Returns:
        dict: A success response with the serialized data if found,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        record = FraudMonitoringTemp.objects.get(pk=fraudmonitoring_id)
        serializer = FraudMonitoringTempPASerializer(record).data
        
        type=record.record_type
        get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
        serializers=ModelRegistrationSerializer(get_table_name).data

        workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
        serializers_data=WorkflowMappingSerializer(workflow_mapping).data

        data={
            'fraudmonitoring':serializer,
            'table_data':serializers,
            'workflow_data':serializers_data
        }
        return success(data)
    
    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def delete_fraudmonitoring(fraudmonitoring_id,model_name):
    """
    Deletes a FraudMonitoring instance with the given ID.
    
    Args:
        fraudmonitoring_id (int): ID of the FraudMonitoring to delete.

    Returns:
        dict: A success response if deletion is successful,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        if  is_have_permission(request,APP_NAME, 'FraudMonitoring', fraudmonitoring_id):
            type='delete'

            is_authorization = self_authorization_for_delete(request,APP_NAME,model_name, fraudmonitoring_id,type)
            user_ids_resp=get_next_user_from_work_flow(request,model_name,temp_instance=fraudmonitoring_id,type=type)
 
            sent_auth=WorkflowMapping.objects.get(table_name__model_name__iexact=model_name,workflow_type=type)
            
            record = FraudMonitoringLive.objects.get(pk=fraudmonitoring_id)
            serializer = FraudMonitoringLiveViewSerializer(record).data

            # get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
            # serializers=ModelRegistrationSerializer(get_table_name).data

            get_table_name = ModelRegistration.objects.get(model_name=model_name)
            serializers=ModelRegistrationSerializer(get_table_name).data

            print('table name of current',get_table_name)
            
            workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
            serializers_data=WorkflowMappingSerializer(workflow_mapping).data

            if user_ids_resp is not None and sent_auth.send_to_authorized == 'False' and sent_auth.same_user_authorized == 'False':

                obj = delete_record(request,APP_NAME, 'FraudMonitoring', fraudmonitoring_id)
                return success("Successfully deleted")
            else:
                data={
                    'FraudMonitoring':serializer,
                    'table_data':serializers,
                    'workflow_data':serializers_data
                }
                return success(data)
        else:
            return error('you have no permission to delete the record')
    
    except FraudMonitoringLive.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def view_fraudmonitoring_tempdata(fraudmonitoring_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = FraudMonitoringTemp.objects.get(code=fraudmonitoring_id)
        serializer = FraudMonitoringTempSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")
    

def view_fraudmonitoring_live(fraudmonitoring_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = FraudMonitoringLive.objects.get(code=fraudmonitoring_id)
        serializer = FraudMonitoringLiveViewSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def authorize_request_data_FraudMonitoring(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=FraudMonitoringTemp.objects.get(pk=pk)
        work_flow_type=get_instance.record_type
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,work_flow_type)
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()

        return success(req)
    
    except FraudMonitoringTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def authorize_request_data_delete_FraudMonitoring(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=FraudMonitoringLive.objects.get(pk=pk)
  
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,type='delete')
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()
        return success(req)
    
    except FraudMonitoringTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")





#add foreign key import model.


def create_riskassessment(top_risks, mitigation_actions, residual_risk_level, risk_review_frequency, reported_date, incidents_tracked, risk_owner, risk_comments):
    """
    Creates a RiskAssessment instance with the provided data.
        Args:
        top_risks, mitigation_actions, residual_risk_level, risk_review_frequency, reported_date, incidents_tracked, risk_owner, risk_comments: Keyword arguments for RiskAssessment fields.

    Returns:
        dict: Success or error message.
        APP_NAME = __name__.split('.')[0]

    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        data={'top_risks': top_risks,
			'mitigation_actions': mitigation_actions,
			'residual_risk_level': residual_risk_level,
			'risk_review_frequency': risk_review_frequency,
			'reported_date': reported_date,
			'incidents_tracked': incidents_tracked,
			'risk_owner': risk_owner,
			'risk_comments': risk_comments,}
        data['code'] = generate_random_id('ABC')
        data_create = data.copy()
        data_create['code'] = generate_random_id('ABC')
        data_create['record_type']='create'
        # Initialize the serializer with the data
        serializer_temp = RiskAssessmentTempSerializer(data=data_create)
        serializer_live=RiskAssessmentLiveSerializer(data=data)
        
        # Validate and save the serializer data
        if serializer_live.is_valid() and serializer_temp.is_valid() :
            temp_instance = serializer_temp.save()
            type=temp_instance.record_type
            # Call auditing and authorization functions if needed
            is_audit = model_audit(request,APP_NAME,'RiskAssessment',temp_instance.pk)
            is_authorization = self_authorization(request,APP_NAME,'RiskAssessment', temp_instance.pk,type)
            
            model_name='RiskAssessment'
            record_id=temp_instance.pk
            # type=temp_instance.record_type
            
            user_ids_resp=get_next_user_from_work_flow(request,model_name,temp_instance=record_id,type=type)
            if user_ids_resp is None:
                return success(f'Successfully created {temp_instance} Temp ')
     
        else:
            errors = {
                'temp_errors': serializer_temp.errors,
                'live_errors': serializer_live.errors,
            }
            return error(f"Error: {errors}")
    except ValidationError as e:
        return error(f"Validation Error: {e}")
    except Exception as e:
        return error(f"An error occurred: {e}")

def update_riskassessment_temp(code,top_risks=None, mitigation_actions=None, residual_risk_level=None, risk_review_frequency=None, reported_date=None, incidents_tracked=None, risk_owner=None, risk_comments=None):
    """
    Updates a RiskAssessment instance with the provided data.
    
    Args:
        riskassessment_id (int): ID of the RiskAssessment to update.
        top_risks=None, mitigation_actions=None, residual_risk_level=None, risk_review_frequency=None, reported_date=None, incidents_tracked=None, risk_owner=None, risk_comments=None: Keyword arguments for RiskAssessment fields to update.

    Returns:
        dict: Success or error message.
    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if  is_have_permission(request,APP_NAME, 'RiskAssessment',code):

            data={'top_risks': top_risks,
			'mitigation_actions': mitigation_actions,
			'residual_risk_level': residual_risk_level,
			'risk_review_frequency': risk_review_frequency,
			'reported_date': reported_date,
			'incidents_tracked': incidents_tracked,
			'risk_owner': risk_owner,
			'risk_comments': risk_comments,}
            data['code']=code

            data['record_type']='update'
            # Initialize the serializer with the data
            serializer_temp = RiskAssessmentTempSerializer(data=data)
            #serializer_live=RiskAssessmentLiveSerializer(data=data)
            
            # Validate and save the serializer data
            if serializer_temp.is_valid() :
                temp_instance = serializer_temp.save()
                type=temp_instance.record_type
                # Call auditing and authorization functions if needed
                is_audit = model_audit(request,APP_NAME,'RiskAssessment',temp_instance.pk)
                is_authorization = self_authorization(request,APP_NAME,'RiskAssessment', temp_instance.pk,type)

                model_name='RiskAssessment'
                record_id=temp_instance.pk
                # type=temp_instance.record_type
                user_ids_resp=get_next_user_from_work_flow(request,model_name,temp_instance=record_id,type=type)
 
                return success(f'Successfully updated {temp_instance} Temp ')
            
            else:
                errors = {
                    'temp_errors': serializer_temp.errors,
                    #'live_errors': serializer_live.errors,
                }
                return error(f"Error: {errors}")
        else:
            return error('you have no permission to update the record')
        return success('Successfully stored in the temp table')
    except  RiskAssessmentTemp.DoesNotExist:
        return error('Instance does not exist')
    except ValidationError as e:
        return error(f"Validation Error: {e}")
    except Exception as e:
        return error(f"An error occurred: {e}")



def view_riskassessment(riskassessment_id=None):
    """
    Retrieves and serializes a RiskAssessment instance by its ID or all instances if ID is None.
    
    Args:
        RiskAssessment_id (int, optional): ID of the RiskAssessment to retrieve.

    Returns:
        dict: A success response with the serialized data if found,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if riskassessment_id is not None:
            record = RiskAssessmentTemp.objects.get(pk=riskassessment_id)
            serializer = RiskAssessmentTempSerializer(record)
        else:
            obj = RiskAssessmentLive.objects.filter(is_deactivate=False)
            obj_pa = get_temp_record(request,APP_NAME,'RiskAssessment').filter(~Q(status='unauthorized_sent'))
            print('object--',obj_pa)
            obj_wait_auth = get_record_for_authorize(str(request.user.pk))
            # records = NoSeriesLinesALive.objects.all()
            live_data = RiskAssessmentLiveSerializer(obj, many=True).data
            temp_data = RiskAssessmentTempSerializer(obj_pa, many=True).data
            auth_request=AuthorizeRequestSerializer(obj_wait_auth,many=True).data
            serializer={
                'obj':live_data,
                'obj_pa':temp_data,
                'auth_request':auth_request
            }
        return success(serializer)
    
    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")


def view_riskassessment_single(code):
    """
    Retrieves and serializes a NoSeriesLinesA instance by its ID or all instances if ID is None.
    
    Args:
        NoSeriesLinesA_id (int, optional): ID of the NoSeriesLinesA to retrieve.

    Returns:
        dict: A success response with the serialized data if found,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        

        record = RiskAssessmentLive.objects.get(pk=code)
        serializer = RiskAssessmentLiveSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")


def pa_riskassessment(riskassessment_id,model_name):
    """
    Retrieves and serializes a NoSeriesLinesA instance by its ID or all instances if ID is None.
    
    Args:
        NoSeriesLinesA_id (int, optional): ID of the NoSeriesLinesA to retrieve.

    Returns:
        dict: A success response with the serialized data if found,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        record = RiskAssessmentTemp.objects.get(pk=riskassessment_id)
        serializer = RiskAssessmentTempPASerializer(record).data
        
        type=record.record_type
        get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
        serializers=ModelRegistrationSerializer(get_table_name).data

        workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
        serializers_data=WorkflowMappingSerializer(workflow_mapping).data

        data={
            'riskassessment':serializer,
            'table_data':serializers,
            'workflow_data':serializers_data
        }
        return success(data)
    
    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def delete_riskassessment(riskassessment_id,model_name):
    """
    Deletes a RiskAssessment instance with the given ID.
    
    Args:
        riskassessment_id (int): ID of the RiskAssessment to delete.

    Returns:
        dict: A success response if deletion is successful,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        if  is_have_permission(request,APP_NAME, 'RiskAssessment', riskassessment_id):
            type='delete'

            is_authorization = self_authorization_for_delete(request,APP_NAME,model_name, riskassessment_id,type)
            user_ids_resp=get_next_user_from_work_flow(request,model_name,temp_instance=riskassessment_id,type=type)
 
            sent_auth=WorkflowMapping.objects.get(table_name__model_name__iexact=model_name,workflow_type=type)
            
            record = RiskAssessmentLive.objects.get(pk=riskassessment_id)
            serializer = RiskAssessmentLiveViewSerializer(record).data

            # get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
            # serializers=ModelRegistrationSerializer(get_table_name).data

            get_table_name = ModelRegistration.objects.get(model_name=model_name)
            serializers=ModelRegistrationSerializer(get_table_name).data

            print('table name of current',get_table_name)
            
            workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
            serializers_data=WorkflowMappingSerializer(workflow_mapping).data

            if user_ids_resp is not None and sent_auth.send_to_authorized == 'False' and sent_auth.same_user_authorized == 'False':

                obj = delete_record(request,APP_NAME, 'RiskAssessment', riskassessment_id)
                return success("Successfully deleted")
            else:
                data={
                    'RiskAssessment':serializer,
                    'table_data':serializers,
                    'workflow_data':serializers_data
                }
                return success(data)
        else:
            return error('you have no permission to delete the record')
    
    except RiskAssessmentLive.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def view_riskassessment_tempdata(riskassessment_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = RiskAssessmentTemp.objects.get(code=riskassessment_id)
        serializer = RiskAssessmentTempSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")
    

def view_riskassessment_live(riskassessment_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = RiskAssessmentLive.objects.get(code=riskassessment_id)
        serializer = RiskAssessmentLiveViewSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def authorize_request_data_RiskAssessment(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=RiskAssessmentTemp.objects.get(pk=pk)
        work_flow_type=get_instance.record_type
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,work_flow_type)
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()

        return success(req)
    
    except RiskAssessmentTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def authorize_request_data_delete_RiskAssessment(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=RiskAssessmentLive.objects.get(pk=pk)
  
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,type='delete')
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()
        return success(req)
    
    except RiskAssessmentTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")





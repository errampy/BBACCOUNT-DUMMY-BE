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
from human_resources_department.models import *
from administration_department.models import *
from aging_reports.models import *
from aging_reports.serializers import *
from financial_department.models import *
from mainapp.models import *
from marketingand_customer_relations_department.models import *
from operations_department.models import *
from riskand_compliance_department.models import *
from riskand_compliance_department.serializers import *
from financial_department.serializers import *
from operations_department.serializers import *
from administration_department.serializers import  *
from marketingand_customer_relations_department.serializers import *
from human_resources_department.serializers import *


APP_NAME = __name__.split('.')[0]



#add foreign key import model.


def create_dataaccuracy(errors_detected, corrected_entries_percentage, audit_frequency, system_generated_errors, reported_date, manual_input_errors, critical_errors, accuracy_comments):
    """
    Creates a DataAccuracy instance with the provided data.
        Args:
        errors_detected, corrected_entries_percentage, audit_frequency, system_generated_errors, reported_date, manual_input_errors, critical_errors, accuracy_comments: Keyword arguments for DataAccuracy fields.

    Returns:
        dict: Success or error message.
        APP_NAME = __name__.split('.')[0]

    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        data={'errors_detected': errors_detected,
			'corrected_entries_percentage': corrected_entries_percentage,
			'audit_frequency': audit_frequency,
			'system_generated_errors': system_generated_errors,
			'reported_date': reported_date,
			'manual_input_errors': manual_input_errors,
			'critical_errors': critical_errors,
			'accuracy_comments': accuracy_comments,}
        data['code'] = generate_random_id('ABC')
        data_create = data.copy()
        data_create['code'] = generate_random_id('ABC')
        data_create['record_type']='create'
        # Initialize the serializer with the data
        serializer_temp = DataAccuracyTempSerializer(data=data_create)
        serializer_live=DataAccuracyLiveSerializer(data=data)
        
        # Validate and save the serializer data
        if serializer_live.is_valid() and serializer_temp.is_valid() :
            temp_instance = serializer_temp.save()
            type=temp_instance.record_type
            # Call auditing and authorization functions if needed
            is_audit = model_audit(request,APP_NAME,'DataAccuracy',temp_instance.pk)
            is_authorization = self_authorization(request,APP_NAME,'DataAccuracy', temp_instance.pk,type)
            
            model_name='DataAccuracy'
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

def update_dataaccuracy_temp(code,errors_detected=None, corrected_entries_percentage=None, audit_frequency=None, system_generated_errors=None, reported_date=None, manual_input_errors=None, critical_errors=None, accuracy_comments=None):
    """
    Updates a DataAccuracy instance with the provided data.
    
    Args:
        dataaccuracy_id (int): ID of the DataAccuracy to update.
        errors_detected=None, corrected_entries_percentage=None, audit_frequency=None, system_generated_errors=None, reported_date=None, manual_input_errors=None, critical_errors=None, accuracy_comments=None: Keyword arguments for DataAccuracy fields to update.

    Returns:
        dict: Success or error message.
    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if  is_have_permission(request,APP_NAME, 'DataAccuracy',code):

            data={'errors_detected': errors_detected,
			'corrected_entries_percentage': corrected_entries_percentage,
			'audit_frequency': audit_frequency,
			'system_generated_errors': system_generated_errors,
			'reported_date': reported_date,
			'manual_input_errors': manual_input_errors,
			'critical_errors': critical_errors,
			'accuracy_comments': accuracy_comments,}
            data['code']=code

            data['record_type']='update'
            # Initialize the serializer with the data
            serializer_temp = DataAccuracyTempSerializer(data=data)
            #serializer_live=DataAccuracyLiveSerializer(data=data)
            
            # Validate and save the serializer data
            if serializer_temp.is_valid() :
                temp_instance = serializer_temp.save()
                type=temp_instance.record_type
                # Call auditing and authorization functions if needed
                is_audit = model_audit(request,APP_NAME,'DataAccuracy',temp_instance.pk)
                is_authorization = self_authorization(request,APP_NAME,'DataAccuracy', temp_instance.pk,type)

                model_name='DataAccuracy'
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
    except  DataAccuracyTemp.DoesNotExist:
        return error('Instance does not exist')
    except ValidationError as e:
        return error(f"Validation Error: {e}")
    except Exception as e:
        return error(f"An error occurred: {e}")



def view_dataaccuracy(dataaccuracy_id=None):
    """
    Retrieves and serializes a DataAccuracy instance by its ID or all instances if ID is None.
    
    Args:
        DataAccuracy_id (int, optional): ID of the DataAccuracy to retrieve.

    Returns:
        dict: A success response with the serialized data if found,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if dataaccuracy_id is not None:
            record = DataAccuracyTemp.objects.get(pk=dataaccuracy_id)
            serializer = DataAccuracyTempSerializer(record)
        else:
            obj = DataAccuracyLive.objects.filter(is_deactivate=False)
            obj_pa = get_temp_record(request,APP_NAME,'DataAccuracy').filter(~Q(status='unauthorized_sent'))
            print('object--',obj_pa)
            obj_wait_auth = get_record_for_authorize(str(request.user.pk))
            # records = NoSeriesLinesALive.objects.all()
            live_data = DataAccuracyLiveSerializer(obj, many=True).data
            temp_data = DataAccuracyTempSerializer(obj_pa, many=True).data
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


def view_dataaccuracy_single(code):
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
        

        record = DataAccuracyLive.objects.get(pk=code)
        serializer = DataAccuracyLiveSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")


def pa_dataaccuracy(dataaccuracy_id,model_name):
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
        
        record = DataAccuracyTemp.objects.get(pk=dataaccuracy_id)
        serializer = DataAccuracyTempPASerializer(record).data
        
        type=record.record_type
        get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
        serializers=ModelRegistrationSerializer(get_table_name).data

        workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
        serializers_data=WorkflowMappingSerializer(workflow_mapping).data

        data={
            'dataaccuracy':serializer,
            'table_data':serializers,
            'workflow_data':serializers_data
        }
        return success(data)
    
    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def delete_dataaccuracy(dataaccuracy_id,model_name):
    """
    Deletes a DataAccuracy instance with the given ID.
    
    Args:
        dataaccuracy_id (int): ID of the DataAccuracy to delete.

    Returns:
        dict: A success response if deletion is successful,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        if  is_have_permission(request,APP_NAME, 'DataAccuracy', dataaccuracy_id):
            type='delete'

            is_authorization = self_authorization_for_delete(request,APP_NAME,model_name, dataaccuracy_id,type)
            user_ids_resp=get_next_user_from_work_flow(request,model_name,temp_instance=dataaccuracy_id,type=type)
 
            sent_auth=WorkflowMapping.objects.get(table_name__model_name__iexact=model_name,workflow_type=type)
            
            record = DataAccuracyLive.objects.get(pk=dataaccuracy_id)
            serializer = DataAccuracyLiveViewSerializer(record).data

            # get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
            # serializers=ModelRegistrationSerializer(get_table_name).data

            get_table_name = ModelRegistration.objects.get(model_name=model_name)
            serializers=ModelRegistrationSerializer(get_table_name).data

            print('table name of current',get_table_name)
            
            workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
            serializers_data=WorkflowMappingSerializer(workflow_mapping).data

            if user_ids_resp is not None and sent_auth.send_to_authorized == 'False' and sent_auth.same_user_authorized == 'False':

                obj = delete_record(request,APP_NAME, 'DataAccuracy', dataaccuracy_id)
                return success("Successfully deleted")
            else:
                data={
                    'DataAccuracy':serializer,
                    'table_data':serializers,
                    'workflow_data':serializers_data
                }
                return success(data)
        else:
            return error('you have no permission to delete the record')
    
    except DataAccuracyLive.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def view_dataaccuracy_tempdata(dataaccuracy_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = DataAccuracyTemp.objects.get(code=dataaccuracy_id)
        serializer = DataAccuracyTempSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")
    

def view_dataaccuracy_live(dataaccuracy_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = DataAccuracyLive.objects.get(code=dataaccuracy_id)
        serializer = DataAccuracyLiveViewSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def authorize_request_data_DataAccuracy(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=DataAccuracyTemp.objects.get(pk=pk)
        work_flow_type=get_instance.record_type
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,work_flow_type)
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()

        return success(req)
    
    except DataAccuracyTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def authorize_request_data_delete_DataAccuracy(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=DataAccuracyLive.objects.get(pk=pk)
  
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,type='delete')
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()
        return success(req)
    
    except DataAccuracyTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")





#add foreign key import model.


def create_systemuptime(total_downtime_hours, uptime_percentage, scheduled_maintenance_hours, unscheduled_outage_hours, critical_systems_affected, reported_date, system_comments):
    """
    Creates a SystemUptime instance with the provided data.
        Args:
        total_downtime_hours, uptime_percentage, scheduled_maintenance_hours, unscheduled_outage_hours, critical_systems_affected, reported_date, system_comments: Keyword arguments for SystemUptime fields.

    Returns:
        dict: Success or error message.
        APP_NAME = __name__.split('.')[0]

    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        data={'total_downtime_hours': total_downtime_hours,
			'uptime_percentage': uptime_percentage,
			'scheduled_maintenance_hours': scheduled_maintenance_hours,
			'unscheduled_outage_hours': unscheduled_outage_hours,
			'critical_systems_affected': critical_systems_affected,
			'reported_date': reported_date,
			'system_comments': system_comments,}
        data['code'] = generate_random_id('ABC')
        data_create = data.copy()
        data_create['code'] = generate_random_id('ABC')
        data_create['record_type']='create'
        # Initialize the serializer with the data
        serializer_temp = SystemUptimeTempSerializer(data=data_create)
        serializer_live=SystemUptimeLiveSerializer(data=data)
        
        # Validate and save the serializer data
        if serializer_live.is_valid() and serializer_temp.is_valid() :
            temp_instance = serializer_temp.save()
            type=temp_instance.record_type
            # Call auditing and authorization functions if needed
            is_audit = model_audit(request,APP_NAME,'SystemUptime',temp_instance.pk)
            is_authorization = self_authorization(request,APP_NAME,'SystemUptime', temp_instance.pk,type)
            
            model_name='SystemUptime'
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

def update_systemuptime_temp(code,total_downtime_hours=None, uptime_percentage=None, scheduled_maintenance_hours=None, unscheduled_outage_hours=None, critical_systems_affected=None, reported_date=None, system_comments=None):
    """
    Updates a SystemUptime instance with the provided data.
    
    Args:
        systemuptime_id (int): ID of the SystemUptime to update.
        total_downtime_hours=None, uptime_percentage=None, scheduled_maintenance_hours=None, unscheduled_outage_hours=None, critical_systems_affected=None, reported_date=None, system_comments=None: Keyword arguments for SystemUptime fields to update.

    Returns:
        dict: Success or error message.
    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if  is_have_permission(request,APP_NAME, 'SystemUptime',code):

            data={'total_downtime_hours': total_downtime_hours,
			'uptime_percentage': uptime_percentage,
			'scheduled_maintenance_hours': scheduled_maintenance_hours,
			'unscheduled_outage_hours': unscheduled_outage_hours,
			'critical_systems_affected': critical_systems_affected,
			'reported_date': reported_date,
			'system_comments': system_comments,}
            data['code']=code

            data['record_type']='update'
            # Initialize the serializer with the data
            serializer_temp = SystemUptimeTempSerializer(data=data)
            #serializer_live=SystemUptimeLiveSerializer(data=data)
            
            # Validate and save the serializer data
            if serializer_temp.is_valid() :
                temp_instance = serializer_temp.save()
                type=temp_instance.record_type
                # Call auditing and authorization functions if needed
                is_audit = model_audit(request,APP_NAME,'SystemUptime',temp_instance.pk)
                is_authorization = self_authorization(request,APP_NAME,'SystemUptime', temp_instance.pk,type)

                model_name='SystemUptime'
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
    except  SystemUptimeTemp.DoesNotExist:
        return error('Instance does not exist')
    except ValidationError as e:
        return error(f"Validation Error: {e}")
    except Exception as e:
        return error(f"An error occurred: {e}")



def view_systemuptime(systemuptime_id=None):
    """
    Retrieves and serializes a SystemUptime instance by its ID or all instances if ID is None.
    
    Args:
        SystemUptime_id (int, optional): ID of the SystemUptime to retrieve.

    Returns:
        dict: A success response with the serialized data if found,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if systemuptime_id is not None:
            record = SystemUptimeTemp.objects.get(pk=systemuptime_id)
            serializer = SystemUptimeTempSerializer(record)
        else:
            obj = SystemUptimeLive.objects.filter(is_deactivate=False)
            obj_pa = get_temp_record(request,APP_NAME,'SystemUptime').filter(~Q(status='unauthorized_sent'))
            print('object--',obj_pa)
            obj_wait_auth = get_record_for_authorize(str(request.user.pk))
            # records = NoSeriesLinesALive.objects.all()
            live_data = SystemUptimeLiveSerializer(obj, many=True).data
            temp_data = SystemUptimeTempSerializer(obj_pa, many=True).data
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


def view_systemuptime_single(code):
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
        

        record = SystemUptimeLive.objects.get(pk=code)
        serializer = SystemUptimeLiveSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")


def pa_systemuptime(systemuptime_id,model_name):
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
        
        record = SystemUptimeTemp.objects.get(pk=systemuptime_id)
        serializer = SystemUptimeTempPASerializer(record).data
        
        type=record.record_type
        get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
        serializers=ModelRegistrationSerializer(get_table_name).data

        workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
        serializers_data=WorkflowMappingSerializer(workflow_mapping).data

        data={
            'systemuptime':serializer,
            'table_data':serializers,
            'workflow_data':serializers_data
        }
        return success(data)
    
    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def delete_systemuptime(systemuptime_id,model_name):
    """
    Deletes a SystemUptime instance with the given ID.
    
    Args:
        systemuptime_id (int): ID of the SystemUptime to delete.

    Returns:
        dict: A success response if deletion is successful,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        if  is_have_permission(request,APP_NAME, 'SystemUptime', systemuptime_id):
            type='delete'

            is_authorization = self_authorization_for_delete(request,APP_NAME,model_name, systemuptime_id,type)
            user_ids_resp=get_next_user_from_work_flow(request,model_name,temp_instance=systemuptime_id,type=type)
 
            sent_auth=WorkflowMapping.objects.get(table_name__model_name__iexact=model_name,workflow_type=type)
            
            record = SystemUptimeLive.objects.get(pk=systemuptime_id)
            serializer = SystemUptimeLiveViewSerializer(record).data

            # get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
            # serializers=ModelRegistrationSerializer(get_table_name).data

            get_table_name = ModelRegistration.objects.get(model_name=model_name)
            serializers=ModelRegistrationSerializer(get_table_name).data

            print('table name of current',get_table_name)
            
            workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
            serializers_data=WorkflowMappingSerializer(workflow_mapping).data

            if user_ids_resp is not None and sent_auth.send_to_authorized == 'False' and sent_auth.same_user_authorized == 'False':

                obj = delete_record(request,APP_NAME, 'SystemUptime', systemuptime_id)
                return success("Successfully deleted")
            else:
                data={
                    'SystemUptime':serializer,
                    'table_data':serializers,
                    'workflow_data':serializers_data
                }
                return success(data)
        else:
            return error('you have no permission to delete the record')
    
    except SystemUptimeLive.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def view_systemuptime_tempdata(systemuptime_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = SystemUptimeTemp.objects.get(code=systemuptime_id)
        serializer = SystemUptimeTempSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")
    

def view_systemuptime_live(systemuptime_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = SystemUptimeLive.objects.get(code=systemuptime_id)
        serializer = SystemUptimeLiveViewSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def authorize_request_data_SystemUptime(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=SystemUptimeTemp.objects.get(pk=pk)
        work_flow_type=get_instance.record_type
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,work_flow_type)
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()

        return success(req)
    
    except SystemUptimeTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def authorize_request_data_delete_SystemUptime(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=SystemUptimeLive.objects.get(pk=pk)
  
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,type='delete')
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()
        return success(req)
    
    except SystemUptimeTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")





#add foreign key import model.


def create_itticketresolution(tickets_raised, tickets_resolved, average_resolution_time_hours, high_priority_tickets, unresolved_tickets, reported_date, escalation_rate, resolution_comments):
    """
    Creates a ITTicketResolution instance with the provided data.
        Args:
        tickets_raised, tickets_resolved, average_resolution_time_hours, high_priority_tickets, unresolved_tickets, reported_date, escalation_rate, resolution_comments: Keyword arguments for ITTicketResolution fields.

    Returns:
        dict: Success or error message.
        APP_NAME = __name__.split('.')[0]

    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        data={'tickets_raised': tickets_raised,
			'tickets_resolved': tickets_resolved,
			'average_resolution_time_hours': average_resolution_time_hours,
			'high_priority_tickets': high_priority_tickets,
			'unresolved_tickets': unresolved_tickets,
			'reported_date': reported_date,
			'escalation_rate': escalation_rate,
			'resolution_comments': resolution_comments,}
        data['code'] = generate_random_id('ABC')
        data_create = data.copy()
        data_create['code'] = generate_random_id('ABC')
        data_create['record_type']='create'
        # Initialize the serializer with the data
        serializer_temp = ITTicketResolutionTempSerializer(data=data_create)
        serializer_live=ITTicketResolutionLiveSerializer(data=data)
        
        # Validate and save the serializer data
        if serializer_live.is_valid() and serializer_temp.is_valid() :
            temp_instance = serializer_temp.save()
            type=temp_instance.record_type
            # Call auditing and authorization functions if needed
            is_audit = model_audit(request,APP_NAME,'ITTicketResolution',temp_instance.pk)
            is_authorization = self_authorization(request,APP_NAME,'ITTicketResolution', temp_instance.pk,type)
            
            model_name='ITTicketResolution'
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

def update_itticketresolution_temp(code,tickets_raised=None, tickets_resolved=None, average_resolution_time_hours=None, high_priority_tickets=None, unresolved_tickets=None, reported_date=None, escalation_rate=None, resolution_comments=None):
    """
    Updates a ITTicketResolution instance with the provided data.
    
    Args:
        itticketresolution_id (int): ID of the ITTicketResolution to update.
        tickets_raised=None, tickets_resolved=None, average_resolution_time_hours=None, high_priority_tickets=None, unresolved_tickets=None, reported_date=None, escalation_rate=None, resolution_comments=None: Keyword arguments for ITTicketResolution fields to update.

    Returns:
        dict: Success or error message.
    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if  is_have_permission(request,APP_NAME, 'ITTicketResolution',code):

            data={'tickets_raised': tickets_raised,
			'tickets_resolved': tickets_resolved,
			'average_resolution_time_hours': average_resolution_time_hours,
			'high_priority_tickets': high_priority_tickets,
			'unresolved_tickets': unresolved_tickets,
			'reported_date': reported_date,
			'escalation_rate': escalation_rate,
			'resolution_comments': resolution_comments,}
            data['code']=code

            data['record_type']='update'
            # Initialize the serializer with the data
            serializer_temp = ITTicketResolutionTempSerializer(data=data)
            #serializer_live=ITTicketResolutionLiveSerializer(data=data)
            
            # Validate and save the serializer data
            if serializer_temp.is_valid() :
                temp_instance = serializer_temp.save()
                type=temp_instance.record_type
                # Call auditing and authorization functions if needed
                is_audit = model_audit(request,APP_NAME,'ITTicketResolution',temp_instance.pk)
                is_authorization = self_authorization(request,APP_NAME,'ITTicketResolution', temp_instance.pk,type)

                model_name='ITTicketResolution'
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
    except  ITTicketResolutionTemp.DoesNotExist:
        return error('Instance does not exist')
    except ValidationError as e:
        return error(f"Validation Error: {e}")
    except Exception as e:
        return error(f"An error occurred: {e}")



def view_itticketresolution(itticketresolution_id=None):
    """
    Retrieves and serializes a ITTicketResolution instance by its ID or all instances if ID is None.
    
    Args:
        ITTicketResolution_id (int, optional): ID of the ITTicketResolution to retrieve.

    Returns:
        dict: A success response with the serialized data if found,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if itticketresolution_id is not None:
            record = ITTicketResolutionTemp.objects.get(pk=itticketresolution_id)
            serializer = ITTicketResolutionTempSerializer(record)
        else:
            obj = ITTicketResolutionLive.objects.filter(is_deactivate=False)
            obj_pa = get_temp_record(request,APP_NAME,'ITTicketResolution').filter(~Q(status='unauthorized_sent'))
            print('object--',obj_pa)
            obj_wait_auth = get_record_for_authorize(str(request.user.pk))
            # records = NoSeriesLinesALive.objects.all()
            live_data = ITTicketResolutionLiveSerializer(obj, many=True).data
            temp_data = ITTicketResolutionTempSerializer(obj_pa, many=True).data
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


def view_itticketresolution_single(code):
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
        

        record = ITTicketResolutionLive.objects.get(pk=code)
        serializer = ITTicketResolutionLiveSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")


def pa_itticketresolution(itticketresolution_id,model_name):
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
        
        record = ITTicketResolutionTemp.objects.get(pk=itticketresolution_id)
        serializer = ITTicketResolutionTempPASerializer(record).data
        
        type=record.record_type
        get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
        serializers=ModelRegistrationSerializer(get_table_name).data

        workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
        serializers_data=WorkflowMappingSerializer(workflow_mapping).data

        data={
            'itticketresolution':serializer,
            'table_data':serializers,
            'workflow_data':serializers_data
        }
        return success(data)
    
    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def delete_itticketresolution(itticketresolution_id,model_name):
    """
    Deletes a ITTicketResolution instance with the given ID.
    
    Args:
        itticketresolution_id (int): ID of the ITTicketResolution to delete.

    Returns:
        dict: A success response if deletion is successful,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        if  is_have_permission(request,APP_NAME, 'ITTicketResolution', itticketresolution_id):
            type='delete'

            is_authorization = self_authorization_for_delete(request,APP_NAME,model_name, itticketresolution_id,type)
            user_ids_resp=get_next_user_from_work_flow(request,model_name,temp_instance=itticketresolution_id,type=type)
 
            sent_auth=WorkflowMapping.objects.get(table_name__model_name__iexact=model_name,workflow_type=type)
            
            record = ITTicketResolutionLive.objects.get(pk=itticketresolution_id)
            serializer = ITTicketResolutionLiveViewSerializer(record).data

            # get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
            # serializers=ModelRegistrationSerializer(get_table_name).data

            get_table_name = ModelRegistration.objects.get(model_name=model_name)
            serializers=ModelRegistrationSerializer(get_table_name).data

            print('table name of current',get_table_name)
            
            workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
            serializers_data=WorkflowMappingSerializer(workflow_mapping).data

            if user_ids_resp is not None and sent_auth.send_to_authorized == 'False' and sent_auth.same_user_authorized == 'False':

                obj = delete_record(request,APP_NAME, 'ITTicketResolution', itticketresolution_id)
                return success("Successfully deleted")
            else:
                data={
                    'ITTicketResolution':serializer,
                    'table_data':serializers,
                    'workflow_data':serializers_data
                }
                return success(data)
        else:
            return error('you have no permission to delete the record')
    
    except ITTicketResolutionLive.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def view_itticketresolution_tempdata(itticketresolution_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = ITTicketResolutionTemp.objects.get(code=itticketresolution_id)
        serializer = ITTicketResolutionTempSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")
    

def view_itticketresolution_live(itticketresolution_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = ITTicketResolutionLive.objects.get(code=itticketresolution_id)
        serializer = ITTicketResolutionLiveViewSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def authorize_request_data_ITTicketResolution(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=ITTicketResolutionTemp.objects.get(pk=pk)
        work_flow_type=get_instance.record_type
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,work_flow_type)
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()

        return success(req)
    
    except ITTicketResolutionTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def authorize_request_data_delete_ITTicketResolution(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=ITTicketResolutionLive.objects.get(pk=pk)
  
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,type='delete')
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()
        return success(req)
    
    except ITTicketResolutionTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")





def accountsreceivableaging_report(from_date=None,to_date=None):

    try:
  
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if from_date:
            from_date = datetime.strptime(from_date, "%Y-%m-%d")
         
        if to_date:
            to_date = datetime.strptime(to_date, "%Y-%m-%d")
    
        if from_date and to_date:
            record_audit = AccountsReceivableAgingAudit.objects.filter(created_at__range=[from_date, to_date])
        elif from_date:
            record_audit = AccountsReceivableAgingAudit.objects.filter(created_at__gte=from_date)
        else:
            record_audit = AccountsReceivableAgingAudit.objects.filter(created_at__lte=to_date)
   
        record_live = AccountsReceivableAgingLive.objects.filter(
            code__in=record_audit.values_list('code', flat=True)
        )

        serializer = AccountsReceivableAgingLiveSerializer(record_live,many=True).data

        return success(serializer)
        

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")

def assetmanagement_report(from_date=None,to_date=None):

    try:
  
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if from_date:
            from_date = datetime.strptime(from_date, "%Y-%m-%d")
         
        if to_date:
            to_date = datetime.strptime(to_date, "%Y-%m-%d")
    
        if from_date and to_date:
            record_audit = AssetManagementAudit.objects.filter(created_at__range=[from_date, to_date])
        elif from_date:
            record_audit = AssetManagementAudit.objects.filter(created_at__gte=from_date)
        else:
            record_audit = AssetManagementAudit.objects.filter(created_at__lte=to_date)
   
        record_live = AssetManagementLive.objects.filter(
            code__in=record_audit.values_list('code', flat=True)
        )

        serializer = AssetManagementLiveSerializer(record_live,many=True).data

        return success(serializer)
        

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")

def balancesheet_report(from_date=None,to_date=None):

    try:
  
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if from_date:
            from_date = datetime.strptime(from_date, "%Y-%m-%d")
         
        if to_date:
            to_date = datetime.strptime(to_date, "%Y-%m-%d")
    
        if from_date and to_date:
            record_audit = BalanceSheetAudit.objects.filter(created_at__range=[from_date, to_date])
        elif from_date:
            record_audit = BalanceSheetAudit.objects.filter(created_at__gte=from_date)
        else:
            record_audit = BalanceSheetAudit.objects.filter(created_at__lte=to_date)
   
        record_live = BalanceSheetLive.objects.filter(
            code__in=record_audit.values_list('code', flat=True)
        )

        serializer = BalanceSheetLiveSerializer(record_live,many=True).data

        return success(serializer)
        

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")

def branchperformance_report(from_date=None,to_date=None):

    try:
  
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if from_date:
            from_date = datetime.strptime(from_date, "%Y-%m-%d")
         
        if to_date:
            to_date = datetime.strptime(to_date, "%Y-%m-%d")
    
        if from_date and to_date:
            record_audit = BranchPerformanceAudit.objects.filter(created_at__range=[from_date, to_date])
        elif from_date:
            record_audit = BranchPerformanceAudit.objects.filter(created_at__gte=from_date)
        else:
            record_audit = BranchPerformanceAudit.objects.filter(created_at__lte=to_date)
   
        record_live = BranchPerformanceLive.objects.filter(
            code__in=record_audit.values_list('code', flat=True)
        )

        serializer = BranchPerformanceLiveSerializer(record_live,many=True).data

        return success(serializer)
        

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")

def cashflowstatement_report(from_date=None,to_date=None):

    try:
  
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if from_date:
            from_date = datetime.strptime(from_date, "%Y-%m-%d")
         
        if to_date:
            to_date = datetime.strptime(to_date, "%Y-%m-%d")
    
        if from_date and to_date:
            record_audit = CashFlowStatementAudit.objects.filter(created_at__range=[from_date, to_date])
        elif from_date:
            record_audit = CashFlowStatementAudit.objects.filter(created_at__gte=from_date)
        else:
            record_audit = CashFlowStatementAudit.objects.filter(created_at__lte=to_date)
   
        record_live = CashFlowStatementLive.objects.filter(
            code__in=record_audit.values_list('code', flat=True)
        )

        serializer = CashFlowStatementLiveSerializer(record_live,many=True).data

        return success(serializer)
        

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")

def clientacquisition_report(from_date=None,to_date=None):

    try:
  
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if from_date:
            from_date = datetime.strptime(from_date, "%Y-%m-%d")
         
        if to_date:
            to_date = datetime.strptime(to_date, "%Y-%m-%d")
    
        if from_date and to_date:
            record_audit = ClientAcquisitionAudit.objects.filter(created_at__range=[from_date, to_date])
        elif from_date:
            record_audit = ClientAcquisitionAudit.objects.filter(created_at__gte=from_date)
        else:
            record_audit = ClientAcquisitionAudit.objects.filter(created_at__lte=to_date)
   
        record_live = ClientAcquisitionLive.objects.filter(
            code__in=record_audit.values_list('code', flat=True)
        )

        serializer = ClientAcquisitionLiveSerializer(record_live,many=True).data

        return success(serializer)
        

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")

def clientoutreach_report(from_date=None,to_date=None):

    try:
  
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if from_date:
            from_date = datetime.strptime(from_date, "%Y-%m-%d")
         
        if to_date:
            to_date = datetime.strptime(to_date, "%Y-%m-%d")
    
        if from_date and to_date:
            record_audit = ClientOutreachAudit.objects.filter(created_at__range=[from_date, to_date])
        elif from_date:
            record_audit = ClientOutreachAudit.objects.filter(created_at__gte=from_date)
        else:
            record_audit = ClientOutreachAudit.objects.filter(created_at__lte=to_date)
   
        record_live = ClientOutreachLive.objects.filter(
            code__in=record_audit.values_list('code', flat=True)
        )

        serializer = ClientOutreachLiveSerializer(record_live,many=True).data

        return success(serializer)
        

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")

def compliance_report(from_date=None,to_date=None):

    try:
  
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if from_date:
            from_date = datetime.strptime(from_date, "%Y-%m-%d")
         
        if to_date:
            to_date = datetime.strptime(to_date, "%Y-%m-%d")
    
        if from_date and to_date:
            record_audit = ComplianceAudit.objects.filter(created_at__range=[from_date, to_date])
        elif from_date:
            record_audit = ComplianceAudit.objects.filter(created_at__gte=from_date)
        else:
            record_audit = ComplianceAudit.objects.filter(created_at__lte=to_date)
   
        record_live = ComplianceLive.objects.filter(
            code__in=record_audit.values_list('code', flat=True)
        )

        serializer = ComplianceLiveSerializer(record_live,many=True).data

        return success(serializer)
        

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")

def customersatisfaction_report(from_date=None,to_date=None):

    try:
  
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if from_date:
            from_date = datetime.strptime(from_date, "%Y-%m-%d")
         
        if to_date:
            to_date = datetime.strptime(to_date, "%Y-%m-%d")
    
        if from_date and to_date:
            record_audit = CustomerSatisfactionAudit.objects.filter(created_at__range=[from_date, to_date])
        elif from_date:
            record_audit = CustomerSatisfactionAudit.objects.filter(created_at__gte=from_date)
        else:
            record_audit = CustomerSatisfactionAudit.objects.filter(created_at__lte=to_date)
   
        record_live = CustomerSatisfactionLive.objects.filter(
            code__in=record_audit.values_list('code', flat=True)
        )

        serializer = CustomerSatisfactionLiveSerializer(record_live,many=True).data

        return success(serializer)
        

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")

def dataaccuracy_report(from_date=None,to_date=None):

    try:
  
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if from_date:
            from_date = datetime.strptime(from_date, "%Y-%m-%d")
         
        if to_date:
            to_date = datetime.strptime(to_date, "%Y-%m-%d")
    
        if from_date and to_date:
            record_audit = DataAccuracyAudit.objects.filter(created_at__range=[from_date, to_date])
        elif from_date:
            record_audit = DataAccuracyAudit.objects.filter(created_at__gte=from_date)
        else:
            record_audit = DataAccuracyAudit.objects.filter(created_at__lte=to_date)
   
        record_live = DataAccuracyLive.objects.filter(
            code__in=record_audit.values_list('code', flat=True)
        )

        serializer = DataAccuracyLiveSerializer(record_live,many=True).data

        return success(serializer)
        

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")

def feedbackandcomplaints_report(from_date=None,to_date=None):

    try:
  
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if from_date:
            from_date = datetime.strptime(from_date, "%Y-%m-%d")
         
        if to_date:
            to_date = datetime.strptime(to_date, "%Y-%m-%d")
    
        if from_date and to_date:
            record_audit = FeedbackAndComplaintsAudit.objects.filter(created_at__range=[from_date, to_date])
        elif from_date:
            record_audit = FeedbackAndComplaintsAudit.objects.filter(created_at__gte=from_date)
        else:
            record_audit = FeedbackAndComplaintsAudit.objects.filter(created_at__lte=to_date)
   
        record_live = FeedbackAndComplaintsLive.objects.filter(
            code__in=record_audit.values_list('code', flat=True)
        )

        serializer = FeedbackAndComplaintsLiveSerializer(record_live,many=True).data

        return success(serializer)
        

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")

def fraudmonitoring_report(from_date=None,to_date=None):

    try:
  
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if from_date:
            from_date = datetime.strptime(from_date, "%Y-%m-%d")
         
        if to_date:
            to_date = datetime.strptime(to_date, "%Y-%m-%d")
    
        if from_date and to_date:
            record_audit = FraudMonitoringAudit.objects.filter(created_at__range=[from_date, to_date])
        elif from_date:
            record_audit = FraudMonitoringAudit.objects.filter(created_at__gte=from_date)
        else:
            record_audit = FraudMonitoringAudit.objects.filter(created_at__lte=to_date)
   
        record_live = FraudMonitoringLive.objects.filter(
            code__in=record_audit.values_list('code', flat=True)
        )

        serializer = FraudMonitoringLiveSerializer(record_live,many=True).data

        return success(serializer)
        

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")

def incomestatement_report(from_date=None,to_date=None):

    try:
  
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if from_date:
            from_date = datetime.strptime(from_date, "%Y-%m-%d")
         
        if to_date:
            to_date = datetime.strptime(to_date, "%Y-%m-%d")
    
        if from_date and to_date:
            record_audit = IncomeStatementAudit.objects.filter(created_at__range=[from_date, to_date])
        elif from_date:
            record_audit = IncomeStatementAudit.objects.filter(created_at__gte=from_date)
        else:
            record_audit = IncomeStatementAudit.objects.filter(created_at__lte=to_date)
   
        record_live = IncomeStatementLive.objects.filter(
            code__in=record_audit.values_list('code', flat=True)
        )

        serializer = IncomeStatementLiveSerializer(record_live,many=True).data

        return success(serializer)
        

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")

def itticketresolution_report(from_date=None,to_date=None):

    try:
  
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if from_date:
            from_date = datetime.strptime(from_date, "%Y-%m-%d")
         
        if to_date:
            to_date = datetime.strptime(to_date, "%Y-%m-%d")
    
        if from_date and to_date:
            record_audit = ITTicketResolutionAudit.objects.filter(created_at__range=[from_date, to_date])
        elif from_date:
            record_audit = ITTicketResolutionAudit.objects.filter(created_at__gte=from_date)
        else:
            record_audit = ITTicketResolutionAudit.objects.filter(created_at__lte=to_date)
   
        record_live = ITTicketResolutionLive.objects.filter(
            code__in=record_audit.values_list('code', flat=True)
        )

        serializer = ITTicketResolutionLiveSerializer(record_live,many=True).data

        return success(serializer)
        

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")

def leavemanagement_report(from_date=None,to_date=None):

    try:
  
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if from_date:
            from_date = datetime.strptime(from_date, "%Y-%m-%d")
         
        if to_date:
            to_date = datetime.strptime(to_date, "%Y-%m-%d")
    
        if from_date and to_date:
            record_audit = LeaveManagementAudit.objects.filter(created_at__range=[from_date, to_date])
        elif from_date:
            record_audit = LeaveManagementAudit.objects.filter(created_at__gte=from_date)
        else:
            record_audit = LeaveManagementAudit.objects.filter(created_at__lte=to_date)
   
        record_live = LeaveManagementLive.objects.filter(
            code__in=record_audit.values_list('code', flat=True)
        )

        serializer = LeaveManagementLiveSerializer(record_live,many=True).data

        return success(serializer)
        

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")

def loanaging_report(from_date=None,to_date=None):

    try:
  
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if from_date:
            from_date = datetime.strptime(from_date, "%Y-%m-%d")
         
        if to_date:
            to_date = datetime.strptime(to_date, "%Y-%m-%d")
    
        if from_date and to_date:
            record_audit = LoanAgingAudit.objects.filter(created_at__range=[from_date, to_date])
        elif from_date:
            record_audit = LoanAgingAudit.objects.filter(created_at__gte=from_date)
        else:
            record_audit = LoanAgingAudit.objects.filter(created_at__lte=to_date)
   
        record_live = LoanAgingLive.objects.filter(
            code__in=record_audit.values_list('code', flat=True)
        )

        serializer = LoanAgingLiveSerializer(record_live,many=True).data

        return success(serializer)
        

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")

def loandisbursement_report(from_date=None,to_date=None):

    try:
  
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if from_date:
            from_date = datetime.strptime(from_date, "%Y-%m-%d")
         
        if to_date:
            to_date = datetime.strptime(to_date, "%Y-%m-%d")
    
        if from_date and to_date:
            record_audit = LoanDisbursementAudit.objects.filter(created_at__range=[from_date, to_date])
        elif from_date:
            record_audit = LoanDisbursementAudit.objects.filter(created_at__gte=from_date)
        else:
            record_audit = LoanDisbursementAudit.objects.filter(created_at__lte=to_date)
   
        record_live = LoanDisbursementLive.objects.filter(
            code__in=record_audit.values_list('code', flat=True)
        )

        serializer = LoanDisbursementLiveSerializer(record_live,many=True).data

        return success(serializer)
        

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")

def loanlossprovision_report(from_date=None,to_date=None):

    try:
  
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if from_date:
            from_date = datetime.strptime(from_date, "%Y-%m-%d")
         
        if to_date:
            to_date = datetime.strptime(to_date, "%Y-%m-%d")
    
        if from_date and to_date:
            record_audit = LoanLossProvisionAudit.objects.filter(created_at__range=[from_date, to_date])
        elif from_date:
            record_audit = LoanLossProvisionAudit.objects.filter(created_at__gte=from_date)
        else:
            record_audit = LoanLossProvisionAudit.objects.filter(created_at__lte=to_date)
   
        record_live = LoanLossProvisionLive.objects.filter(
            code__in=record_audit.values_list('code', flat=True)
        )

        serializer = LoanLossProvisionLiveSerializer(record_live,many=True).data

        return success(serializer)
        

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")

def logisticsandfleetmanagement_report(from_date=None,to_date=None):

    try:
  
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if from_date:
            from_date = datetime.strptime(from_date, "%Y-%m-%d")
         
        if to_date:
            to_date = datetime.strptime(to_date, "%Y-%m-%d")
    
        if from_date and to_date:
            record_audit = LogisticsAndFleetManagementAudit.objects.filter(created_at__range=[from_date, to_date])
        elif from_date:
            record_audit = LogisticsAndFleetManagementAudit.objects.filter(created_at__gte=from_date)
        else:
            record_audit = LogisticsAndFleetManagementAudit.objects.filter(created_at__lte=to_date)
   
        record_live = LogisticsAndFleetManagementLive.objects.filter(
            code__in=record_audit.values_list('code', flat=True)
        )

        serializer = LogisticsAndFleetManagementLiveSerializer(record_live,many=True).data

        return success(serializer)
        

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")

def officeexpense_report(from_date=None,to_date=None):

    try:
  
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if from_date:
            from_date = datetime.strptime(from_date, "%Y-%m-%d")
         
        if to_date:
            to_date = datetime.strptime(to_date, "%Y-%m-%d")
    
        if from_date and to_date:
            record_audit = OfficeExpenseAudit.objects.filter(created_at__range=[from_date, to_date])
        elif from_date:
            record_audit = OfficeExpenseAudit.objects.filter(created_at__gte=from_date)
        else:
            record_audit = OfficeExpenseAudit.objects.filter(created_at__lte=to_date)
   
        record_live = OfficeExpenseLive.objects.filter(
            code__in=record_audit.values_list('code', flat=True)
        )

        serializer = OfficeExpenseLiveSerializer(record_live,many=True).data

        return success(serializer)
        

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")

def portfolioquality_report(from_date=None,to_date=None):

    try:
  
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if from_date:
            from_date = datetime.strptime(from_date, "%Y-%m-%d")
         
        if to_date:
            to_date = datetime.strptime(to_date, "%Y-%m-%d")
    
        if from_date and to_date:
            record_audit = PortfolioQualityAudit.objects.filter(created_at__range=[from_date, to_date])
        elif from_date:
            record_audit = PortfolioQualityAudit.objects.filter(created_at__gte=from_date)
        else:
            record_audit = PortfolioQualityAudit.objects.filter(created_at__lte=to_date)
   
        record_live = PortfolioQualityLive.objects.filter(
            code__in=record_audit.values_list('code', flat=True)
        )

        serializer = PortfolioQualityLiveSerializer(record_live,many=True).data

        return success(serializer)
        

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")

def riskassessment_report(from_date=None,to_date=None):

    try:
  
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if from_date:
            from_date = datetime.strptime(from_date, "%Y-%m-%d")
         
        if to_date:
            to_date = datetime.strptime(to_date, "%Y-%m-%d")
    
        if from_date and to_date:
            record_audit = RiskAssessmentAudit.objects.filter(created_at__range=[from_date, to_date])
        elif from_date:
            record_audit = RiskAssessmentAudit.objects.filter(created_at__gte=from_date)
        else:
            record_audit = RiskAssessmentAudit.objects.filter(created_at__lte=to_date)
   
        record_live = RiskAssessmentLive.objects.filter(
            code__in=record_audit.values_list('code', flat=True)
        )

        serializer = RiskAssessmentLiveSerializer(record_live,many=True).data

        return success(serializer)
        

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")

def staffproductivity_report(from_date=None,to_date=None):

    try:
  
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if from_date:
            from_date = datetime.strptime(from_date, "%Y-%m-%d")
         
        if to_date:
            to_date = datetime.strptime(to_date, "%Y-%m-%d")
    
        if from_date and to_date:
            record_audit = StaffProductivityAudit.objects.filter(created_at__range=[from_date, to_date])
        elif from_date:
            record_audit = StaffProductivityAudit.objects.filter(created_at__gte=from_date)
        else:
            record_audit = StaffProductivityAudit.objects.filter(created_at__lte=to_date)
   
        record_live = StaffProductivityLive.objects.filter(
            code__in=record_audit.values_list('code', flat=True)
        )

        serializer = StaffProductivityLiveSerializer(record_live,many=True).data

        return success(serializer)
        

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")

def staffturnover_report(from_date=None,to_date=None):

    try:
  
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if from_date:
            from_date = datetime.strptime(from_date, "%Y-%m-%d")
         
        if to_date:
            to_date = datetime.strptime(to_date, "%Y-%m-%d")
    
        if from_date and to_date:
            record_audit = StaffTurnoverAudit.objects.filter(created_at__range=[from_date, to_date])
        elif from_date:
            record_audit = StaffTurnoverAudit.objects.filter(created_at__gte=from_date)
        else:
            record_audit = StaffTurnoverAudit.objects.filter(created_at__lte=to_date)
   
        record_live = StaffTurnoverLive.objects.filter(
            code__in=record_audit.values_list('code', flat=True)
        )

        serializer = StaffTurnoverLiveSerializer(record_live,many=True).data

        return success(serializer)
        

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")

def systemuptime_report(from_date=None,to_date=None):

    try:
  
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if from_date:
            from_date = datetime.strptime(from_date, "%Y-%m-%d")
         
        if to_date:
            to_date = datetime.strptime(to_date, "%Y-%m-%d")
    
        if from_date and to_date:
            record_audit = SystemUptimeAudit.objects.filter(created_at__range=[from_date, to_date])
        elif from_date:
            record_audit = SystemUptimeAudit.objects.filter(created_at__gte=from_date)
        else:
            record_audit = SystemUptimeAudit.objects.filter(created_at__lte=to_date)
   
        record_live = SystemUptimeLive.objects.filter(
            code__in=record_audit.values_list('code', flat=True)
        )

        serializer = SystemUptimeLiveSerializer(record_live,many=True).data

        return success(serializer)
        

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")

def trainingdevelopment_report(from_date=None,to_date=None):

    try:
  
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if from_date:
            from_date = datetime.strptime(from_date, "%Y-%m-%d")
         
        if to_date:
            to_date = datetime.strptime(to_date, "%Y-%m-%d")
    
        if from_date and to_date:
            record_audit = TrainingDevelopmentAudit.objects.filter(created_at__range=[from_date, to_date])
        elif from_date:
            record_audit = TrainingDevelopmentAudit.objects.filter(created_at__gte=from_date)
        else:
            record_audit = TrainingDevelopmentAudit.objects.filter(created_at__lte=to_date)
   
        record_live = TrainingDevelopmentLive.objects.filter(
            code__in=record_audit.values_list('code', flat=True)
        )

        serializer = TrainingDevelopmentLiveSerializer(record_live,many=True).data

        return success(serializer)
        

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")

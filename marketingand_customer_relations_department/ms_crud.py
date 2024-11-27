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


def create_customersatisfaction(surveys_conducted, satisfaction_score, top_complaints, net_promoter_score, repeat_customer_percentage, reported_date, survey_response_rate, comments):
    """
    Creates a CustomerSatisfaction instance with the provided data.
        Args:
        surveys_conducted, satisfaction_score, top_complaints, net_promoter_score, repeat_customer_percentage, reported_date, survey_response_rate, comments: Keyword arguments for CustomerSatisfaction fields.

    Returns:
        dict: Success or error message.
        APP_NAME = __name__.split('.')[0]

    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        data={'surveys_conducted': surveys_conducted,
			'satisfaction_score': satisfaction_score,
			'top_complaints': top_complaints,
			'net_promoter_score': net_promoter_score,
			'repeat_customer_percentage': repeat_customer_percentage,
			'reported_date': reported_date,
			'survey_response_rate': survey_response_rate,
			'comments': comments,}
        data['code'] = generate_random_id('ABC')
        data_create = data.copy()
        data_create['code'] = generate_random_id('ABC')
        data_create['record_type']='create'
        # Initialize the serializer with the data
        serializer_temp = CustomerSatisfactionTempSerializer(data=data_create)
        serializer_live=CustomerSatisfactionLiveSerializer(data=data)
        
        # Validate and save the serializer data
        if serializer_live.is_valid() and serializer_temp.is_valid() :
            temp_instance = serializer_temp.save()
            type=temp_instance.record_type
            # Call auditing and authorization functions if needed
            is_audit = model_audit(request,APP_NAME,'CustomerSatisfaction',temp_instance.pk)
            is_authorization = self_authorization(request,APP_NAME,'CustomerSatisfaction', temp_instance.pk,type)
            
            model_name='CustomerSatisfaction'
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

def update_customersatisfaction_temp(code,surveys_conducted=None, satisfaction_score=None, top_complaints=None, net_promoter_score=None, repeat_customer_percentage=None, reported_date=None, survey_response_rate=None, comments=None):
    """
    Updates a CustomerSatisfaction instance with the provided data.
    
    Args:
        customersatisfaction_id (int): ID of the CustomerSatisfaction to update.
        surveys_conducted=None, satisfaction_score=None, top_complaints=None, net_promoter_score=None, repeat_customer_percentage=None, reported_date=None, survey_response_rate=None, comments=None: Keyword arguments for CustomerSatisfaction fields to update.

    Returns:
        dict: Success or error message.
    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if  is_have_permission(request,APP_NAME, 'CustomerSatisfaction',code):

            data={'surveys_conducted': surveys_conducted,
			'satisfaction_score': satisfaction_score,
			'top_complaints': top_complaints,
			'net_promoter_score': net_promoter_score,
			'repeat_customer_percentage': repeat_customer_percentage,
			'reported_date': reported_date,
			'survey_response_rate': survey_response_rate,
			'comments': comments,}
            data['code']=code

            data['record_type']='update'
            # Initialize the serializer with the data
            serializer_temp = CustomerSatisfactionTempSerializer(data=data)
            #serializer_live=CustomerSatisfactionLiveSerializer(data=data)
            
            # Validate and save the serializer data
            if serializer_temp.is_valid() :
                temp_instance = serializer_temp.save()
                type=temp_instance.record_type
                # Call auditing and authorization functions if needed
                is_audit = model_audit(request,APP_NAME,'CustomerSatisfaction',temp_instance.pk)
                is_authorization = self_authorization(request,APP_NAME,'CustomerSatisfaction', temp_instance.pk,type)

                model_name='CustomerSatisfaction'
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
    except  CustomerSatisfactionTemp.DoesNotExist:
        return error('Instance does not exist')
    except ValidationError as e:
        return error(f"Validation Error: {e}")
    except Exception as e:
        return error(f"An error occurred: {e}")



def view_customersatisfaction(customersatisfaction_id=None):
    """
    Retrieves and serializes a CustomerSatisfaction instance by its ID or all instances if ID is None.
    
    Args:
        CustomerSatisfaction_id (int, optional): ID of the CustomerSatisfaction to retrieve.

    Returns:
        dict: A success response with the serialized data if found,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if customersatisfaction_id is not None:
            record = CustomerSatisfactionTemp.objects.get(pk=customersatisfaction_id)
            serializer = CustomerSatisfactionTempSerializer(record)
        else:
            obj = CustomerSatisfactionLive.objects.filter(is_deactivate=False)
            obj_pa = get_temp_record(request,APP_NAME,'CustomerSatisfaction').filter(~Q(status='unauthorized_sent'))
            print('object--',obj_pa)
            obj_wait_auth = get_record_for_authorize(str(request.user.pk))
            # records = NoSeriesLinesALive.objects.all()
            live_data = CustomerSatisfactionLiveSerializer(obj, many=True).data
            temp_data = CustomerSatisfactionTempSerializer(obj_pa, many=True).data
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


def view_customersatisfaction_single(code):
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
        

        record = CustomerSatisfactionLive.objects.get(pk=code)
        serializer = CustomerSatisfactionLiveSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")


def pa_customersatisfaction(customersatisfaction_id,model_name):
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
        
        record = CustomerSatisfactionTemp.objects.get(pk=customersatisfaction_id)
        serializer = CustomerSatisfactionTempPASerializer(record).data
        
        type=record.record_type
        get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
        serializers=ModelRegistrationSerializer(get_table_name).data

        workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
        serializers_data=WorkflowMappingSerializer(workflow_mapping).data

        data={
            'customersatisfaction':serializer,
            'table_data':serializers,
            'workflow_data':serializers_data
        }
        return success(data)
    
    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def delete_customersatisfaction(customersatisfaction_id,model_name):
    """
    Deletes a CustomerSatisfaction instance with the given ID.
    
    Args:
        customersatisfaction_id (int): ID of the CustomerSatisfaction to delete.

    Returns:
        dict: A success response if deletion is successful,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        if  is_have_permission(request,APP_NAME, 'CustomerSatisfaction', customersatisfaction_id):
            type='delete'

            is_authorization = self_authorization_for_delete(request,APP_NAME,model_name, customersatisfaction_id,type)
            user_ids_resp=get_next_user_from_work_flow(request,model_name,temp_instance=customersatisfaction_id,type=type)
 
            sent_auth=WorkflowMapping.objects.get(table_name__model_name__iexact=model_name,workflow_type=type)
            
            record = CustomerSatisfactionLive.objects.get(pk=customersatisfaction_id)
            serializer = CustomerSatisfactionLiveViewSerializer(record).data

            # get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
            # serializers=ModelRegistrationSerializer(get_table_name).data

            get_table_name = ModelRegistration.objects.get(model_name=model_name)
            serializers=ModelRegistrationSerializer(get_table_name).data

            print('table name of current',get_table_name)
            
            workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
            serializers_data=WorkflowMappingSerializer(workflow_mapping).data

            if user_ids_resp is not None and sent_auth.send_to_authorized == 'False' and sent_auth.same_user_authorized == 'False':

                obj = delete_record(request,APP_NAME, 'CustomerSatisfaction', customersatisfaction_id)
                return success("Successfully deleted")
            else:
                data={
                    'CustomerSatisfaction':serializer,
                    'table_data':serializers,
                    'workflow_data':serializers_data
                }
                return success(data)
        else:
            return error('you have no permission to delete the record')
    
    except CustomerSatisfactionLive.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def view_customersatisfaction_tempdata(customersatisfaction_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = CustomerSatisfactionTemp.objects.get(code=customersatisfaction_id)
        serializer = CustomerSatisfactionTempSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")
    

def view_customersatisfaction_live(customersatisfaction_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = CustomerSatisfactionLive.objects.get(code=customersatisfaction_id)
        serializer = CustomerSatisfactionLiveViewSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def authorize_request_data_CustomerSatisfaction(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=CustomerSatisfactionTemp.objects.get(pk=pk)
        work_flow_type=get_instance.record_type
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,work_flow_type)
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()

        return success(req)
    
    except CustomerSatisfactionTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def authorize_request_data_delete_CustomerSatisfaction(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=CustomerSatisfactionLive.objects.get(pk=pk)
  
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,type='delete')
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()
        return success(req)
    
    except CustomerSatisfactionTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")





#add foreign key import model.


def create_clientacquisition(new_clients, acquisition_cost_per_client, total_acquisition_cost, average_conversion_rate, reported_date, referral_percentage, comments):
    """
    Creates a ClientAcquisition instance with the provided data.
        Args:
        new_clients, acquisition_cost_per_client, total_acquisition_cost, average_conversion_rate, reported_date, referral_percentage, comments: Keyword arguments for ClientAcquisition fields.

    Returns:
        dict: Success or error message.
        APP_NAME = __name__.split('.')[0]

    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        data={'new_clients': new_clients,
			'acquisition_cost_per_client': acquisition_cost_per_client,
			'total_acquisition_cost': total_acquisition_cost,
			'average_conversion_rate': average_conversion_rate,
			'reported_date': reported_date,
			'referral_percentage': referral_percentage,
			'comments': comments,}
        data['code'] = generate_random_id('ABC')
        data_create = data.copy()
        data_create['code'] = generate_random_id('ABC')
        data_create['record_type']='create'
        # Initialize the serializer with the data
        serializer_temp = ClientAcquisitionTempSerializer(data=data_create)
        serializer_live=ClientAcquisitionLiveSerializer(data=data)
        
        # Validate and save the serializer data
        if serializer_live.is_valid() and serializer_temp.is_valid() :
            temp_instance = serializer_temp.save()
            type=temp_instance.record_type
            # Call auditing and authorization functions if needed
            is_audit = model_audit(request,APP_NAME,'ClientAcquisition',temp_instance.pk)
            is_authorization = self_authorization(request,APP_NAME,'ClientAcquisition', temp_instance.pk,type)
            
            model_name='ClientAcquisition'
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

def update_clientacquisition_temp(code,new_clients=None, acquisition_cost_per_client=None, total_acquisition_cost=None, average_conversion_rate=None, reported_date=None, referral_percentage=None, comments=None):
    """
    Updates a ClientAcquisition instance with the provided data.
    
    Args:
        clientacquisition_id (int): ID of the ClientAcquisition to update.
        new_clients=None, acquisition_cost_per_client=None, total_acquisition_cost=None, average_conversion_rate=None, reported_date=None, referral_percentage=None, comments=None: Keyword arguments for ClientAcquisition fields to update.

    Returns:
        dict: Success or error message.
    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if  is_have_permission(request,APP_NAME, 'ClientAcquisition',code):

            data={'new_clients': new_clients,
			'acquisition_cost_per_client': acquisition_cost_per_client,
			'total_acquisition_cost': total_acquisition_cost,
			'average_conversion_rate': average_conversion_rate,
			'reported_date': reported_date,
			'referral_percentage': referral_percentage,
			'comments': comments,}
            data['code']=code

            data['record_type']='update'
            # Initialize the serializer with the data
            serializer_temp = ClientAcquisitionTempSerializer(data=data)
            #serializer_live=ClientAcquisitionLiveSerializer(data=data)
            
            # Validate and save the serializer data
            if serializer_temp.is_valid() :
                temp_instance = serializer_temp.save()
                type=temp_instance.record_type
                # Call auditing and authorization functions if needed
                is_audit = model_audit(request,APP_NAME,'ClientAcquisition',temp_instance.pk)
                is_authorization = self_authorization(request,APP_NAME,'ClientAcquisition', temp_instance.pk,type)

                model_name='ClientAcquisition'
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
    except  ClientAcquisitionTemp.DoesNotExist:
        return error('Instance does not exist')
    except ValidationError as e:
        return error(f"Validation Error: {e}")
    except Exception as e:
        return error(f"An error occurred: {e}")



def view_clientacquisition(clientacquisition_id=None):
    """
    Retrieves and serializes a ClientAcquisition instance by its ID or all instances if ID is None.
    
    Args:
        ClientAcquisition_id (int, optional): ID of the ClientAcquisition to retrieve.

    Returns:
        dict: A success response with the serialized data if found,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if clientacquisition_id is not None:
            record = ClientAcquisitionTemp.objects.get(pk=clientacquisition_id)
            serializer = ClientAcquisitionTempSerializer(record)
        else:
            obj = ClientAcquisitionLive.objects.filter(is_deactivate=False)
            obj_pa = get_temp_record(request,APP_NAME,'ClientAcquisition').filter(~Q(status='unauthorized_sent'))
            print('object--',obj_pa)
            obj_wait_auth = get_record_for_authorize(str(request.user.pk))
            # records = NoSeriesLinesALive.objects.all()
            live_data = ClientAcquisitionLiveSerializer(obj, many=True).data
            temp_data = ClientAcquisitionTempSerializer(obj_pa, many=True).data
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


def view_clientacquisition_single(code):
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
        

        record = ClientAcquisitionLive.objects.get(pk=code)
        serializer = ClientAcquisitionLiveSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")


def pa_clientacquisition(clientacquisition_id,model_name):
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
        
        record = ClientAcquisitionTemp.objects.get(pk=clientacquisition_id)
        serializer = ClientAcquisitionTempPASerializer(record).data
        
        type=record.record_type
        get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
        serializers=ModelRegistrationSerializer(get_table_name).data

        workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
        serializers_data=WorkflowMappingSerializer(workflow_mapping).data

        data={
            'clientacquisition':serializer,
            'table_data':serializers,
            'workflow_data':serializers_data
        }
        return success(data)
    
    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def delete_clientacquisition(clientacquisition_id,model_name):
    """
    Deletes a ClientAcquisition instance with the given ID.
    
    Args:
        clientacquisition_id (int): ID of the ClientAcquisition to delete.

    Returns:
        dict: A success response if deletion is successful,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        if  is_have_permission(request,APP_NAME, 'ClientAcquisition', clientacquisition_id):
            type='delete'

            is_authorization = self_authorization_for_delete(request,APP_NAME,model_name, clientacquisition_id,type)
            user_ids_resp=get_next_user_from_work_flow(request,model_name,temp_instance=clientacquisition_id,type=type)
 
            sent_auth=WorkflowMapping.objects.get(table_name__model_name__iexact=model_name,workflow_type=type)
            
            record = ClientAcquisitionLive.objects.get(pk=clientacquisition_id)
            serializer = ClientAcquisitionLiveViewSerializer(record).data

            # get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
            # serializers=ModelRegistrationSerializer(get_table_name).data

            get_table_name = ModelRegistration.objects.get(model_name=model_name)
            serializers=ModelRegistrationSerializer(get_table_name).data

            print('table name of current',get_table_name)
            
            workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
            serializers_data=WorkflowMappingSerializer(workflow_mapping).data

            if user_ids_resp is not None and sent_auth.send_to_authorized == 'False' and sent_auth.same_user_authorized == 'False':

                obj = delete_record(request,APP_NAME, 'ClientAcquisition', clientacquisition_id)
                return success("Successfully deleted")
            else:
                data={
                    'ClientAcquisition':serializer,
                    'table_data':serializers,
                    'workflow_data':serializers_data
                }
                return success(data)
        else:
            return error('you have no permission to delete the record')
    
    except ClientAcquisitionLive.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def view_clientacquisition_tempdata(clientacquisition_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = ClientAcquisitionTemp.objects.get(code=clientacquisition_id)
        serializer = ClientAcquisitionTempSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")
    

def view_clientacquisition_live(clientacquisition_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = ClientAcquisitionLive.objects.get(code=clientacquisition_id)
        serializer = ClientAcquisitionLiveViewSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def authorize_request_data_ClientAcquisition(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=ClientAcquisitionTemp.objects.get(pk=pk)
        work_flow_type=get_instance.record_type
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,work_flow_type)
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()

        return success(req)
    
    except ClientAcquisitionTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def authorize_request_data_delete_ClientAcquisition(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=ClientAcquisitionLive.objects.get(pk=pk)
  
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,type='delete')
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()
        return success(req)
    
    except ClientAcquisitionTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")





#add foreign key import model.


def create_feedbackandcomplaints(total_complaints_logged, resolved_complaints, resolution_rate, feedback_received, positive_feedback_percentage, reported_date, average_resolution_time_hours, unresolved_complaints, escalation_rate, comments):
    """
    Creates a FeedbackAndComplaints instance with the provided data.
        Args:
        total_complaints_logged, resolved_complaints, resolution_rate, feedback_received, positive_feedback_percentage, reported_date, average_resolution_time_hours, unresolved_complaints, escalation_rate, comments: Keyword arguments for FeedbackAndComplaints fields.

    Returns:
        dict: Success or error message.
        APP_NAME = __name__.split('.')[0]

    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        data={'total_complaints_logged': total_complaints_logged,
			'resolved_complaints': resolved_complaints,
			'resolution_rate': resolution_rate,
			'feedback_received': feedback_received,
			'positive_feedback_percentage': positive_feedback_percentage,
			'reported_date': reported_date,
			'average_resolution_time_hours': average_resolution_time_hours,
			'unresolved_complaints': unresolved_complaints,
			'escalation_rate': escalation_rate,
			'comments': comments,}
        data['code'] = generate_random_id('ABC')
        data_create = data.copy()
        data_create['code'] = generate_random_id('ABC')
        data_create['record_type']='create'
        # Initialize the serializer with the data
        serializer_temp = FeedbackAndComplaintsTempSerializer(data=data_create)
        serializer_live=FeedbackAndComplaintsLiveSerializer(data=data)
        
        # Validate and save the serializer data
        if serializer_live.is_valid() and serializer_temp.is_valid() :
            temp_instance = serializer_temp.save()
            type=temp_instance.record_type
            # Call auditing and authorization functions if needed
            is_audit = model_audit(request,APP_NAME,'FeedbackAndComplaints',temp_instance.pk)
            is_authorization = self_authorization(request,APP_NAME,'FeedbackAndComplaints', temp_instance.pk,type)
            
            model_name='FeedbackAndComplaints'
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

def update_feedbackandcomplaints_temp(code,total_complaints_logged=None, resolved_complaints=None, resolution_rate=None, feedback_received=None, positive_feedback_percentage=None, reported_date=None, average_resolution_time_hours=None, unresolved_complaints=None, escalation_rate=None, comments=None):
    """
    Updates a FeedbackAndComplaints instance with the provided data.
    
    Args:
        feedbackandcomplaints_id (int): ID of the FeedbackAndComplaints to update.
        total_complaints_logged=None, resolved_complaints=None, resolution_rate=None, feedback_received=None, positive_feedback_percentage=None, reported_date=None, average_resolution_time_hours=None, unresolved_complaints=None, escalation_rate=None, comments=None: Keyword arguments for FeedbackAndComplaints fields to update.

    Returns:
        dict: Success or error message.
    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if  is_have_permission(request,APP_NAME, 'FeedbackAndComplaints',code):

            data={'total_complaints_logged': total_complaints_logged,
			'resolved_complaints': resolved_complaints,
			'resolution_rate': resolution_rate,
			'feedback_received': feedback_received,
			'positive_feedback_percentage': positive_feedback_percentage,
			'reported_date': reported_date,
			'average_resolution_time_hours': average_resolution_time_hours,
			'unresolved_complaints': unresolved_complaints,
			'escalation_rate': escalation_rate,
			'comments': comments,}
            data['code']=code

            data['record_type']='update'
            # Initialize the serializer with the data
            serializer_temp = FeedbackAndComplaintsTempSerializer(data=data)
            #serializer_live=FeedbackAndComplaintsLiveSerializer(data=data)
            
            # Validate and save the serializer data
            if serializer_temp.is_valid() :
                temp_instance = serializer_temp.save()
                type=temp_instance.record_type
                # Call auditing and authorization functions if needed
                is_audit = model_audit(request,APP_NAME,'FeedbackAndComplaints',temp_instance.pk)
                is_authorization = self_authorization(request,APP_NAME,'FeedbackAndComplaints', temp_instance.pk,type)

                model_name='FeedbackAndComplaints'
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
    except  FeedbackAndComplaintsTemp.DoesNotExist:
        return error('Instance does not exist')
    except ValidationError as e:
        return error(f"Validation Error: {e}")
    except Exception as e:
        return error(f"An error occurred: {e}")



def view_feedbackandcomplaints(feedbackandcomplaints_id=None):
    """
    Retrieves and serializes a FeedbackAndComplaints instance by its ID or all instances if ID is None.
    
    Args:
        FeedbackAndComplaints_id (int, optional): ID of the FeedbackAndComplaints to retrieve.

    Returns:
        dict: A success response with the serialized data if found,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if feedbackandcomplaints_id is not None:
            record = FeedbackAndComplaintsTemp.objects.get(pk=feedbackandcomplaints_id)
            serializer = FeedbackAndComplaintsTempSerializer(record)
        else:
            obj = FeedbackAndComplaintsLive.objects.filter(is_deactivate=False)
            obj_pa = get_temp_record(request,APP_NAME,'FeedbackAndComplaints').filter(~Q(status='unauthorized_sent'))
            print('object--',obj_pa)
            obj_wait_auth = get_record_for_authorize(str(request.user.pk))
            # records = NoSeriesLinesALive.objects.all()
            live_data = FeedbackAndComplaintsLiveSerializer(obj, many=True).data
            temp_data = FeedbackAndComplaintsTempSerializer(obj_pa, many=True).data
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


def view_feedbackandcomplaints_single(code):
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
        

        record = FeedbackAndComplaintsLive.objects.get(pk=code)
        serializer = FeedbackAndComplaintsLiveSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")


def pa_feedbackandcomplaints(feedbackandcomplaints_id,model_name):
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
        
        record = FeedbackAndComplaintsTemp.objects.get(pk=feedbackandcomplaints_id)
        serializer = FeedbackAndComplaintsTempPASerializer(record).data
        
        type=record.record_type
        get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
        serializers=ModelRegistrationSerializer(get_table_name).data

        workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
        serializers_data=WorkflowMappingSerializer(workflow_mapping).data

        data={
            'feedbackandcomplaints':serializer,
            'table_data':serializers,
            'workflow_data':serializers_data
        }
        return success(data)
    
    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def delete_feedbackandcomplaints(feedbackandcomplaints_id,model_name):
    """
    Deletes a FeedbackAndComplaints instance with the given ID.
    
    Args:
        feedbackandcomplaints_id (int): ID of the FeedbackAndComplaints to delete.

    Returns:
        dict: A success response if deletion is successful,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        if  is_have_permission(request,APP_NAME, 'FeedbackAndComplaints', feedbackandcomplaints_id):
            type='delete'

            is_authorization = self_authorization_for_delete(request,APP_NAME,model_name, feedbackandcomplaints_id,type)
            user_ids_resp=get_next_user_from_work_flow(request,model_name,temp_instance=feedbackandcomplaints_id,type=type)
 
            sent_auth=WorkflowMapping.objects.get(table_name__model_name__iexact=model_name,workflow_type=type)
            
            record = FeedbackAndComplaintsLive.objects.get(pk=feedbackandcomplaints_id)
            serializer = FeedbackAndComplaintsLiveViewSerializer(record).data

            # get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
            # serializers=ModelRegistrationSerializer(get_table_name).data

            get_table_name = ModelRegistration.objects.get(model_name=model_name)
            serializers=ModelRegistrationSerializer(get_table_name).data

            print('table name of current',get_table_name)
            
            workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
            serializers_data=WorkflowMappingSerializer(workflow_mapping).data

            if user_ids_resp is not None and sent_auth.send_to_authorized == 'False' and sent_auth.same_user_authorized == 'False':

                obj = delete_record(request,APP_NAME, 'FeedbackAndComplaints', feedbackandcomplaints_id)
                return success("Successfully deleted")
            else:
                data={
                    'FeedbackAndComplaints':serializer,
                    'table_data':serializers,
                    'workflow_data':serializers_data
                }
                return success(data)
        else:
            return error('you have no permission to delete the record')
    
    except FeedbackAndComplaintsLive.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def view_feedbackandcomplaints_tempdata(feedbackandcomplaints_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = FeedbackAndComplaintsTemp.objects.get(code=feedbackandcomplaints_id)
        serializer = FeedbackAndComplaintsTempSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")
    

def view_feedbackandcomplaints_live(feedbackandcomplaints_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = FeedbackAndComplaintsLive.objects.get(code=feedbackandcomplaints_id)
        serializer = FeedbackAndComplaintsLiveViewSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def authorize_request_data_FeedbackAndComplaints(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=FeedbackAndComplaintsTemp.objects.get(pk=pk)
        work_flow_type=get_instance.record_type
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,work_flow_type)
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()

        return success(req)
    
    except FeedbackAndComplaintsTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def authorize_request_data_delete_FeedbackAndComplaints(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=FeedbackAndComplaintsLive.objects.get(pk=pk)
  
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,type='delete')
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()
        return success(req)
    
    except FeedbackAndComplaintsTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")





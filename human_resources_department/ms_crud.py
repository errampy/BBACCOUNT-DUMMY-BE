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


def create_leavemanagement(pending_leave_requests, total_leave_days_taken, average_leave_days_per_staff, highest_leave_days, lowest_leave_days, reported_date, leave_trends, leave_policy_notes):
    """
    Creates a LeaveManagement instance with the provided data.
        Args:
        pending_leave_requests, total_leave_days_taken, average_leave_days_per_staff, highest_leave_days, lowest_leave_days, reported_date, leave_trends, leave_policy_notes: Keyword arguments for LeaveManagement fields.

    Returns:
        dict: Success or error message.
        APP_NAME = __name__.split('.')[0]

    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        data={'pending_leave_requests': pending_leave_requests,
			'total_leave_days_taken': total_leave_days_taken,
			'average_leave_days_per_staff': average_leave_days_per_staff,
			'highest_leave_days': highest_leave_days,
			'lowest_leave_days': lowest_leave_days,
			'reported_date': reported_date,
			'leave_trends': leave_trends,
			'leave_policy_notes': leave_policy_notes,}
        data['code'] = generate_random_id('ABC')
        data_create = data.copy()
        data_create['code'] = generate_random_id('ABC')
        data_create['record_type']='create'
        # Initialize the serializer with the data
        serializer_temp = LeaveManagementTempSerializer(data=data_create)
        serializer_live=LeaveManagementLiveSerializer(data=data)
        
        # Validate and save the serializer data
        if serializer_live.is_valid() and serializer_temp.is_valid() :
            temp_instance = serializer_temp.save()
            type=temp_instance.record_type
            # Call auditing and authorization functions if needed
            is_audit = model_audit(request,APP_NAME,'LeaveManagement',temp_instance.pk)
            is_authorization = self_authorization(request,APP_NAME,'LeaveManagement', temp_instance.pk,type)
            
            model_name='LeaveManagement'
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

def update_leavemanagement_temp(code,pending_leave_requests=None, total_leave_days_taken=None, average_leave_days_per_staff=None, highest_leave_days=None, lowest_leave_days=None, reported_date=None, leave_trends=None, leave_policy_notes=None):
    """
    Updates a LeaveManagement instance with the provided data.
    
    Args:
        leavemanagement_id (int): ID of the LeaveManagement to update.
        pending_leave_requests=None, total_leave_days_taken=None, average_leave_days_per_staff=None, highest_leave_days=None, lowest_leave_days=None, reported_date=None, leave_trends=None, leave_policy_notes=None: Keyword arguments for LeaveManagement fields to update.

    Returns:
        dict: Success or error message.
    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if  is_have_permission(request,APP_NAME, 'LeaveManagement',code):

            data={'pending_leave_requests': pending_leave_requests,
			'total_leave_days_taken': total_leave_days_taken,
			'average_leave_days_per_staff': average_leave_days_per_staff,
			'highest_leave_days': highest_leave_days,
			'lowest_leave_days': lowest_leave_days,
			'reported_date': reported_date,
			'leave_trends': leave_trends,
			'leave_policy_notes': leave_policy_notes,}
            data['code']=code

            data['record_type']='update'
            # Initialize the serializer with the data
            serializer_temp = LeaveManagementTempSerializer(data=data)
            #serializer_live=LeaveManagementLiveSerializer(data=data)
            
            # Validate and save the serializer data
            if serializer_temp.is_valid() :
                temp_instance = serializer_temp.save()
                type=temp_instance.record_type
                # Call auditing and authorization functions if needed
                is_audit = model_audit(request,APP_NAME,'LeaveManagement',temp_instance.pk)
                is_authorization = self_authorization(request,APP_NAME,'LeaveManagement', temp_instance.pk,type)

                model_name='LeaveManagement'
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
    except  LeaveManagementTemp.DoesNotExist:
        return error('Instance does not exist')
    except ValidationError as e:
        return error(f"Validation Error: {e}")
    except Exception as e:
        return error(f"An error occurred: {e}")



def view_leavemanagement(leavemanagement_id=None):
    """
    Retrieves and serializes a LeaveManagement instance by its ID or all instances if ID is None.
    
    Args:
        LeaveManagement_id (int, optional): ID of the LeaveManagement to retrieve.

    Returns:
        dict: A success response with the serialized data if found,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if leavemanagement_id is not None:
            record = LeaveManagementTemp.objects.get(pk=leavemanagement_id)
            serializer = LeaveManagementTempSerializer(record)
        else:
            obj = LeaveManagementLive.objects.filter(is_deactivate=False)
            obj_pa = get_temp_record(request,APP_NAME,'LeaveManagement').filter(~Q(status='unauthorized_sent'))
            print('object--',obj_pa)
            obj_wait_auth = get_record_for_authorize(str(request.user.pk))
            # records = NoSeriesLinesALive.objects.all()
            live_data = LeaveManagementLiveSerializer(obj, many=True).data
            temp_data = LeaveManagementTempSerializer(obj_pa, many=True).data
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


def view_leavemanagement_single(code):
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
        

        record = LeaveManagementLive.objects.get(pk=code)
        serializer = LeaveManagementLiveSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")


def pa_leavemanagement(leavemanagement_id,model_name):
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
        
        record = LeaveManagementTemp.objects.get(pk=leavemanagement_id)
        serializer = LeaveManagementTempPASerializer(record).data
        
        type=record.record_type
        get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
        serializers=ModelRegistrationSerializer(get_table_name).data

        workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
        serializers_data=WorkflowMappingSerializer(workflow_mapping).data

        data={
            'leavemanagement':serializer,
            'table_data':serializers,
            'workflow_data':serializers_data
        }
        return success(data)
    
    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def delete_leavemanagement(leavemanagement_id,model_name):
    """
    Deletes a LeaveManagement instance with the given ID.
    
    Args:
        leavemanagement_id (int): ID of the LeaveManagement to delete.

    Returns:
        dict: A success response if deletion is successful,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        if  is_have_permission(request,APP_NAME, 'LeaveManagement', leavemanagement_id):
            type='delete'

            is_authorization = self_authorization_for_delete(request,APP_NAME,model_name, leavemanagement_id,type)
            user_ids_resp=get_next_user_from_work_flow(request,model_name,temp_instance=leavemanagement_id,type=type)
 
            sent_auth=WorkflowMapping.objects.get(table_name__model_name__iexact=model_name,workflow_type=type)
            
            record = LeaveManagementLive.objects.get(pk=leavemanagement_id)
            serializer = LeaveManagementLiveViewSerializer(record).data

            # get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
            # serializers=ModelRegistrationSerializer(get_table_name).data

            get_table_name = ModelRegistration.objects.get(model_name=model_name)
            serializers=ModelRegistrationSerializer(get_table_name).data

            print('table name of current',get_table_name)
            
            workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
            serializers_data=WorkflowMappingSerializer(workflow_mapping).data

            if user_ids_resp is not None and sent_auth.send_to_authorized == 'False' and sent_auth.same_user_authorized == 'False':

                obj = delete_record(request,APP_NAME, 'LeaveManagement', leavemanagement_id)
                return success("Successfully deleted")
            else:
                data={
                    'LeaveManagement':serializer,
                    'table_data':serializers,
                    'workflow_data':serializers_data
                }
                return success(data)
        else:
            return error('you have no permission to delete the record')
    
    except LeaveManagementLive.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def view_leavemanagement_tempdata(leavemanagement_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = LeaveManagementTemp.objects.get(code=leavemanagement_id)
        serializer = LeaveManagementTempSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")
    

def view_leavemanagement_live(leavemanagement_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = LeaveManagementLive.objects.get(code=leavemanagement_id)
        serializer = LeaveManagementLiveViewSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def authorize_request_data_LeaveManagement(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=LeaveManagementTemp.objects.get(pk=pk)
        work_flow_type=get_instance.record_type
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,work_flow_type)
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()

        return success(req)
    
    except LeaveManagementTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def authorize_request_data_delete_LeaveManagement(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=LeaveManagementLive.objects.get(pk=pk)
  
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,type='delete')
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()
        return success(req)
    
    except LeaveManagementTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")





#add foreign key import model.


def create_staffproductivity(total_loan_officers, loans_per_officer, average_portfolio_per_officer, total_loans, highest_loans_by_officer, reported_date, lowest_loans_by_officer, performance_comments):
    """
    Creates a StaffProductivity instance with the provided data.
        Args:
        total_loan_officers, loans_per_officer, average_portfolio_per_officer, total_loans, highest_loans_by_officer, reported_date, lowest_loans_by_officer, performance_comments: Keyword arguments for StaffProductivity fields.

    Returns:
        dict: Success or error message.
        APP_NAME = __name__.split('.')[0]

    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        data={'total_loan_officers': total_loan_officers,
			'loans_per_officer': loans_per_officer,
			'average_portfolio_per_officer': average_portfolio_per_officer,
			'total_loans': total_loans,
			'highest_loans_by_officer': highest_loans_by_officer,
			'reported_date': reported_date,
			'lowest_loans_by_officer': lowest_loans_by_officer,
			'performance_comments': performance_comments,}
        data['code'] = generate_random_id('ABC')
        data_create = data.copy()
        data_create['code'] = generate_random_id('ABC')
        data_create['record_type']='create'
        # Initialize the serializer with the data
        serializer_temp = StaffProductivityTempSerializer(data=data_create)
        serializer_live=StaffProductivityLiveSerializer(data=data)
        
        # Validate and save the serializer data
        if serializer_live.is_valid() and serializer_temp.is_valid() :
            temp_instance = serializer_temp.save()
            type=temp_instance.record_type
            # Call auditing and authorization functions if needed
            is_audit = model_audit(request,APP_NAME,'StaffProductivity',temp_instance.pk)
            is_authorization = self_authorization(request,APP_NAME,'StaffProductivity', temp_instance.pk,type)
            
            model_name='StaffProductivity'
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

def update_staffproductivity_temp(code,total_loan_officers=None, loans_per_officer=None, average_portfolio_per_officer=None, total_loans=None, highest_loans_by_officer=None, reported_date=None, lowest_loans_by_officer=None, performance_comments=None):
    """
    Updates a StaffProductivity instance with the provided data.
    
    Args:
        staffproductivity_id (int): ID of the StaffProductivity to update.
        total_loan_officers=None, loans_per_officer=None, average_portfolio_per_officer=None, total_loans=None, highest_loans_by_officer=None, reported_date=None, lowest_loans_by_officer=None, performance_comments=None: Keyword arguments for StaffProductivity fields to update.

    Returns:
        dict: Success or error message.
    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if  is_have_permission(request,APP_NAME, 'StaffProductivity',code):

            data={'total_loan_officers': total_loan_officers,
			'loans_per_officer': loans_per_officer,
			'average_portfolio_per_officer': average_portfolio_per_officer,
			'total_loans': total_loans,
			'highest_loans_by_officer': highest_loans_by_officer,
			'reported_date': reported_date,
			'lowest_loans_by_officer': lowest_loans_by_officer,
			'performance_comments': performance_comments,}
            data['code']=code

            data['record_type']='update'
            # Initialize the serializer with the data
            serializer_temp = StaffProductivityTempSerializer(data=data)
            #serializer_live=StaffProductivityLiveSerializer(data=data)
            
            # Validate and save the serializer data
            if serializer_temp.is_valid() :
                temp_instance = serializer_temp.save()
                type=temp_instance.record_type
                # Call auditing and authorization functions if needed
                is_audit = model_audit(request,APP_NAME,'StaffProductivity',temp_instance.pk)
                is_authorization = self_authorization(request,APP_NAME,'StaffProductivity', temp_instance.pk,type)

                model_name='StaffProductivity'
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
    except  StaffProductivityTemp.DoesNotExist:
        return error('Instance does not exist')
    except ValidationError as e:
        return error(f"Validation Error: {e}")
    except Exception as e:
        return error(f"An error occurred: {e}")



def view_staffproductivity(staffproductivity_id=None):
    """
    Retrieves and serializes a StaffProductivity instance by its ID or all instances if ID is None.
    
    Args:
        StaffProductivity_id (int, optional): ID of the StaffProductivity to retrieve.

    Returns:
        dict: A success response with the serialized data if found,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if staffproductivity_id is not None:
            record = StaffProductivityTemp.objects.get(pk=staffproductivity_id)
            serializer = StaffProductivityTempSerializer(record)
        else:
            obj = StaffProductivityLive.objects.filter(is_deactivate=False)
            obj_pa = get_temp_record(request,APP_NAME,'StaffProductivity').filter(~Q(status='unauthorized_sent'))
            print('object--',obj_pa)
            obj_wait_auth = get_record_for_authorize(str(request.user.pk))
            # records = NoSeriesLinesALive.objects.all()
            live_data = StaffProductivityLiveSerializer(obj, many=True).data
            temp_data = StaffProductivityTempSerializer(obj_pa, many=True).data
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


def view_staffproductivity_single(code):
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
        

        record = StaffProductivityLive.objects.get(pk=code)
        serializer = StaffProductivityLiveSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")


def pa_staffproductivity(staffproductivity_id,model_name):
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
        
        record = StaffProductivityTemp.objects.get(pk=staffproductivity_id)
        serializer = StaffProductivityTempPASerializer(record).data
        
        type=record.record_type
        get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
        serializers=ModelRegistrationSerializer(get_table_name).data

        workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
        serializers_data=WorkflowMappingSerializer(workflow_mapping).data

        data={
            'staffproductivity':serializer,
            'table_data':serializers,
            'workflow_data':serializers_data
        }
        return success(data)
    
    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def delete_staffproductivity(staffproductivity_id,model_name):
    """
    Deletes a StaffProductivity instance with the given ID.
    
    Args:
        staffproductivity_id (int): ID of the StaffProductivity to delete.

    Returns:
        dict: A success response if deletion is successful,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        if  is_have_permission(request,APP_NAME, 'StaffProductivity', staffproductivity_id):
            type='delete'

            is_authorization = self_authorization_for_delete(request,APP_NAME,model_name, staffproductivity_id,type)
            user_ids_resp=get_next_user_from_work_flow(request,model_name,temp_instance=staffproductivity_id,type=type)
 
            sent_auth=WorkflowMapping.objects.get(table_name__model_name__iexact=model_name,workflow_type=type)
            
            record = StaffProductivityLive.objects.get(pk=staffproductivity_id)
            serializer = StaffProductivityLiveViewSerializer(record).data

            # get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
            # serializers=ModelRegistrationSerializer(get_table_name).data

            get_table_name = ModelRegistration.objects.get(model_name=model_name)
            serializers=ModelRegistrationSerializer(get_table_name).data

            print('table name of current',get_table_name)
            
            workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
            serializers_data=WorkflowMappingSerializer(workflow_mapping).data

            if user_ids_resp is not None and sent_auth.send_to_authorized == 'False' and sent_auth.same_user_authorized == 'False':

                obj = delete_record(request,APP_NAME, 'StaffProductivity', staffproductivity_id)
                return success("Successfully deleted")
            else:
                data={
                    'StaffProductivity':serializer,
                    'table_data':serializers,
                    'workflow_data':serializers_data
                }
                return success(data)
        else:
            return error('you have no permission to delete the record')
    
    except StaffProductivityLive.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def view_staffproductivity_tempdata(staffproductivity_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = StaffProductivityTemp.objects.get(code=staffproductivity_id)
        serializer = StaffProductivityTempSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")
    

def view_staffproductivity_live(staffproductivity_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = StaffProductivityLive.objects.get(code=staffproductivity_id)
        serializer = StaffProductivityLiveViewSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def authorize_request_data_StaffProductivity(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=StaffProductivityTemp.objects.get(pk=pk)
        work_flow_type=get_instance.record_type
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,work_flow_type)
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()

        return success(req)
    
    except StaffProductivityTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def authorize_request_data_delete_StaffProductivity(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=StaffProductivityLive.objects.get(pk=pk)
  
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,type='delete')
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()
        return success(req)
    
    except StaffProductivityTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")





#add foreign key import model.


def create_trainingdevelopment(training_sessions_conducted, staff_trained, total_training_costs, average_training_cost_per_person, training_focus_areas, reported_date, training_feedback_summary):
    """
    Creates a TrainingDevelopment instance with the provided data.
        Args:
        training_sessions_conducted, staff_trained, total_training_costs, average_training_cost_per_person, training_focus_areas, reported_date, training_feedback_summary: Keyword arguments for TrainingDevelopment fields.

    Returns:
        dict: Success or error message.
        APP_NAME = __name__.split('.')[0]

    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        data={'training_sessions_conducted': training_sessions_conducted,
			'staff_trained': staff_trained,
			'total_training_costs': total_training_costs,
			'average_training_cost_per_person': average_training_cost_per_person,
			'training_focus_areas': training_focus_areas,
			'reported_date': reported_date,
			'training_feedback_summary': training_feedback_summary,}
        data['code'] = generate_random_id('ABC')
        data_create = data.copy()
        data_create['code'] = generate_random_id('ABC')
        data_create['record_type']='create'
        # Initialize the serializer with the data
        serializer_temp = TrainingDevelopmentTempSerializer(data=data_create)
        serializer_live=TrainingDevelopmentLiveSerializer(data=data)
        
        # Validate and save the serializer data
        if serializer_live.is_valid() and serializer_temp.is_valid() :
            temp_instance = serializer_temp.save()
            type=temp_instance.record_type
            # Call auditing and authorization functions if needed
            is_audit = model_audit(request,APP_NAME,'TrainingDevelopment',temp_instance.pk)
            is_authorization = self_authorization(request,APP_NAME,'TrainingDevelopment', temp_instance.pk,type)
            
            model_name='TrainingDevelopment'
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

def update_trainingdevelopment_temp(code,training_sessions_conducted=None, staff_trained=None, total_training_costs=None, average_training_cost_per_person=None, training_focus_areas=None, reported_date=None, training_feedback_summary=None):
    """
    Updates a TrainingDevelopment instance with the provided data.
    
    Args:
        trainingdevelopment_id (int): ID of the TrainingDevelopment to update.
        training_sessions_conducted=None, staff_trained=None, total_training_costs=None, average_training_cost_per_person=None, training_focus_areas=None, reported_date=None, training_feedback_summary=None: Keyword arguments for TrainingDevelopment fields to update.

    Returns:
        dict: Success or error message.
    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if  is_have_permission(request,APP_NAME, 'TrainingDevelopment',code):

            data={'training_sessions_conducted': training_sessions_conducted,
			'staff_trained': staff_trained,
			'total_training_costs': total_training_costs,
			'average_training_cost_per_person': average_training_cost_per_person,
			'training_focus_areas': training_focus_areas,
			'reported_date': reported_date,
			'training_feedback_summary': training_feedback_summary,}
            data['code']=code

            data['record_type']='update'
            # Initialize the serializer with the data
            serializer_temp = TrainingDevelopmentTempSerializer(data=data)
            #serializer_live=TrainingDevelopmentLiveSerializer(data=data)
            
            # Validate and save the serializer data
            if serializer_temp.is_valid() :
                temp_instance = serializer_temp.save()
                type=temp_instance.record_type
                # Call auditing and authorization functions if needed
                is_audit = model_audit(request,APP_NAME,'TrainingDevelopment',temp_instance.pk)
                is_authorization = self_authorization(request,APP_NAME,'TrainingDevelopment', temp_instance.pk,type)

                model_name='TrainingDevelopment'
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
    except  TrainingDevelopmentTemp.DoesNotExist:
        return error('Instance does not exist')
    except ValidationError as e:
        return error(f"Validation Error: {e}")
    except Exception as e:
        return error(f"An error occurred: {e}")



def view_trainingdevelopment(trainingdevelopment_id=None):
    """
    Retrieves and serializes a TrainingDevelopment instance by its ID or all instances if ID is None.
    
    Args:
        TrainingDevelopment_id (int, optional): ID of the TrainingDevelopment to retrieve.

    Returns:
        dict: A success response with the serialized data if found,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if trainingdevelopment_id is not None:
            record = TrainingDevelopmentTemp.objects.get(pk=trainingdevelopment_id)
            serializer = TrainingDevelopmentTempSerializer(record)
        else:
            obj = TrainingDevelopmentLive.objects.filter(is_deactivate=False)
            obj_pa = get_temp_record(request,APP_NAME,'TrainingDevelopment').filter(~Q(status='unauthorized_sent'))
            print('object--',obj_pa)
            obj_wait_auth = get_record_for_authorize(str(request.user.pk))
            # records = NoSeriesLinesALive.objects.all()
            live_data = TrainingDevelopmentLiveSerializer(obj, many=True).data
            temp_data = TrainingDevelopmentTempSerializer(obj_pa, many=True).data
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


def view_trainingdevelopment_single(code):
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
        

        record = TrainingDevelopmentLive.objects.get(pk=code)
        serializer = TrainingDevelopmentLiveSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")


def pa_trainingdevelopment(trainingdevelopment_id,model_name):
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
        
        record = TrainingDevelopmentTemp.objects.get(pk=trainingdevelopment_id)
        serializer = TrainingDevelopmentTempPASerializer(record).data
        
        type=record.record_type
        get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
        serializers=ModelRegistrationSerializer(get_table_name).data

        workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
        serializers_data=WorkflowMappingSerializer(workflow_mapping).data

        data={
            'trainingdevelopment':serializer,
            'table_data':serializers,
            'workflow_data':serializers_data
        }
        return success(data)
    
    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def delete_trainingdevelopment(trainingdevelopment_id,model_name):
    """
    Deletes a TrainingDevelopment instance with the given ID.
    
    Args:
        trainingdevelopment_id (int): ID of the TrainingDevelopment to delete.

    Returns:
        dict: A success response if deletion is successful,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        if  is_have_permission(request,APP_NAME, 'TrainingDevelopment', trainingdevelopment_id):
            type='delete'

            is_authorization = self_authorization_for_delete(request,APP_NAME,model_name, trainingdevelopment_id,type)
            user_ids_resp=get_next_user_from_work_flow(request,model_name,temp_instance=trainingdevelopment_id,type=type)
 
            sent_auth=WorkflowMapping.objects.get(table_name__model_name__iexact=model_name,workflow_type=type)
            
            record = TrainingDevelopmentLive.objects.get(pk=trainingdevelopment_id)
            serializer = TrainingDevelopmentLiveViewSerializer(record).data

            # get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
            # serializers=ModelRegistrationSerializer(get_table_name).data

            get_table_name = ModelRegistration.objects.get(model_name=model_name)
            serializers=ModelRegistrationSerializer(get_table_name).data

            print('table name of current',get_table_name)
            
            workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
            serializers_data=WorkflowMappingSerializer(workflow_mapping).data

            if user_ids_resp is not None and sent_auth.send_to_authorized == 'False' and sent_auth.same_user_authorized == 'False':

                obj = delete_record(request,APP_NAME, 'TrainingDevelopment', trainingdevelopment_id)
                return success("Successfully deleted")
            else:
                data={
                    'TrainingDevelopment':serializer,
                    'table_data':serializers,
                    'workflow_data':serializers_data
                }
                return success(data)
        else:
            return error('you have no permission to delete the record')
    
    except TrainingDevelopmentLive.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def view_trainingdevelopment_tempdata(trainingdevelopment_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = TrainingDevelopmentTemp.objects.get(code=trainingdevelopment_id)
        serializer = TrainingDevelopmentTempSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")
    

def view_trainingdevelopment_live(trainingdevelopment_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = TrainingDevelopmentLive.objects.get(code=trainingdevelopment_id)
        serializer = TrainingDevelopmentLiveViewSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def authorize_request_data_TrainingDevelopment(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=TrainingDevelopmentTemp.objects.get(pk=pk)
        work_flow_type=get_instance.record_type
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,work_flow_type)
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()

        return success(req)
    
    except TrainingDevelopmentTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def authorize_request_data_delete_TrainingDevelopment(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=TrainingDevelopmentLive.objects.get(pk=pk)
  
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,type='delete')
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()
        return success(req)
    
    except TrainingDevelopmentTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")





#add foreign key import model.


def create_staffturnover(total_departures, total_new_hires, turnover_rate, current_staff_count, total_staff_at_start, reported_date, key_departures, hiring_notes):
    """
    Creates a StaffTurnover instance with the provided data.
        Args:
        total_departures, total_new_hires, turnover_rate, current_staff_count, total_staff_at_start, reported_date, key_departures, hiring_notes: Keyword arguments for StaffTurnover fields.

    Returns:
        dict: Success or error message.
        APP_NAME = __name__.split('.')[0]

    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        data={'total_departures': total_departures,
			'total_new_hires': total_new_hires,
			'turnover_rate': turnover_rate,
			'current_staff_count': current_staff_count,
			'total_staff_at_start': total_staff_at_start,
			'reported_date': reported_date,
			'key_departures': key_departures,
			'hiring_notes': hiring_notes,}
        data['code'] = generate_random_id('ABC')
        data_create = data.copy()
        data_create['code'] = generate_random_id('ABC')
        data_create['record_type']='create'
        # Initialize the serializer with the data
        serializer_temp = StaffTurnoverTempSerializer(data=data_create)
        serializer_live=StaffTurnoverLiveSerializer(data=data)
        
        # Validate and save the serializer data
        if serializer_live.is_valid() and serializer_temp.is_valid() :
            temp_instance = serializer_temp.save()
            type=temp_instance.record_type
            # Call auditing and authorization functions if needed
            is_audit = model_audit(request,APP_NAME,'StaffTurnover',temp_instance.pk)
            is_authorization = self_authorization(request,APP_NAME,'StaffTurnover', temp_instance.pk,type)
            
            model_name='StaffTurnover'
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

def update_staffturnover_temp(code,total_departures=None, total_new_hires=None, turnover_rate=None, current_staff_count=None, total_staff_at_start=None, reported_date=None, key_departures=None, hiring_notes=None):
    """
    Updates a StaffTurnover instance with the provided data.
    
    Args:
        staffturnover_id (int): ID of the StaffTurnover to update.
        total_departures=None, total_new_hires=None, turnover_rate=None, current_staff_count=None, total_staff_at_start=None, reported_date=None, key_departures=None, hiring_notes=None: Keyword arguments for StaffTurnover fields to update.

    Returns:
        dict: Success or error message.
    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if  is_have_permission(request,APP_NAME, 'StaffTurnover',code):

            data={'total_departures': total_departures,
			'total_new_hires': total_new_hires,
			'turnover_rate': turnover_rate,
			'current_staff_count': current_staff_count,
			'total_staff_at_start': total_staff_at_start,
			'reported_date': reported_date,
			'key_departures': key_departures,
			'hiring_notes': hiring_notes,}
            data['code']=code

            data['record_type']='update'
            # Initialize the serializer with the data
            serializer_temp = StaffTurnoverTempSerializer(data=data)
            #serializer_live=StaffTurnoverLiveSerializer(data=data)
            
            # Validate and save the serializer data
            if serializer_temp.is_valid() :
                temp_instance = serializer_temp.save()
                type=temp_instance.record_type
                # Call auditing and authorization functions if needed
                is_audit = model_audit(request,APP_NAME,'StaffTurnover',temp_instance.pk)
                is_authorization = self_authorization(request,APP_NAME,'StaffTurnover', temp_instance.pk,type)

                model_name='StaffTurnover'
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
    except  StaffTurnoverTemp.DoesNotExist:
        return error('Instance does not exist')
    except ValidationError as e:
        return error(f"Validation Error: {e}")
    except Exception as e:
        return error(f"An error occurred: {e}")



def view_staffturnover(staffturnover_id=None):
    """
    Retrieves and serializes a StaffTurnover instance by its ID or all instances if ID is None.
    
    Args:
        StaffTurnover_id (int, optional): ID of the StaffTurnover to retrieve.

    Returns:
        dict: A success response with the serialized data if found,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if staffturnover_id is not None:
            record = StaffTurnoverTemp.objects.get(pk=staffturnover_id)
            serializer = StaffTurnoverTempSerializer(record)
        else:
            obj = StaffTurnoverLive.objects.filter(is_deactivate=False)
            obj_pa = get_temp_record(request,APP_NAME,'StaffTurnover').filter(~Q(status='unauthorized_sent'))
            print('object--',obj_pa)
            obj_wait_auth = get_record_for_authorize(str(request.user.pk))
            # records = NoSeriesLinesALive.objects.all()
            live_data = StaffTurnoverLiveSerializer(obj, many=True).data
            temp_data = StaffTurnoverTempSerializer(obj_pa, many=True).data
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


def view_staffturnover_single(code):
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
        

        record = StaffTurnoverLive.objects.get(pk=code)
        serializer = StaffTurnoverLiveSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")


def pa_staffturnover(staffturnover_id,model_name):
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
        
        record = StaffTurnoverTemp.objects.get(pk=staffturnover_id)
        serializer = StaffTurnoverTempPASerializer(record).data
        
        type=record.record_type
        get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
        serializers=ModelRegistrationSerializer(get_table_name).data

        workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
        serializers_data=WorkflowMappingSerializer(workflow_mapping).data

        data={
            'staffturnover':serializer,
            'table_data':serializers,
            'workflow_data':serializers_data
        }
        return success(data)
    
    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def delete_staffturnover(staffturnover_id,model_name):
    """
    Deletes a StaffTurnover instance with the given ID.
    
    Args:
        staffturnover_id (int): ID of the StaffTurnover to delete.

    Returns:
        dict: A success response if deletion is successful,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        if  is_have_permission(request,APP_NAME, 'StaffTurnover', staffturnover_id):
            type='delete'

            is_authorization = self_authorization_for_delete(request,APP_NAME,model_name, staffturnover_id,type)
            user_ids_resp=get_next_user_from_work_flow(request,model_name,temp_instance=staffturnover_id,type=type)
 
            sent_auth=WorkflowMapping.objects.get(table_name__model_name__iexact=model_name,workflow_type=type)
            
            record = StaffTurnoverLive.objects.get(pk=staffturnover_id)
            serializer = StaffTurnoverLiveViewSerializer(record).data

            # get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
            # serializers=ModelRegistrationSerializer(get_table_name).data

            get_table_name = ModelRegistration.objects.get(model_name=model_name)
            serializers=ModelRegistrationSerializer(get_table_name).data

            print('table name of current',get_table_name)
            
            workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
            serializers_data=WorkflowMappingSerializer(workflow_mapping).data

            if user_ids_resp is not None and sent_auth.send_to_authorized == 'False' and sent_auth.same_user_authorized == 'False':

                obj = delete_record(request,APP_NAME, 'StaffTurnover', staffturnover_id)
                return success("Successfully deleted")
            else:
                data={
                    'StaffTurnover':serializer,
                    'table_data':serializers,
                    'workflow_data':serializers_data
                }
                return success(data)
        else:
            return error('you have no permission to delete the record')
    
    except StaffTurnoverLive.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def view_staffturnover_tempdata(staffturnover_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = StaffTurnoverTemp.objects.get(code=staffturnover_id)
        serializer = StaffTurnoverTempSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")
    

def view_staffturnover_live(staffturnover_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = StaffTurnoverLive.objects.get(code=staffturnover_id)
        serializer = StaffTurnoverLiveViewSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def authorize_request_data_StaffTurnover(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=StaffTurnoverTemp.objects.get(pk=pk)
        work_flow_type=get_instance.record_type
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,work_flow_type)
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()

        return success(req)
    
    except StaffTurnoverTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def authorize_request_data_delete_StaffTurnover(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=StaffTurnoverLive.objects.get(pk=pk)
  
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,type='delete')
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()
        return success(req)
    
    except StaffTurnoverTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")





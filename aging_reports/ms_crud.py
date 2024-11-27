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


def create_loanaging(overdue_0_30_days, overdue_31_60_days, overdue_61_90_days, overdue_91_days_plus, total_outstanding_loans, reported_date, comments):
    """
    Creates a LoanAging instance with the provided data.
        Args:
        overdue_0_30_days, overdue_31_60_days, overdue_61_90_days, overdue_91_days_plus, total_outstanding_loans, reported_date, comments: Keyword arguments for LoanAging fields.

    Returns:
        dict: Success or error message.
        APP_NAME = __name__.split('.')[0]

    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        data={'overdue_0_30_days': overdue_0_30_days,
			'overdue_31_60_days': overdue_31_60_days,
			'overdue_61_90_days': overdue_61_90_days,
			'overdue_91_days_plus': overdue_91_days_plus,
			'total_outstanding_loans': total_outstanding_loans,
			'reported_date': reported_date,
			'comments': comments,}
        data['code'] = generate_random_id('ABC')
        data_create = data.copy()
        data_create['code'] = generate_random_id('ABC')
        data_create['record_type']='create'
        # Initialize the serializer with the data
        serializer_temp = LoanAgingTempSerializer(data=data_create)
        serializer_live=LoanAgingLiveSerializer(data=data)
        
        # Validate and save the serializer data
        if serializer_live.is_valid() and serializer_temp.is_valid() :
            temp_instance = serializer_temp.save()
            type=temp_instance.record_type
            # Call auditing and authorization functions if needed
            is_audit = model_audit(request,APP_NAME,'LoanAging',temp_instance.pk)
            is_authorization = self_authorization(request,APP_NAME,'LoanAging', temp_instance.pk,type)
            
            model_name='LoanAging'
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

def update_loanaging_temp(code,overdue_0_30_days=None, overdue_31_60_days=None, overdue_61_90_days=None, overdue_91_days_plus=None, total_outstanding_loans=None, reported_date=None, comments=None):
    """
    Updates a LoanAging instance with the provided data.
    
    Args:
        loanaging_id (int): ID of the LoanAging to update.
        overdue_0_30_days=None, overdue_31_60_days=None, overdue_61_90_days=None, overdue_91_days_plus=None, total_outstanding_loans=None, reported_date=None, comments=None: Keyword arguments for LoanAging fields to update.

    Returns:
        dict: Success or error message.
    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if  is_have_permission(request,APP_NAME, 'LoanAging',code):

            data={'overdue_0_30_days': overdue_0_30_days,
			'overdue_31_60_days': overdue_31_60_days,
			'overdue_61_90_days': overdue_61_90_days,
			'overdue_91_days_plus': overdue_91_days_plus,
			'total_outstanding_loans': total_outstanding_loans,
			'reported_date': reported_date,
			'comments': comments,}
            data['code']=code

            data['record_type']='update'
            # Initialize the serializer with the data
            serializer_temp = LoanAgingTempSerializer(data=data)
            #serializer_live=LoanAgingLiveSerializer(data=data)
            
            # Validate and save the serializer data
            if serializer_temp.is_valid() :
                temp_instance = serializer_temp.save()
                type=temp_instance.record_type
                # Call auditing and authorization functions if needed
                is_audit = model_audit(request,APP_NAME,'LoanAging',temp_instance.pk)
                is_authorization = self_authorization(request,APP_NAME,'LoanAging', temp_instance.pk,type)

                model_name='LoanAging'
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
    except  LoanAgingTemp.DoesNotExist:
        return error('Instance does not exist')
    except ValidationError as e:
        return error(f"Validation Error: {e}")
    except Exception as e:
        return error(f"An error occurred: {e}")



def view_loanaging(loanaging_id=None):
    """
    Retrieves and serializes a LoanAging instance by its ID or all instances if ID is None.
    
    Args:
        LoanAging_id (int, optional): ID of the LoanAging to retrieve.

    Returns:
        dict: A success response with the serialized data if found,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if loanaging_id is not None:
            record = LoanAgingTemp.objects.get(pk=loanaging_id)
            serializer = LoanAgingTempSerializer(record)
        else:
            obj = LoanAgingLive.objects.filter(is_deactivate=False)
            obj_pa = get_temp_record(request,APP_NAME,'LoanAging').filter(~Q(status='unauthorized_sent'))
            print('object--',obj_pa)
            obj_wait_auth = get_record_for_authorize(str(request.user.pk))
            # records = NoSeriesLinesALive.objects.all()
            live_data = LoanAgingLiveSerializer(obj, many=True).data
            temp_data = LoanAgingTempSerializer(obj_pa, many=True).data
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


def view_loanaging_single(code):
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
        

        record = LoanAgingLive.objects.get(pk=code)
        serializer = LoanAgingLiveSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")


def pa_loanaging(loanaging_id,model_name):
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
        
        record = LoanAgingTemp.objects.get(pk=loanaging_id)
        serializer = LoanAgingTempPASerializer(record).data
        
        type=record.record_type
        get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
        serializers=ModelRegistrationSerializer(get_table_name).data

        workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
        serializers_data=WorkflowMappingSerializer(workflow_mapping).data

        data={
            'loanaging':serializer,
            'table_data':serializers,
            'workflow_data':serializers_data
        }
        return success(data)
    
    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def delete_loanaging(loanaging_id,model_name):
    """
    Deletes a LoanAging instance with the given ID.
    
    Args:
        loanaging_id (int): ID of the LoanAging to delete.

    Returns:
        dict: A success response if deletion is successful,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        if  is_have_permission(request,APP_NAME, 'LoanAging', loanaging_id):
            type='delete'

            is_authorization = self_authorization_for_delete(request,APP_NAME,model_name, loanaging_id,type)
            user_ids_resp=get_next_user_from_work_flow(request,model_name,temp_instance=loanaging_id,type=type)
 
            sent_auth=WorkflowMapping.objects.get(table_name__model_name__iexact=model_name,workflow_type=type)
            
            record = LoanAgingLive.objects.get(pk=loanaging_id)
            serializer = LoanAgingLiveViewSerializer(record).data

            # get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
            # serializers=ModelRegistrationSerializer(get_table_name).data

            get_table_name = ModelRegistration.objects.get(model_name=model_name)
            serializers=ModelRegistrationSerializer(get_table_name).data

            print('table name of current',get_table_name)
            
            workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
            serializers_data=WorkflowMappingSerializer(workflow_mapping).data

            if user_ids_resp is not None and sent_auth.send_to_authorized == 'False' and sent_auth.same_user_authorized == 'False':

                obj = delete_record(request,APP_NAME, 'LoanAging', loanaging_id)
                return success("Successfully deleted")
            else:
                data={
                    'LoanAging':serializer,
                    'table_data':serializers,
                    'workflow_data':serializers_data
                }
                return success(data)
        else:
            return error('you have no permission to delete the record')
    
    except LoanAgingLive.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def view_loanaging_tempdata(loanaging_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = LoanAgingTemp.objects.get(code=loanaging_id)
        serializer = LoanAgingTempSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")
    

def view_loanaging_live(loanaging_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = LoanAgingLive.objects.get(code=loanaging_id)
        serializer = LoanAgingLiveViewSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def authorize_request_data_LoanAging(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=LoanAgingTemp.objects.get(pk=pk)
        work_flow_type=get_instance.record_type
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,work_flow_type)
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()

        return success(req)
    
    except LoanAgingTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def authorize_request_data_delete_LoanAging(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=LoanAgingLive.objects.get(pk=pk)
  
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,type='delete')
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()
        return success(req)
    
    except LoanAgingTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")





#add foreign key import model.


def create_accountsreceivableaging(current, overdue_30_days, overdue_60_days, overdue_90_days, overdue_90_days_plus, reported_date, total_receivables, comments):
    """
    Creates a AccountsReceivableAging instance with the provided data.
        Args:
        current, overdue_30_days, overdue_60_days, overdue_90_days, overdue_90_days_plus, reported_date, total_receivables, comments: Keyword arguments for AccountsReceivableAging fields.

    Returns:
        dict: Success or error message.
        APP_NAME = __name__.split('.')[0]

    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        data={'current': current,
			'overdue_30_days': overdue_30_days,
			'overdue_60_days': overdue_60_days,
			'overdue_90_days': overdue_90_days,
			'overdue_90_days_plus': overdue_90_days_plus,
			'reported_date': reported_date,
			'total_receivables': total_receivables,
			'comments': comments,}
        data['code'] = generate_random_id('ABC')
        data_create = data.copy()
        data_create['code'] = generate_random_id('ABC')
        data_create['record_type']='create'
        # Initialize the serializer with the data
        serializer_temp = AccountsReceivableAgingTempSerializer(data=data_create)
        serializer_live=AccountsReceivableAgingLiveSerializer(data=data)
        
        # Validate and save the serializer data
        if serializer_live.is_valid() and serializer_temp.is_valid() :
            temp_instance = serializer_temp.save()
            type=temp_instance.record_type
            # Call auditing and authorization functions if needed
            is_audit = model_audit(request,APP_NAME,'AccountsReceivableAging',temp_instance.pk)
            is_authorization = self_authorization(request,APP_NAME,'AccountsReceivableAging', temp_instance.pk,type)
            
            model_name='AccountsReceivableAging'
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

def update_accountsreceivableaging_temp(code,current=None, overdue_30_days=None, overdue_60_days=None, overdue_90_days=None, overdue_90_days_plus=None, reported_date=None, total_receivables=None, comments=None):
    """
    Updates a AccountsReceivableAging instance with the provided data.
    
    Args:
        accountsreceivableaging_id (int): ID of the AccountsReceivableAging to update.
        current=None, overdue_30_days=None, overdue_60_days=None, overdue_90_days=None, overdue_90_days_plus=None, reported_date=None, total_receivables=None, comments=None: Keyword arguments for AccountsReceivableAging fields to update.

    Returns:
        dict: Success or error message.
    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if  is_have_permission(request,APP_NAME, 'AccountsReceivableAging',code):

            data={'current': current,
			'overdue_30_days': overdue_30_days,
			'overdue_60_days': overdue_60_days,
			'overdue_90_days': overdue_90_days,
			'overdue_90_days_plus': overdue_90_days_plus,
			'reported_date': reported_date,
			'total_receivables': total_receivables,
			'comments': comments,}
            data['code']=code

            data['record_type']='update'
            # Initialize the serializer with the data
            serializer_temp = AccountsReceivableAgingTempSerializer(data=data)
            #serializer_live=AccountsReceivableAgingLiveSerializer(data=data)
            
            # Validate and save the serializer data
            if serializer_temp.is_valid() :
                temp_instance = serializer_temp.save()
                type=temp_instance.record_type
                # Call auditing and authorization functions if needed
                is_audit = model_audit(request,APP_NAME,'AccountsReceivableAging',temp_instance.pk)
                is_authorization = self_authorization(request,APP_NAME,'AccountsReceivableAging', temp_instance.pk,type)

                model_name='AccountsReceivableAging'
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
    except  AccountsReceivableAgingTemp.DoesNotExist:
        return error('Instance does not exist')
    except ValidationError as e:
        return error(f"Validation Error: {e}")
    except Exception as e:
        return error(f"An error occurred: {e}")



def view_accountsreceivableaging(accountsreceivableaging_id=None):
    """
    Retrieves and serializes a AccountsReceivableAging instance by its ID or all instances if ID is None.
    
    Args:
        AccountsReceivableAging_id (int, optional): ID of the AccountsReceivableAging to retrieve.

    Returns:
        dict: A success response with the serialized data if found,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if accountsreceivableaging_id is not None:
            record = AccountsReceivableAgingTemp.objects.get(pk=accountsreceivableaging_id)
            serializer = AccountsReceivableAgingTempSerializer(record)
        else:
            obj = AccountsReceivableAgingLive.objects.filter(is_deactivate=False)
            obj_pa = get_temp_record(request,APP_NAME,'AccountsReceivableAging').filter(~Q(status='unauthorized_sent'))
            print('object--',obj_pa)
            obj_wait_auth = get_record_for_authorize(str(request.user.pk))
            # records = NoSeriesLinesALive.objects.all()
            live_data = AccountsReceivableAgingLiveSerializer(obj, many=True).data
            temp_data = AccountsReceivableAgingTempSerializer(obj_pa, many=True).data
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


def view_accountsreceivableaging_single(code):
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
        

        record = AccountsReceivableAgingLive.objects.get(pk=code)
        serializer = AccountsReceivableAgingLiveSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")


def pa_accountsreceivableaging(accountsreceivableaging_id,model_name):
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
        
        record = AccountsReceivableAgingTemp.objects.get(pk=accountsreceivableaging_id)
        serializer = AccountsReceivableAgingTempPASerializer(record).data
        
        type=record.record_type
        get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
        serializers=ModelRegistrationSerializer(get_table_name).data

        workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
        serializers_data=WorkflowMappingSerializer(workflow_mapping).data

        data={
            'accountsreceivableaging':serializer,
            'table_data':serializers,
            'workflow_data':serializers_data
        }
        return success(data)
    
    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def delete_accountsreceivableaging(accountsreceivableaging_id,model_name):
    """
    Deletes a AccountsReceivableAging instance with the given ID.
    
    Args:
        accountsreceivableaging_id (int): ID of the AccountsReceivableAging to delete.

    Returns:
        dict: A success response if deletion is successful,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        if  is_have_permission(request,APP_NAME, 'AccountsReceivableAging', accountsreceivableaging_id):
            type='delete'

            is_authorization = self_authorization_for_delete(request,APP_NAME,model_name, accountsreceivableaging_id,type)
            user_ids_resp=get_next_user_from_work_flow(request,model_name,temp_instance=accountsreceivableaging_id,type=type)
 
            sent_auth=WorkflowMapping.objects.get(table_name__model_name__iexact=model_name,workflow_type=type)
            
            record = AccountsReceivableAgingLive.objects.get(pk=accountsreceivableaging_id)
            serializer = AccountsReceivableAgingLiveViewSerializer(record).data

            # get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
            # serializers=ModelRegistrationSerializer(get_table_name).data

            get_table_name = ModelRegistration.objects.get(model_name=model_name)
            serializers=ModelRegistrationSerializer(get_table_name).data

            print('table name of current',get_table_name)
            
            workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
            serializers_data=WorkflowMappingSerializer(workflow_mapping).data

            if user_ids_resp is not None and sent_auth.send_to_authorized == 'False' and sent_auth.same_user_authorized == 'False':

                obj = delete_record(request,APP_NAME, 'AccountsReceivableAging', accountsreceivableaging_id)
                return success("Successfully deleted")
            else:
                data={
                    'AccountsReceivableAging':serializer,
                    'table_data':serializers,
                    'workflow_data':serializers_data
                }
                return success(data)
        else:
            return error('you have no permission to delete the record')
    
    except AccountsReceivableAgingLive.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def view_accountsreceivableaging_tempdata(accountsreceivableaging_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = AccountsReceivableAgingTemp.objects.get(code=accountsreceivableaging_id)
        serializer = AccountsReceivableAgingTempSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")
    

def view_accountsreceivableaging_live(accountsreceivableaging_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = AccountsReceivableAgingLive.objects.get(code=accountsreceivableaging_id)
        serializer = AccountsReceivableAgingLiveViewSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def authorize_request_data_AccountsReceivableAging(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=AccountsReceivableAgingTemp.objects.get(pk=pk)
        work_flow_type=get_instance.record_type
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,work_flow_type)
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()

        return success(req)
    
    except AccountsReceivableAgingTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def authorize_request_data_delete_AccountsReceivableAging(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=AccountsReceivableAgingLive.objects.get(pk=pk)
  
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,type='delete')
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()
        return success(req)
    
    except AccountsReceivableAgingTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")





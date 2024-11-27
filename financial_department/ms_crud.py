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


def create_loanlossprovision(loans_at_risk, provision_rate, required_provisions, loan_categories, remarks, reported_date):
    """
    Creates a LoanLossProvision instance with the provided data.
        Args:
        loans_at_risk, provision_rate, required_provisions, loan_categories, remarks, reported_date: Keyword arguments for LoanLossProvision fields.

    Returns:
        dict: Success or error message.
        APP_NAME = __name__.split('.')[0]

    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        data={'loans_at_risk': loans_at_risk,
			'provision_rate': provision_rate,
			'required_provisions': required_provisions,
			'loan_categories': loan_categories,
			'remarks': remarks,
			'reported_date': reported_date,}
        data['code'] = generate_random_id('ABC')
        data_create = data.copy()
        data_create['code'] = generate_random_id('ABC')
        data_create['record_type']='create'
        # Initialize the serializer with the data
        serializer_temp = LoanLossProvisionTempSerializer(data=data_create)
        serializer_live=LoanLossProvisionLiveSerializer(data=data)
        
        # Validate and save the serializer data
        if serializer_live.is_valid() and serializer_temp.is_valid() :
            temp_instance = serializer_temp.save()
            type=temp_instance.record_type
            # Call auditing and authorization functions if needed
            is_audit = model_audit(request,APP_NAME,'LoanLossProvision',temp_instance.pk)
            is_authorization = self_authorization(request,APP_NAME,'LoanLossProvision', temp_instance.pk,type)
            
            model_name='LoanLossProvision'
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

def update_loanlossprovision_temp(code,loans_at_risk=None, provision_rate=None, required_provisions=None, loan_categories=None, remarks=None, reported_date=None):
    """
    Updates a LoanLossProvision instance with the provided data.
    
    Args:
        loanlossprovision_id (int): ID of the LoanLossProvision to update.
        loans_at_risk=None, provision_rate=None, required_provisions=None, loan_categories=None, remarks=None, reported_date=None: Keyword arguments for LoanLossProvision fields to update.

    Returns:
        dict: Success or error message.
    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if  is_have_permission(request,APP_NAME, 'LoanLossProvision',code):

            data={'loans_at_risk': loans_at_risk,
			'provision_rate': provision_rate,
			'required_provisions': required_provisions,
			'loan_categories': loan_categories,
			'remarks': remarks,
			'reported_date': reported_date,}
            data['code']=code

            data['record_type']='update'
            # Initialize the serializer with the data
            serializer_temp = LoanLossProvisionTempSerializer(data=data)
            #serializer_live=LoanLossProvisionLiveSerializer(data=data)
            
            # Validate and save the serializer data
            if serializer_temp.is_valid() :
                temp_instance = serializer_temp.save()
                type=temp_instance.record_type
                # Call auditing and authorization functions if needed
                is_audit = model_audit(request,APP_NAME,'LoanLossProvision',temp_instance.pk)
                is_authorization = self_authorization(request,APP_NAME,'LoanLossProvision', temp_instance.pk,type)

                model_name='LoanLossProvision'
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
    except  LoanLossProvisionTemp.DoesNotExist:
        return error('Instance does not exist')
    except ValidationError as e:
        return error(f"Validation Error: {e}")
    except Exception as e:
        return error(f"An error occurred: {e}")



def view_loanlossprovision(loanlossprovision_id=None):
    """
    Retrieves and serializes a LoanLossProvision instance by its ID or all instances if ID is None.
    
    Args:
        LoanLossProvision_id (int, optional): ID of the LoanLossProvision to retrieve.

    Returns:
        dict: A success response with the serialized data if found,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if loanlossprovision_id is not None:
            record = LoanLossProvisionTemp.objects.get(pk=loanlossprovision_id)
            serializer = LoanLossProvisionTempSerializer(record)
        else:
            obj = LoanLossProvisionLive.objects.filter(is_deactivate=False)
            obj_pa = get_temp_record(request,APP_NAME,'LoanLossProvision').filter(~Q(status='unauthorized_sent'))
            print('object--',obj_pa)
            obj_wait_auth = get_record_for_authorize(str(request.user.pk))
            # records = NoSeriesLinesALive.objects.all()
            live_data = LoanLossProvisionLiveSerializer(obj, many=True).data
            temp_data = LoanLossProvisionTempSerializer(obj_pa, many=True).data
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


def view_loanlossprovision_single(code):
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
        

        record = LoanLossProvisionLive.objects.get(pk=code)
        serializer = LoanLossProvisionLiveSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")


def pa_loanlossprovision(loanlossprovision_id,model_name):
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
        
        record = LoanLossProvisionTemp.objects.get(pk=loanlossprovision_id)
        serializer = LoanLossProvisionTempPASerializer(record).data
        
        type=record.record_type
        get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
        serializers=ModelRegistrationSerializer(get_table_name).data

        workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
        serializers_data=WorkflowMappingSerializer(workflow_mapping).data

        data={
            'loanlossprovision':serializer,
            'table_data':serializers,
            'workflow_data':serializers_data
        }
        return success(data)
    
    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def delete_loanlossprovision(loanlossprovision_id,model_name):
    """
    Deletes a LoanLossProvision instance with the given ID.
    
    Args:
        loanlossprovision_id (int): ID of the LoanLossProvision to delete.

    Returns:
        dict: A success response if deletion is successful,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        if  is_have_permission(request,APP_NAME, 'LoanLossProvision', loanlossprovision_id):
            type='delete'

            is_authorization = self_authorization_for_delete(request,APP_NAME,model_name, loanlossprovision_id,type)
            user_ids_resp=get_next_user_from_work_flow(request,model_name,temp_instance=loanlossprovision_id,type=type)
 
            sent_auth=WorkflowMapping.objects.get(table_name__model_name__iexact=model_name,workflow_type=type)
            
            record = LoanLossProvisionLive.objects.get(pk=loanlossprovision_id)
            serializer = LoanLossProvisionLiveViewSerializer(record).data

            # get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
            # serializers=ModelRegistrationSerializer(get_table_name).data

            get_table_name = ModelRegistration.objects.get(model_name=model_name)
            serializers=ModelRegistrationSerializer(get_table_name).data

            print('table name of current',get_table_name)
            
            workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
            serializers_data=WorkflowMappingSerializer(workflow_mapping).data

            if user_ids_resp is not None and sent_auth.send_to_authorized == 'False' and sent_auth.same_user_authorized == 'False':

                obj = delete_record(request,APP_NAME, 'LoanLossProvision', loanlossprovision_id)
                return success("Successfully deleted")
            else:
                data={
                    'LoanLossProvision':serializer,
                    'table_data':serializers,
                    'workflow_data':serializers_data
                }
                return success(data)
        else:
            return error('you have no permission to delete the record')
    
    except LoanLossProvisionLive.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def view_loanlossprovision_tempdata(loanlossprovision_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = LoanLossProvisionTemp.objects.get(code=loanlossprovision_id)
        serializer = LoanLossProvisionTempSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")
    

def view_loanlossprovision_live(loanlossprovision_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = LoanLossProvisionLive.objects.get(code=loanlossprovision_id)
        serializer = LoanLossProvisionLiveViewSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def authorize_request_data_LoanLossProvision(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=LoanLossProvisionTemp.objects.get(pk=pk)
        work_flow_type=get_instance.record_type
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,work_flow_type)
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()

        return success(req)
    
    except LoanLossProvisionTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def authorize_request_data_delete_LoanLossProvision(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=LoanLossProvisionLive.objects.get(pk=pk)
  
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,type='delete')
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()
        return success(req)
    
    except LoanLossProvisionTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")





#add foreign key import model.


def create_balancesheet(assets, liabilities, equity, asset_breakdown, liability_breakdown, reported_date):
    """
    Creates a BalanceSheet instance with the provided data.
        Args:
        assets, liabilities, equity, asset_breakdown, liability_breakdown, reported_date: Keyword arguments for BalanceSheet fields.

    Returns:
        dict: Success or error message.
        APP_NAME = __name__.split('.')[0]

    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        data={'assets': assets,
			'liabilities': liabilities,
			'equity': equity,
			'asset_breakdown': asset_breakdown,
			'liability_breakdown': liability_breakdown,
			'reported_date': reported_date,}
        data['code'] = generate_random_id('ABC')
        data_create = data.copy()
        data_create['code'] = generate_random_id('ABC')
        data_create['record_type']='create'
        # Initialize the serializer with the data
        serializer_temp = BalanceSheetTempSerializer(data=data_create)
        serializer_live=BalanceSheetLiveSerializer(data=data)
        
        # Validate and save the serializer data
        if serializer_live.is_valid() and serializer_temp.is_valid() :
            temp_instance = serializer_temp.save()
            type=temp_instance.record_type
            # Call auditing and authorization functions if needed
            is_audit = model_audit(request,APP_NAME,'BalanceSheet',temp_instance.pk)
            is_authorization = self_authorization(request,APP_NAME,'BalanceSheet', temp_instance.pk,type)
            
            model_name='BalanceSheet'
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

def update_balancesheet_temp(code,assets=None, liabilities=None, equity=None, asset_breakdown=None, liability_breakdown=None, reported_date=None):
    """
    Updates a BalanceSheet instance with the provided data.
    
    Args:
        balancesheet_id (int): ID of the BalanceSheet to update.
        assets=None, liabilities=None, equity=None, asset_breakdown=None, liability_breakdown=None, reported_date=None: Keyword arguments for BalanceSheet fields to update.

    Returns:
        dict: Success or error message.
    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if  is_have_permission(request,APP_NAME, 'BalanceSheet',code):

            data={'assets': assets,
			'liabilities': liabilities,
			'equity': equity,
			'asset_breakdown': asset_breakdown,
			'liability_breakdown': liability_breakdown,
			'reported_date': reported_date,}
            data['code']=code

            data['record_type']='update'
            # Initialize the serializer with the data
            serializer_temp = BalanceSheetTempSerializer(data=data)
            #serializer_live=BalanceSheetLiveSerializer(data=data)
            
            # Validate and save the serializer data
            if serializer_temp.is_valid() :
                temp_instance = serializer_temp.save()
                type=temp_instance.record_type
                # Call auditing and authorization functions if needed
                is_audit = model_audit(request,APP_NAME,'BalanceSheet',temp_instance.pk)
                is_authorization = self_authorization(request,APP_NAME,'BalanceSheet', temp_instance.pk,type)

                model_name='BalanceSheet'
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
    except  BalanceSheetTemp.DoesNotExist:
        return error('Instance does not exist')
    except ValidationError as e:
        return error(f"Validation Error: {e}")
    except Exception as e:
        return error(f"An error occurred: {e}")



def view_balancesheet(balancesheet_id=None):
    """
    Retrieves and serializes a BalanceSheet instance by its ID or all instances if ID is None.
    
    Args:
        BalanceSheet_id (int, optional): ID of the BalanceSheet to retrieve.

    Returns:
        dict: A success response with the serialized data if found,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if balancesheet_id is not None:
            record = BalanceSheetTemp.objects.get(pk=balancesheet_id)
            serializer = BalanceSheetTempSerializer(record)
        else:
            obj = BalanceSheetLive.objects.filter(is_deactivate=False)
            obj_pa = get_temp_record(request,APP_NAME,'BalanceSheet').filter(~Q(status='unauthorized_sent'))
            print('object--',obj_pa)
            obj_wait_auth = get_record_for_authorize(str(request.user.pk))
            # records = NoSeriesLinesALive.objects.all()
            live_data = BalanceSheetLiveSerializer(obj, many=True).data
            temp_data = BalanceSheetTempSerializer(obj_pa, many=True).data
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


def view_balancesheet_single(code):
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
        

        record = BalanceSheetLive.objects.get(pk=code)
        serializer = BalanceSheetLiveSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")


def pa_balancesheet(balancesheet_id,model_name):
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
        
        record = BalanceSheetTemp.objects.get(pk=balancesheet_id)
        serializer = BalanceSheetTempPASerializer(record).data
        
        type=record.record_type
        get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
        serializers=ModelRegistrationSerializer(get_table_name).data

        workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
        serializers_data=WorkflowMappingSerializer(workflow_mapping).data

        data={
            'balancesheet':serializer,
            'table_data':serializers,
            'workflow_data':serializers_data
        }
        return success(data)
    
    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def delete_balancesheet(balancesheet_id,model_name):
    """
    Deletes a BalanceSheet instance with the given ID.
    
    Args:
        balancesheet_id (int): ID of the BalanceSheet to delete.

    Returns:
        dict: A success response if deletion is successful,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        if  is_have_permission(request,APP_NAME, 'BalanceSheet', balancesheet_id):
            type='delete'

            is_authorization = self_authorization_for_delete(request,APP_NAME,model_name, balancesheet_id,type)
            user_ids_resp=get_next_user_from_work_flow(request,model_name,temp_instance=balancesheet_id,type=type)
 
            sent_auth=WorkflowMapping.objects.get(table_name__model_name__iexact=model_name,workflow_type=type)
            
            record = BalanceSheetLive.objects.get(pk=balancesheet_id)
            serializer = BalanceSheetLiveViewSerializer(record).data

            # get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
            # serializers=ModelRegistrationSerializer(get_table_name).data

            get_table_name = ModelRegistration.objects.get(model_name=model_name)
            serializers=ModelRegistrationSerializer(get_table_name).data

            print('table name of current',get_table_name)
            
            workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
            serializers_data=WorkflowMappingSerializer(workflow_mapping).data

            if user_ids_resp is not None and sent_auth.send_to_authorized == 'False' and sent_auth.same_user_authorized == 'False':

                obj = delete_record(request,APP_NAME, 'BalanceSheet', balancesheet_id)
                return success("Successfully deleted")
            else:
                data={
                    'BalanceSheet':serializer,
                    'table_data':serializers,
                    'workflow_data':serializers_data
                }
                return success(data)
        else:
            return error('you have no permission to delete the record')
    
    except BalanceSheetLive.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def view_balancesheet_tempdata(balancesheet_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = BalanceSheetTemp.objects.get(code=balancesheet_id)
        serializer = BalanceSheetTempSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")
    

def view_balancesheet_live(balancesheet_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = BalanceSheetLive.objects.get(code=balancesheet_id)
        serializer = BalanceSheetLiveViewSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def authorize_request_data_BalanceSheet(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=BalanceSheetTemp.objects.get(pk=pk)
        work_flow_type=get_instance.record_type
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,work_flow_type)
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()

        return success(req)
    
    except BalanceSheetTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def authorize_request_data_delete_BalanceSheet(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=BalanceSheetLive.objects.get(pk=pk)
  
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,type='delete')
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()
        return success(req)
    
    except BalanceSheetTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")





#add foreign key import model.


def create_incomestatement(revenue, operating_expenses, net_income, revenue_sources, expense_breakdown, reported_date):
    """
    Creates a IncomeStatement instance with the provided data.
        Args:
        revenue, operating_expenses, net_income, revenue_sources, expense_breakdown, reported_date: Keyword arguments for IncomeStatement fields.

    Returns:
        dict: Success or error message.
        APP_NAME = __name__.split('.')[0]

    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        data={'revenue': revenue,
			'operating_expenses': operating_expenses,
			'net_income': net_income,
			'revenue_sources': revenue_sources,
			'expense_breakdown': expense_breakdown,
			'reported_date': reported_date,}
        data['code'] = generate_random_id('ABC')
        data_create = data.copy()
        data_create['code'] = generate_random_id('ABC')
        data_create['record_type']='create'
        # Initialize the serializer with the data
        serializer_temp = IncomeStatementTempSerializer(data=data_create)
        serializer_live=IncomeStatementLiveSerializer(data=data)
        
        # Validate and save the serializer data
        if serializer_live.is_valid() and serializer_temp.is_valid() :
            temp_instance = serializer_temp.save()
            type=temp_instance.record_type
            # Call auditing and authorization functions if needed
            is_audit = model_audit(request,APP_NAME,'IncomeStatement',temp_instance.pk)
            is_authorization = self_authorization(request,APP_NAME,'IncomeStatement', temp_instance.pk,type)
            
            model_name='IncomeStatement'
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

def update_incomestatement_temp(code,revenue=None, operating_expenses=None, net_income=None, revenue_sources=None, expense_breakdown=None, reported_date=None):
    """
    Updates a IncomeStatement instance with the provided data.
    
    Args:
        incomestatement_id (int): ID of the IncomeStatement to update.
        revenue=None, operating_expenses=None, net_income=None, revenue_sources=None, expense_breakdown=None, reported_date=None: Keyword arguments for IncomeStatement fields to update.

    Returns:
        dict: Success or error message.
    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if  is_have_permission(request,APP_NAME, 'IncomeStatement',code):

            data={'revenue': revenue,
			'operating_expenses': operating_expenses,
			'net_income': net_income,
			'revenue_sources': revenue_sources,
			'expense_breakdown': expense_breakdown,
			'reported_date': reported_date,}
            data['code']=code

            data['record_type']='update'
            # Initialize the serializer with the data
            serializer_temp = IncomeStatementTempSerializer(data=data)
            #serializer_live=IncomeStatementLiveSerializer(data=data)
            
            # Validate and save the serializer data
            if serializer_temp.is_valid() :
                temp_instance = serializer_temp.save()
                type=temp_instance.record_type
                # Call auditing and authorization functions if needed
                is_audit = model_audit(request,APP_NAME,'IncomeStatement',temp_instance.pk)
                is_authorization = self_authorization(request,APP_NAME,'IncomeStatement', temp_instance.pk,type)

                model_name='IncomeStatement'
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
    except  IncomeStatementTemp.DoesNotExist:
        return error('Instance does not exist')
    except ValidationError as e:
        return error(f"Validation Error: {e}")
    except Exception as e:
        return error(f"An error occurred: {e}")



def view_incomestatement(incomestatement_id=None):
    """
    Retrieves and serializes a IncomeStatement instance by its ID or all instances if ID is None.
    
    Args:
        IncomeStatement_id (int, optional): ID of the IncomeStatement to retrieve.

    Returns:
        dict: A success response with the serialized data if found,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if incomestatement_id is not None:
            record = IncomeStatementTemp.objects.get(pk=incomestatement_id)
            serializer = IncomeStatementTempSerializer(record)
        else:
            obj = IncomeStatementLive.objects.filter(is_deactivate=False)
            obj_pa = get_temp_record(request,APP_NAME,'IncomeStatement').filter(~Q(status='unauthorized_sent'))
            print('object--',obj_pa)
            obj_wait_auth = get_record_for_authorize(str(request.user.pk))
            # records = NoSeriesLinesALive.objects.all()
            live_data = IncomeStatementLiveSerializer(obj, many=True).data
            temp_data = IncomeStatementTempSerializer(obj_pa, many=True).data
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


def view_incomestatement_single(code):
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
        

        record = IncomeStatementLive.objects.get(pk=code)
        serializer = IncomeStatementLiveSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")


def pa_incomestatement(incomestatement_id,model_name):
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
        
        record = IncomeStatementTemp.objects.get(pk=incomestatement_id)
        serializer = IncomeStatementTempPASerializer(record).data
        
        type=record.record_type
        get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
        serializers=ModelRegistrationSerializer(get_table_name).data

        workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
        serializers_data=WorkflowMappingSerializer(workflow_mapping).data

        data={
            'incomestatement':serializer,
            'table_data':serializers,
            'workflow_data':serializers_data
        }
        return success(data)
    
    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def delete_incomestatement(incomestatement_id,model_name):
    """
    Deletes a IncomeStatement instance with the given ID.
    
    Args:
        incomestatement_id (int): ID of the IncomeStatement to delete.

    Returns:
        dict: A success response if deletion is successful,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        if  is_have_permission(request,APP_NAME, 'IncomeStatement', incomestatement_id):
            type='delete'

            is_authorization = self_authorization_for_delete(request,APP_NAME,model_name, incomestatement_id,type)
            user_ids_resp=get_next_user_from_work_flow(request,model_name,temp_instance=incomestatement_id,type=type)
 
            sent_auth=WorkflowMapping.objects.get(table_name__model_name__iexact=model_name,workflow_type=type)
            
            record = IncomeStatementLive.objects.get(pk=incomestatement_id)
            serializer = IncomeStatementLiveViewSerializer(record).data

            # get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
            # serializers=ModelRegistrationSerializer(get_table_name).data

            get_table_name = ModelRegistration.objects.get(model_name=model_name)
            serializers=ModelRegistrationSerializer(get_table_name).data

            print('table name of current',get_table_name)
            
            workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
            serializers_data=WorkflowMappingSerializer(workflow_mapping).data

            if user_ids_resp is not None and sent_auth.send_to_authorized == 'False' and sent_auth.same_user_authorized == 'False':

                obj = delete_record(request,APP_NAME, 'IncomeStatement', incomestatement_id)
                return success("Successfully deleted")
            else:
                data={
                    'IncomeStatement':serializer,
                    'table_data':serializers,
                    'workflow_data':serializers_data
                }
                return success(data)
        else:
            return error('you have no permission to delete the record')
    
    except IncomeStatementLive.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def view_incomestatement_tempdata(incomestatement_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = IncomeStatementTemp.objects.get(code=incomestatement_id)
        serializer = IncomeStatementTempSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")
    

def view_incomestatement_live(incomestatement_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = IncomeStatementLive.objects.get(code=incomestatement_id)
        serializer = IncomeStatementLiveViewSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def authorize_request_data_IncomeStatement(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=IncomeStatementTemp.objects.get(pk=pk)
        work_flow_type=get_instance.record_type
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,work_flow_type)
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()

        return success(req)
    
    except IncomeStatementTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def authorize_request_data_delete_IncomeStatement(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=IncomeStatementLive.objects.get(pk=pk)
  
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,type='delete')
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()
        return success(req)
    
    except IncomeStatementTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")





#add foreign key import model.


def create_cashflowstatement(inflows, outflows, net_cash_flow, inflow_sources, outflow_categories, reported_date):
    """
    Creates a CashFlowStatement instance with the provided data.
        Args:
        inflows, outflows, net_cash_flow, inflow_sources, outflow_categories, reported_date: Keyword arguments for CashFlowStatement fields.

    Returns:
        dict: Success or error message.
        APP_NAME = __name__.split('.')[0]

    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        data={'inflows': inflows,
			'outflows': outflows,
			'net_cash_flow': net_cash_flow,
			'inflow_sources': inflow_sources,
			'outflow_categories': outflow_categories,
			'reported_date': reported_date,}
        data['code'] = generate_random_id('ABC')
        data_create = data.copy()
        data_create['code'] = generate_random_id('ABC')
        data_create['record_type']='create'
        # Initialize the serializer with the data
        serializer_temp = CashFlowStatementTempSerializer(data=data_create)
        serializer_live=CashFlowStatementLiveSerializer(data=data)
        
        # Validate and save the serializer data
        if serializer_live.is_valid() and serializer_temp.is_valid() :
            temp_instance = serializer_temp.save()
            type=temp_instance.record_type
            # Call auditing and authorization functions if needed
            is_audit = model_audit(request,APP_NAME,'CashFlowStatement',temp_instance.pk)
            is_authorization = self_authorization(request,APP_NAME,'CashFlowStatement', temp_instance.pk,type)
            
            model_name='CashFlowStatement'
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

def update_cashflowstatement_temp(code,inflows=None, outflows=None, net_cash_flow=None, inflow_sources=None, outflow_categories=None, reported_date=None):
    """
    Updates a CashFlowStatement instance with the provided data.
    
    Args:
        cashflowstatement_id (int): ID of the CashFlowStatement to update.
        inflows=None, outflows=None, net_cash_flow=None, inflow_sources=None, outflow_categories=None, reported_date=None: Keyword arguments for CashFlowStatement fields to update.

    Returns:
        dict: Success or error message.
    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if  is_have_permission(request,APP_NAME, 'CashFlowStatement',code):

            data={'inflows': inflows,
			'outflows': outflows,
			'net_cash_flow': net_cash_flow,
			'inflow_sources': inflow_sources,
			'outflow_categories': outflow_categories,
			'reported_date': reported_date,}
            data['code']=code

            data['record_type']='update'
            # Initialize the serializer with the data
            serializer_temp = CashFlowStatementTempSerializer(data=data)
            #serializer_live=CashFlowStatementLiveSerializer(data=data)
            
            # Validate and save the serializer data
            if serializer_temp.is_valid() :
                temp_instance = serializer_temp.save()
                type=temp_instance.record_type
                # Call auditing and authorization functions if needed
                is_audit = model_audit(request,APP_NAME,'CashFlowStatement',temp_instance.pk)
                is_authorization = self_authorization(request,APP_NAME,'CashFlowStatement', temp_instance.pk,type)

                model_name='CashFlowStatement'
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
    except  CashFlowStatementTemp.DoesNotExist:
        return error('Instance does not exist')
    except ValidationError as e:
        return error(f"Validation Error: {e}")
    except Exception as e:
        return error(f"An error occurred: {e}")



def view_cashflowstatement(cashflowstatement_id=None):
    """
    Retrieves and serializes a CashFlowStatement instance by its ID or all instances if ID is None.
    
    Args:
        CashFlowStatement_id (int, optional): ID of the CashFlowStatement to retrieve.

    Returns:
        dict: A success response with the serialized data if found,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if cashflowstatement_id is not None:
            record = CashFlowStatementTemp.objects.get(pk=cashflowstatement_id)
            serializer = CashFlowStatementTempSerializer(record)
        else:
            obj = CashFlowStatementLive.objects.filter(is_deactivate=False)
            obj_pa = get_temp_record(request,APP_NAME,'CashFlowStatement').filter(~Q(status='unauthorized_sent'))
            print('object--',obj_pa)
            obj_wait_auth = get_record_for_authorize(str(request.user.pk))
            # records = NoSeriesLinesALive.objects.all()
            live_data = CashFlowStatementLiveSerializer(obj, many=True).data
            temp_data = CashFlowStatementTempSerializer(obj_pa, many=True).data
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


def view_cashflowstatement_single(code):
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
        

        record = CashFlowStatementLive.objects.get(pk=code)
        serializer = CashFlowStatementLiveSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")


def pa_cashflowstatement(cashflowstatement_id,model_name):
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
        
        record = CashFlowStatementTemp.objects.get(pk=cashflowstatement_id)
        serializer = CashFlowStatementTempPASerializer(record).data
        
        type=record.record_type
        get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
        serializers=ModelRegistrationSerializer(get_table_name).data

        workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
        serializers_data=WorkflowMappingSerializer(workflow_mapping).data

        data={
            'cashflowstatement':serializer,
            'table_data':serializers,
            'workflow_data':serializers_data
        }
        return success(data)
    
    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def delete_cashflowstatement(cashflowstatement_id,model_name):
    """
    Deletes a CashFlowStatement instance with the given ID.
    
    Args:
        cashflowstatement_id (int): ID of the CashFlowStatement to delete.

    Returns:
        dict: A success response if deletion is successful,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        if  is_have_permission(request,APP_NAME, 'CashFlowStatement', cashflowstatement_id):
            type='delete'

            is_authorization = self_authorization_for_delete(request,APP_NAME,model_name, cashflowstatement_id,type)
            user_ids_resp=get_next_user_from_work_flow(request,model_name,temp_instance=cashflowstatement_id,type=type)
 
            sent_auth=WorkflowMapping.objects.get(table_name__model_name__iexact=model_name,workflow_type=type)
            
            record = CashFlowStatementLive.objects.get(pk=cashflowstatement_id)
            serializer = CashFlowStatementLiveViewSerializer(record).data

            # get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
            # serializers=ModelRegistrationSerializer(get_table_name).data

            get_table_name = ModelRegistration.objects.get(model_name=model_name)
            serializers=ModelRegistrationSerializer(get_table_name).data

            print('table name of current',get_table_name)
            
            workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
            serializers_data=WorkflowMappingSerializer(workflow_mapping).data

            if user_ids_resp is not None and sent_auth.send_to_authorized == 'False' and sent_auth.same_user_authorized == 'False':

                obj = delete_record(request,APP_NAME, 'CashFlowStatement', cashflowstatement_id)
                return success("Successfully deleted")
            else:
                data={
                    'CashFlowStatement':serializer,
                    'table_data':serializers,
                    'workflow_data':serializers_data
                }
                return success(data)
        else:
            return error('you have no permission to delete the record')
    
    except CashFlowStatementLive.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def view_cashflowstatement_tempdata(cashflowstatement_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = CashFlowStatementTemp.objects.get(code=cashflowstatement_id)
        serializer = CashFlowStatementTempSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")
    

def view_cashflowstatement_live(cashflowstatement_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = CashFlowStatementLive.objects.get(code=cashflowstatement_id)
        serializer = CashFlowStatementLiveViewSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def authorize_request_data_CashFlowStatement(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=CashFlowStatementTemp.objects.get(pk=pk)
        work_flow_type=get_instance.record_type
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,work_flow_type)
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()

        return success(req)
    
    except CashFlowStatementTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def authorize_request_data_delete_CashFlowStatement(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=CashFlowStatementLive.objects.get(pk=pk)
  
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,type='delete')
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()
        return success(req)
    
    except CashFlowStatementTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")





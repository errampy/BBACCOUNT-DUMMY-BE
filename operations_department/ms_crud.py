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


def create_loandisbursement(total_loans_disbursed, number_of_loans, average_loan_size, highest_loan_disbursed, lowest_loan_disbursed, loan_purpose_distribution, disbursement_channels, reported_date):
    """
    Creates a LoanDisbursement instance with the provided data.
        Args:
        total_loans_disbursed, number_of_loans, average_loan_size, highest_loan_disbursed, lowest_loan_disbursed, loan_purpose_distribution, disbursement_channels, reported_date: Keyword arguments for LoanDisbursement fields.

    Returns:
        dict: Success or error message.
        APP_NAME = __name__.split('.')[0]

    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        data={'total_loans_disbursed': total_loans_disbursed,
			'number_of_loans': number_of_loans,
			'average_loan_size': average_loan_size,
			'highest_loan_disbursed': highest_loan_disbursed,
			'lowest_loan_disbursed': lowest_loan_disbursed,
			'loan_purpose_distribution': loan_purpose_distribution,
			'disbursement_channels': disbursement_channels,
			'reported_date': reported_date,}
        data['code'] = generate_random_id('ABC')
        data_create = data.copy()
        data_create['code'] = generate_random_id('ABC')
        data_create['record_type']='create'
        # Initialize the serializer with the data
        serializer_temp = LoanDisbursementTempSerializer(data=data_create)
        serializer_live=LoanDisbursementLiveSerializer(data=data)
        
        # Validate and save the serializer data
        if serializer_live.is_valid() and serializer_temp.is_valid() :
            temp_instance = serializer_temp.save()
            type=temp_instance.record_type
            # Call auditing and authorization functions if needed
            is_audit = model_audit(request,APP_NAME,'LoanDisbursement',temp_instance.pk)
            is_authorization = self_authorization(request,APP_NAME,'LoanDisbursement', temp_instance.pk,type)
            
            model_name='LoanDisbursement'
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

def update_loandisbursement_temp(code,total_loans_disbursed=None, number_of_loans=None, average_loan_size=None, highest_loan_disbursed=None, lowest_loan_disbursed=None, loan_purpose_distribution=None, disbursement_channels=None, reported_date=None):
    """
    Updates a LoanDisbursement instance with the provided data.
    
    Args:
        loandisbursement_id (int): ID of the LoanDisbursement to update.
        total_loans_disbursed=None, number_of_loans=None, average_loan_size=None, highest_loan_disbursed=None, lowest_loan_disbursed=None, loan_purpose_distribution=None, disbursement_channels=None, reported_date=None: Keyword arguments for LoanDisbursement fields to update.

    Returns:
        dict: Success or error message.
    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if  is_have_permission(request,APP_NAME, 'LoanDisbursement',code):

            data={'total_loans_disbursed': total_loans_disbursed,
			'number_of_loans': number_of_loans,
			'average_loan_size': average_loan_size,
			'highest_loan_disbursed': highest_loan_disbursed,
			'lowest_loan_disbursed': lowest_loan_disbursed,
			'loan_purpose_distribution': loan_purpose_distribution,
			'disbursement_channels': disbursement_channels,
			'reported_date': reported_date,}
            data['code']=code

            data['record_type']='update'
            # Initialize the serializer with the data
            serializer_temp = LoanDisbursementTempSerializer(data=data)
            #serializer_live=LoanDisbursementLiveSerializer(data=data)
            
            # Validate and save the serializer data
            if serializer_temp.is_valid() :
                temp_instance = serializer_temp.save()
                type=temp_instance.record_type
                # Call auditing and authorization functions if needed
                is_audit = model_audit(request,APP_NAME,'LoanDisbursement',temp_instance.pk)
                is_authorization = self_authorization(request,APP_NAME,'LoanDisbursement', temp_instance.pk,type)

                model_name='LoanDisbursement'
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
    except  LoanDisbursementTemp.DoesNotExist:
        return error('Instance does not exist')
    except ValidationError as e:
        return error(f"Validation Error: {e}")
    except Exception as e:
        return error(f"An error occurred: {e}")



def view_loandisbursement(loandisbursement_id=None):
    """
    Retrieves and serializes a LoanDisbursement instance by its ID or all instances if ID is None.
    
    Args:
        LoanDisbursement_id (int, optional): ID of the LoanDisbursement to retrieve.

    Returns:
        dict: A success response with the serialized data if found,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if loandisbursement_id is not None:
            record = LoanDisbursementTemp.objects.get(pk=loandisbursement_id)
            serializer = LoanDisbursementTempSerializer(record)
        else:
            obj = LoanDisbursementLive.objects.filter(is_deactivate=False)
            obj_pa = get_temp_record(request,APP_NAME,'LoanDisbursement').filter(~Q(status='unauthorized_sent'))
            print('object--',obj_pa)
            obj_wait_auth = get_record_for_authorize(str(request.user.pk))
            # records = NoSeriesLinesALive.objects.all()
            live_data = LoanDisbursementLiveSerializer(obj, many=True).data
            temp_data = LoanDisbursementTempSerializer(obj_pa, many=True).data
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


def view_loandisbursement_single(code):
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
        

        record = LoanDisbursementLive.objects.get(pk=code)
        serializer = LoanDisbursementLiveSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")


def pa_loandisbursement(loandisbursement_id,model_name):
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
        
        record = LoanDisbursementTemp.objects.get(pk=loandisbursement_id)
        serializer = LoanDisbursementTempPASerializer(record).data
        
        type=record.record_type
        get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
        serializers=ModelRegistrationSerializer(get_table_name).data

        workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
        serializers_data=WorkflowMappingSerializer(workflow_mapping).data

        data={
            'loandisbursement':serializer,
            'table_data':serializers,
            'workflow_data':serializers_data
        }
        return success(data)
    
    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def delete_loandisbursement(loandisbursement_id,model_name):
    """
    Deletes a LoanDisbursement instance with the given ID.
    
    Args:
        loandisbursement_id (int): ID of the LoanDisbursement to delete.

    Returns:
        dict: A success response if deletion is successful,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        if  is_have_permission(request,APP_NAME, 'LoanDisbursement', loandisbursement_id):
            type='delete'

            is_authorization = self_authorization_for_delete(request,APP_NAME,model_name, loandisbursement_id,type)
            user_ids_resp=get_next_user_from_work_flow(request,model_name,temp_instance=loandisbursement_id,type=type)
 
            sent_auth=WorkflowMapping.objects.get(table_name__model_name__iexact=model_name,workflow_type=type)
            
            record = LoanDisbursementLive.objects.get(pk=loandisbursement_id)
            serializer = LoanDisbursementLiveViewSerializer(record).data

            # get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
            # serializers=ModelRegistrationSerializer(get_table_name).data

            get_table_name = ModelRegistration.objects.get(model_name=model_name)
            serializers=ModelRegistrationSerializer(get_table_name).data

            print('table name of current',get_table_name)
            
            workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
            serializers_data=WorkflowMappingSerializer(workflow_mapping).data

            if user_ids_resp is not None and sent_auth.send_to_authorized == 'False' and sent_auth.same_user_authorized == 'False':

                obj = delete_record(request,APP_NAME, 'LoanDisbursement', loandisbursement_id)
                return success("Successfully deleted")
            else:
                data={
                    'LoanDisbursement':serializer,
                    'table_data':serializers,
                    'workflow_data':serializers_data
                }
                return success(data)
        else:
            return error('you have no permission to delete the record')
    
    except LoanDisbursementLive.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def view_loandisbursement_tempdata(loandisbursement_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = LoanDisbursementTemp.objects.get(code=loandisbursement_id)
        serializer = LoanDisbursementTempSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")
    

def view_loandisbursement_live(loandisbursement_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = LoanDisbursementLive.objects.get(code=loandisbursement_id)
        serializer = LoanDisbursementLiveViewSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def authorize_request_data_LoanDisbursement(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=LoanDisbursementTemp.objects.get(pk=pk)
        work_flow_type=get_instance.record_type
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,work_flow_type)
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()

        return success(req)
    
    except LoanDisbursementTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def authorize_request_data_delete_LoanDisbursement(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=LoanDisbursementLive.objects.get(pk=pk)
  
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,type='delete')
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()
        return success(req)
    
    except LoanDisbursementTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")





#add foreign key import model.


def create_portfolioquality(portfolio_at_risk, total_outstanding_portfolio, amount_overdue, loans_at_risk_count, risk_categorization, recovery_rate, average_loan_age, reported_date):
    """
    Creates a PortfolioQuality instance with the provided data.
        Args:
        portfolio_at_risk, total_outstanding_portfolio, amount_overdue, loans_at_risk_count, risk_categorization, recovery_rate, average_loan_age, reported_date: Keyword arguments for PortfolioQuality fields.

    Returns:
        dict: Success or error message.
        APP_NAME = __name__.split('.')[0]

    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        data={'portfolio_at_risk': portfolio_at_risk,
			'total_outstanding_portfolio': total_outstanding_portfolio,
			'amount_overdue': amount_overdue,
			'loans_at_risk_count': loans_at_risk_count,
			'risk_categorization': risk_categorization,
			'recovery_rate': recovery_rate,
			'average_loan_age': average_loan_age,
			'reported_date': reported_date,}
        data['code'] = generate_random_id('ABC')
        data_create = data.copy()
        data_create['code'] = generate_random_id('ABC')
        data_create['record_type']='create'
        # Initialize the serializer with the data
        serializer_temp = PortfolioQualityTempSerializer(data=data_create)
        serializer_live=PortfolioQualityLiveSerializer(data=data)
        
        # Validate and save the serializer data
        if serializer_live.is_valid() and serializer_temp.is_valid() :
            temp_instance = serializer_temp.save()
            type=temp_instance.record_type
            # Call auditing and authorization functions if needed
            is_audit = model_audit(request,APP_NAME,'PortfolioQuality',temp_instance.pk)
            is_authorization = self_authorization(request,APP_NAME,'PortfolioQuality', temp_instance.pk,type)
            
            model_name='PortfolioQuality'
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

def update_portfolioquality_temp(code,portfolio_at_risk=None, total_outstanding_portfolio=None, amount_overdue=None, loans_at_risk_count=None, risk_categorization=None, recovery_rate=None, average_loan_age=None, reported_date=None):
    """
    Updates a PortfolioQuality instance with the provided data.
    
    Args:
        portfolioquality_id (int): ID of the PortfolioQuality to update.
        portfolio_at_risk=None, total_outstanding_portfolio=None, amount_overdue=None, loans_at_risk_count=None, risk_categorization=None, recovery_rate=None, average_loan_age=None, reported_date=None: Keyword arguments for PortfolioQuality fields to update.

    Returns:
        dict: Success or error message.
    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if  is_have_permission(request,APP_NAME, 'PortfolioQuality',code):

            data={'portfolio_at_risk': portfolio_at_risk,
			'total_outstanding_portfolio': total_outstanding_portfolio,
			'amount_overdue': amount_overdue,
			'loans_at_risk_count': loans_at_risk_count,
			'risk_categorization': risk_categorization,
			'recovery_rate': recovery_rate,
			'average_loan_age': average_loan_age,
			'reported_date': reported_date,}
            data['code']=code

            data['record_type']='update'
            # Initialize the serializer with the data
            serializer_temp = PortfolioQualityTempSerializer(data=data)
            #serializer_live=PortfolioQualityLiveSerializer(data=data)
            
            # Validate and save the serializer data
            if serializer_temp.is_valid() :
                temp_instance = serializer_temp.save()
                type=temp_instance.record_type
                # Call auditing and authorization functions if needed
                is_audit = model_audit(request,APP_NAME,'PortfolioQuality',temp_instance.pk)
                is_authorization = self_authorization(request,APP_NAME,'PortfolioQuality', temp_instance.pk,type)

                model_name='PortfolioQuality'
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
    except  PortfolioQualityTemp.DoesNotExist:
        return error('Instance does not exist')
    except ValidationError as e:
        return error(f"Validation Error: {e}")
    except Exception as e:
        return error(f"An error occurred: {e}")



def view_portfolioquality(portfolioquality_id=None):
    """
    Retrieves and serializes a PortfolioQuality instance by its ID or all instances if ID is None.
    
    Args:
        PortfolioQuality_id (int, optional): ID of the PortfolioQuality to retrieve.

    Returns:
        dict: A success response with the serialized data if found,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if portfolioquality_id is not None:
            record = PortfolioQualityTemp.objects.get(pk=portfolioquality_id)
            serializer = PortfolioQualityTempSerializer(record)
        else:
            obj = PortfolioQualityLive.objects.filter(is_deactivate=False)
            obj_pa = get_temp_record(request,APP_NAME,'PortfolioQuality').filter(~Q(status='unauthorized_sent'))
            print('object--',obj_pa)
            obj_wait_auth = get_record_for_authorize(str(request.user.pk))
            # records = NoSeriesLinesALive.objects.all()
            live_data = PortfolioQualityLiveSerializer(obj, many=True).data
            temp_data = PortfolioQualityTempSerializer(obj_pa, many=True).data
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


def view_portfolioquality_single(code):
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
        

        record = PortfolioQualityLive.objects.get(pk=code)
        serializer = PortfolioQualityLiveSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")


def pa_portfolioquality(portfolioquality_id,model_name):
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
        
        record = PortfolioQualityTemp.objects.get(pk=portfolioquality_id)
        serializer = PortfolioQualityTempPASerializer(record).data
        
        type=record.record_type
        get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
        serializers=ModelRegistrationSerializer(get_table_name).data

        workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
        serializers_data=WorkflowMappingSerializer(workflow_mapping).data

        data={
            'portfolioquality':serializer,
            'table_data':serializers,
            'workflow_data':serializers_data
        }
        return success(data)
    
    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def delete_portfolioquality(portfolioquality_id,model_name):
    """
    Deletes a PortfolioQuality instance with the given ID.
    
    Args:
        portfolioquality_id (int): ID of the PortfolioQuality to delete.

    Returns:
        dict: A success response if deletion is successful,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        if  is_have_permission(request,APP_NAME, 'PortfolioQuality', portfolioquality_id):
            type='delete'

            is_authorization = self_authorization_for_delete(request,APP_NAME,model_name, portfolioquality_id,type)
            user_ids_resp=get_next_user_from_work_flow(request,model_name,temp_instance=portfolioquality_id,type=type)
 
            sent_auth=WorkflowMapping.objects.get(table_name__model_name__iexact=model_name,workflow_type=type)
            
            record = PortfolioQualityLive.objects.get(pk=portfolioquality_id)
            serializer = PortfolioQualityLiveViewSerializer(record).data

            # get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
            # serializers=ModelRegistrationSerializer(get_table_name).data

            get_table_name = ModelRegistration.objects.get(model_name=model_name)
            serializers=ModelRegistrationSerializer(get_table_name).data

            print('table name of current',get_table_name)
            
            workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
            serializers_data=WorkflowMappingSerializer(workflow_mapping).data

            if user_ids_resp is not None and sent_auth.send_to_authorized == 'False' and sent_auth.same_user_authorized == 'False':

                obj = delete_record(request,APP_NAME, 'PortfolioQuality', portfolioquality_id)
                return success("Successfully deleted")
            else:
                data={
                    'PortfolioQuality':serializer,
                    'table_data':serializers,
                    'workflow_data':serializers_data
                }
                return success(data)
        else:
            return error('you have no permission to delete the record')
    
    except PortfolioQualityLive.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def view_portfolioquality_tempdata(portfolioquality_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = PortfolioQualityTemp.objects.get(code=portfolioquality_id)
        serializer = PortfolioQualityTempSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")
    

def view_portfolioquality_live(portfolioquality_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = PortfolioQualityLive.objects.get(code=portfolioquality_id)
        serializer = PortfolioQualityLiveViewSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def authorize_request_data_PortfolioQuality(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=PortfolioQualityTemp.objects.get(pk=pk)
        work_flow_type=get_instance.record_type
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,work_flow_type)
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()

        return success(req)
    
    except PortfolioQualityTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def authorize_request_data_delete_PortfolioQuality(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=PortfolioQualityLive.objects.get(pk=pk)
  
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,type='delete')
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()
        return success(req)
    
    except PortfolioQualityTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")





#add foreign key import model.


def create_clientoutreach(active_clients, new_clients_this_quarter, client_retention_rate, average_client_loan_size, inactive_clients, reported_date, outreach_campaigns, client_feedback_summary):
    """
    Creates a ClientOutreach instance with the provided data.
        Args:
        active_clients, new_clients_this_quarter, client_retention_rate, average_client_loan_size, inactive_clients, reported_date, outreach_campaigns, client_feedback_summary: Keyword arguments for ClientOutreach fields.

    Returns:
        dict: Success or error message.
        APP_NAME = __name__.split('.')[0]

    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        data={'active_clients': active_clients,
			'new_clients_this_quarter': new_clients_this_quarter,
			'client_retention_rate': client_retention_rate,
			'average_client_loan_size': average_client_loan_size,
			'inactive_clients': inactive_clients,
			'reported_date': reported_date,
			'outreach_campaigns': outreach_campaigns,
			'client_feedback_summary': client_feedback_summary,}
        data['code'] = generate_random_id('ABC')
        data_create = data.copy()
        data_create['code'] = generate_random_id('ABC')
        data_create['record_type']='create'
        # Initialize the serializer with the data
        serializer_temp = ClientOutreachTempSerializer(data=data_create)
        serializer_live=ClientOutreachLiveSerializer(data=data)
        
        # Validate and save the serializer data
        if serializer_live.is_valid() and serializer_temp.is_valid() :
            temp_instance = serializer_temp.save()
            type=temp_instance.record_type
            # Call auditing and authorization functions if needed
            is_audit = model_audit(request,APP_NAME,'ClientOutreach',temp_instance.pk)
            is_authorization = self_authorization(request,APP_NAME,'ClientOutreach', temp_instance.pk,type)
            
            model_name='ClientOutreach'
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

def update_clientoutreach_temp(code,active_clients=None, new_clients_this_quarter=None, client_retention_rate=None, average_client_loan_size=None, inactive_clients=None, reported_date=None, outreach_campaigns=None, client_feedback_summary=None):
    """
    Updates a ClientOutreach instance with the provided data.
    
    Args:
        clientoutreach_id (int): ID of the ClientOutreach to update.
        active_clients=None, new_clients_this_quarter=None, client_retention_rate=None, average_client_loan_size=None, inactive_clients=None, reported_date=None, outreach_campaigns=None, client_feedback_summary=None: Keyword arguments for ClientOutreach fields to update.

    Returns:
        dict: Success or error message.
    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if  is_have_permission(request,APP_NAME, 'ClientOutreach',code):

            data={'active_clients': active_clients,
			'new_clients_this_quarter': new_clients_this_quarter,
			'client_retention_rate': client_retention_rate,
			'average_client_loan_size': average_client_loan_size,
			'inactive_clients': inactive_clients,
			'reported_date': reported_date,
			'outreach_campaigns': outreach_campaigns,
			'client_feedback_summary': client_feedback_summary,}
            data['code']=code

            data['record_type']='update'
            # Initialize the serializer with the data
            serializer_temp = ClientOutreachTempSerializer(data=data)
            #serializer_live=ClientOutreachLiveSerializer(data=data)
            
            # Validate and save the serializer data
            if serializer_temp.is_valid() :
                temp_instance = serializer_temp.save()
                type=temp_instance.record_type
                # Call auditing and authorization functions if needed
                is_audit = model_audit(request,APP_NAME,'ClientOutreach',temp_instance.pk)
                is_authorization = self_authorization(request,APP_NAME,'ClientOutreach', temp_instance.pk,type)

                model_name='ClientOutreach'
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
    except  ClientOutreachTemp.DoesNotExist:
        return error('Instance does not exist')
    except ValidationError as e:
        return error(f"Validation Error: {e}")
    except Exception as e:
        return error(f"An error occurred: {e}")



def view_clientoutreach(clientoutreach_id=None):
    """
    Retrieves and serializes a ClientOutreach instance by its ID or all instances if ID is None.
    
    Args:
        ClientOutreach_id (int, optional): ID of the ClientOutreach to retrieve.

    Returns:
        dict: A success response with the serialized data if found,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if clientoutreach_id is not None:
            record = ClientOutreachTemp.objects.get(pk=clientoutreach_id)
            serializer = ClientOutreachTempSerializer(record)
        else:
            obj = ClientOutreachLive.objects.filter(is_deactivate=False)
            obj_pa = get_temp_record(request,APP_NAME,'ClientOutreach').filter(~Q(status='unauthorized_sent'))
            print('object--',obj_pa)
            obj_wait_auth = get_record_for_authorize(str(request.user.pk))
            # records = NoSeriesLinesALive.objects.all()
            live_data = ClientOutreachLiveSerializer(obj, many=True).data
            temp_data = ClientOutreachTempSerializer(obj_pa, many=True).data
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


def view_clientoutreach_single(code):
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
        

        record = ClientOutreachLive.objects.get(pk=code)
        serializer = ClientOutreachLiveSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")


def pa_clientoutreach(clientoutreach_id,model_name):
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
        
        record = ClientOutreachTemp.objects.get(pk=clientoutreach_id)
        serializer = ClientOutreachTempPASerializer(record).data
        
        type=record.record_type
        get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
        serializers=ModelRegistrationSerializer(get_table_name).data

        workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
        serializers_data=WorkflowMappingSerializer(workflow_mapping).data

        data={
            'clientoutreach':serializer,
            'table_data':serializers,
            'workflow_data':serializers_data
        }
        return success(data)
    
    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def delete_clientoutreach(clientoutreach_id,model_name):
    """
    Deletes a ClientOutreach instance with the given ID.
    
    Args:
        clientoutreach_id (int): ID of the ClientOutreach to delete.

    Returns:
        dict: A success response if deletion is successful,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        if  is_have_permission(request,APP_NAME, 'ClientOutreach', clientoutreach_id):
            type='delete'

            is_authorization = self_authorization_for_delete(request,APP_NAME,model_name, clientoutreach_id,type)
            user_ids_resp=get_next_user_from_work_flow(request,model_name,temp_instance=clientoutreach_id,type=type)
 
            sent_auth=WorkflowMapping.objects.get(table_name__model_name__iexact=model_name,workflow_type=type)
            
            record = ClientOutreachLive.objects.get(pk=clientoutreach_id)
            serializer = ClientOutreachLiveViewSerializer(record).data

            # get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
            # serializers=ModelRegistrationSerializer(get_table_name).data

            get_table_name = ModelRegistration.objects.get(model_name=model_name)
            serializers=ModelRegistrationSerializer(get_table_name).data

            print('table name of current',get_table_name)
            
            workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
            serializers_data=WorkflowMappingSerializer(workflow_mapping).data

            if user_ids_resp is not None and sent_auth.send_to_authorized == 'False' and sent_auth.same_user_authorized == 'False':

                obj = delete_record(request,APP_NAME, 'ClientOutreach', clientoutreach_id)
                return success("Successfully deleted")
            else:
                data={
                    'ClientOutreach':serializer,
                    'table_data':serializers,
                    'workflow_data':serializers_data
                }
                return success(data)
        else:
            return error('you have no permission to delete the record')
    
    except ClientOutreachLive.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def view_clientoutreach_tempdata(clientoutreach_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = ClientOutreachTemp.objects.get(code=clientoutreach_id)
        serializer = ClientOutreachTempSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")
    

def view_clientoutreach_live(clientoutreach_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = ClientOutreachLive.objects.get(code=clientoutreach_id)
        serializer = ClientOutreachLiveViewSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def authorize_request_data_ClientOutreach(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=ClientOutreachTemp.objects.get(pk=pk)
        work_flow_type=get_instance.record_type
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,work_flow_type)
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()

        return success(req)
    
    except ClientOutreachTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def authorize_request_data_delete_ClientOutreach(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=ClientOutreachLive.objects.get(pk=pk)
  
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,type='delete')
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()
        return success(req)
    
    except ClientOutreachTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")





#add foreign key import model.


def create_branchperformance(branch_name, loan_portfolio, repayment_rate, total_clients, new_clients_this_month, reported_date, branch_location, branch_manager):
    """
    Creates a BranchPerformance instance with the provided data.
        Args:
        branch_name, loan_portfolio, repayment_rate, total_clients, new_clients_this_month, reported_date, branch_location, branch_manager: Keyword arguments for BranchPerformance fields.

    Returns:
        dict: Success or error message.
        APP_NAME = __name__.split('.')[0]

    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        data={'branch_name': branch_name,
			'loan_portfolio': loan_portfolio,
			'repayment_rate': repayment_rate,
			'total_clients': total_clients,
			'new_clients_this_month': new_clients_this_month,
			'reported_date': reported_date,
			'branch_location': branch_location,
			'branch_manager': branch_manager,}
        data['code'] = generate_random_id('ABC')
        data_create = data.copy()
        data_create['code'] = generate_random_id('ABC')
        data_create['record_type']='create'
        # Initialize the serializer with the data
        serializer_temp = BranchPerformanceTempSerializer(data=data_create)
        serializer_live=BranchPerformanceLiveSerializer(data=data)
        
        # Validate and save the serializer data
        if serializer_live.is_valid() and serializer_temp.is_valid() :
            temp_instance = serializer_temp.save()
            type=temp_instance.record_type
            # Call auditing and authorization functions if needed
            is_audit = model_audit(request,APP_NAME,'BranchPerformance',temp_instance.pk)
            is_authorization = self_authorization(request,APP_NAME,'BranchPerformance', temp_instance.pk,type)
            
            model_name='BranchPerformance'
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

def update_branchperformance_temp(code,branch_name=None, loan_portfolio=None, repayment_rate=None, total_clients=None, new_clients_this_month=None, reported_date=None, branch_location=None, branch_manager=None):
    """
    Updates a BranchPerformance instance with the provided data.
    
    Args:
        branchperformance_id (int): ID of the BranchPerformance to update.
        branch_name=None, loan_portfolio=None, repayment_rate=None, total_clients=None, new_clients_this_month=None, reported_date=None, branch_location=None, branch_manager=None: Keyword arguments for BranchPerformance fields to update.

    Returns:
        dict: Success or error message.
    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if  is_have_permission(request,APP_NAME, 'BranchPerformance',code):

            data={'branch_name': branch_name,
			'loan_portfolio': loan_portfolio,
			'repayment_rate': repayment_rate,
			'total_clients': total_clients,
			'new_clients_this_month': new_clients_this_month,
			'reported_date': reported_date,
			'branch_location': branch_location,
			'branch_manager': branch_manager,}
            data['code']=code

            data['record_type']='update'
            # Initialize the serializer with the data
            serializer_temp = BranchPerformanceTempSerializer(data=data)
            #serializer_live=BranchPerformanceLiveSerializer(data=data)
            
            # Validate and save the serializer data
            if serializer_temp.is_valid() :
                temp_instance = serializer_temp.save()
                type=temp_instance.record_type
                # Call auditing and authorization functions if needed
                is_audit = model_audit(request,APP_NAME,'BranchPerformance',temp_instance.pk)
                is_authorization = self_authorization(request,APP_NAME,'BranchPerformance', temp_instance.pk,type)

                model_name='BranchPerformance'
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
    except  BranchPerformanceTemp.DoesNotExist:
        return error('Instance does not exist')
    except ValidationError as e:
        return error(f"Validation Error: {e}")
    except Exception as e:
        return error(f"An error occurred: {e}")



def view_branchperformance(branchperformance_id=None):
    """
    Retrieves and serializes a BranchPerformance instance by its ID or all instances if ID is None.
    
    Args:
        BranchPerformance_id (int, optional): ID of the BranchPerformance to retrieve.

    Returns:
        dict: A success response with the serialized data if found,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if branchperformance_id is not None:
            record = BranchPerformanceTemp.objects.get(pk=branchperformance_id)
            serializer = BranchPerformanceTempSerializer(record)
        else:
            obj = BranchPerformanceLive.objects.filter(is_deactivate=False)
            obj_pa = get_temp_record(request,APP_NAME,'BranchPerformance').filter(~Q(status='unauthorized_sent'))
            print('object--',obj_pa)
            obj_wait_auth = get_record_for_authorize(str(request.user.pk))
            # records = NoSeriesLinesALive.objects.all()
            live_data = BranchPerformanceLiveSerializer(obj, many=True).data
            temp_data = BranchPerformanceTempSerializer(obj_pa, many=True).data
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


def view_branchperformance_single(code):
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
        

        record = BranchPerformanceLive.objects.get(pk=code)
        serializer = BranchPerformanceLiveSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")


def pa_branchperformance(branchperformance_id,model_name):
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
        
        record = BranchPerformanceTemp.objects.get(pk=branchperformance_id)
        serializer = BranchPerformanceTempPASerializer(record).data
        
        type=record.record_type
        get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
        serializers=ModelRegistrationSerializer(get_table_name).data

        workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
        serializers_data=WorkflowMappingSerializer(workflow_mapping).data

        data={
            'branchperformance':serializer,
            'table_data':serializers,
            'workflow_data':serializers_data
        }
        return success(data)
    
    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def delete_branchperformance(branchperformance_id,model_name):
    """
    Deletes a BranchPerformance instance with the given ID.
    
    Args:
        branchperformance_id (int): ID of the BranchPerformance to delete.

    Returns:
        dict: A success response if deletion is successful,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        if  is_have_permission(request,APP_NAME, 'BranchPerformance', branchperformance_id):
            type='delete'

            is_authorization = self_authorization_for_delete(request,APP_NAME,model_name, branchperformance_id,type)
            user_ids_resp=get_next_user_from_work_flow(request,model_name,temp_instance=branchperformance_id,type=type)
 
            sent_auth=WorkflowMapping.objects.get(table_name__model_name__iexact=model_name,workflow_type=type)
            
            record = BranchPerformanceLive.objects.get(pk=branchperformance_id)
            serializer = BranchPerformanceLiveViewSerializer(record).data

            # get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
            # serializers=ModelRegistrationSerializer(get_table_name).data

            get_table_name = ModelRegistration.objects.get(model_name=model_name)
            serializers=ModelRegistrationSerializer(get_table_name).data

            print('table name of current',get_table_name)
            
            workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
            serializers_data=WorkflowMappingSerializer(workflow_mapping).data

            if user_ids_resp is not None and sent_auth.send_to_authorized == 'False' and sent_auth.same_user_authorized == 'False':

                obj = delete_record(request,APP_NAME, 'BranchPerformance', branchperformance_id)
                return success("Successfully deleted")
            else:
                data={
                    'BranchPerformance':serializer,
                    'table_data':serializers,
                    'workflow_data':serializers_data
                }
                return success(data)
        else:
            return error('you have no permission to delete the record')
    
    except BranchPerformanceLive.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def view_branchperformance_tempdata(branchperformance_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = BranchPerformanceTemp.objects.get(code=branchperformance_id)
        serializer = BranchPerformanceTempSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")
    

def view_branchperformance_live(branchperformance_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = BranchPerformanceLive.objects.get(code=branchperformance_id)
        serializer = BranchPerformanceLiveViewSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def authorize_request_data_BranchPerformance(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=BranchPerformanceTemp.objects.get(pk=pk)
        work_flow_type=get_instance.record_type
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,work_flow_type)
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()

        return success(req)
    
    except BranchPerformanceTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def authorize_request_data_delete_BranchPerformance(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=BranchPerformanceLive.objects.get(pk=pk)
  
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,type='delete')
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()
        return success(req)
    
    except BranchPerformanceTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")





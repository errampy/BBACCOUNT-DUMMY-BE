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


def create_officeexpense(total_office_expenses, top_expenses, utilities_expenses, rent_expenses, office_supplies_expenses, reported_date, employee_welfare_expenses, maintenance_expenses, comments):
    """
    Creates a OfficeExpense instance with the provided data.
        Args:
        total_office_expenses, top_expenses, utilities_expenses, rent_expenses, office_supplies_expenses, reported_date, employee_welfare_expenses, maintenance_expenses, comments: Keyword arguments for OfficeExpense fields.

    Returns:
        dict: Success or error message.
        APP_NAME = __name__.split('.')[0]

    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        data={'total_office_expenses': total_office_expenses,
			'top_expenses': top_expenses,
			'utilities_expenses': utilities_expenses,
			'rent_expenses': rent_expenses,
			'office_supplies_expenses': office_supplies_expenses,
			'reported_date': reported_date,
			'employee_welfare_expenses': employee_welfare_expenses,
			'maintenance_expenses': maintenance_expenses,
			'comments': comments,}
        data['code'] = generate_random_id('ABC')
        data_create = data.copy()
        data_create['code'] = generate_random_id('ABC')
        data_create['record_type']='create'
        # Initialize the serializer with the data
        serializer_temp = OfficeExpenseTempSerializer(data=data_create)
        serializer_live=OfficeExpenseLiveSerializer(data=data)
        
        # Validate and save the serializer data
        if serializer_live.is_valid() and serializer_temp.is_valid() :
            temp_instance = serializer_temp.save()
            type=temp_instance.record_type
            # Call auditing and authorization functions if needed
            is_audit = model_audit(request,APP_NAME,'OfficeExpense',temp_instance.pk)
            is_authorization = self_authorization(request,APP_NAME,'OfficeExpense', temp_instance.pk,type)
            
            model_name='OfficeExpense'
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

def update_officeexpense_temp(code,total_office_expenses=None, top_expenses=None, utilities_expenses=None, rent_expenses=None, office_supplies_expenses=None, reported_date=None, employee_welfare_expenses=None, maintenance_expenses=None, comments=None):
    """
    Updates a OfficeExpense instance with the provided data.
    
    Args:
        officeexpense_id (int): ID of the OfficeExpense to update.
        total_office_expenses=None, top_expenses=None, utilities_expenses=None, rent_expenses=None, office_supplies_expenses=None, reported_date=None, employee_welfare_expenses=None, maintenance_expenses=None, comments=None: Keyword arguments for OfficeExpense fields to update.

    Returns:
        dict: Success or error message.
    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if  is_have_permission(request,APP_NAME, 'OfficeExpense',code):

            data={'total_office_expenses': total_office_expenses,
			'top_expenses': top_expenses,
			'utilities_expenses': utilities_expenses,
			'rent_expenses': rent_expenses,
			'office_supplies_expenses': office_supplies_expenses,
			'reported_date': reported_date,
			'employee_welfare_expenses': employee_welfare_expenses,
			'maintenance_expenses': maintenance_expenses,
			'comments': comments,}
            data['code']=code

            data['record_type']='update'
            # Initialize the serializer with the data
            serializer_temp = OfficeExpenseTempSerializer(data=data)
            #serializer_live=OfficeExpenseLiveSerializer(data=data)
            
            # Validate and save the serializer data
            if serializer_temp.is_valid() :
                temp_instance = serializer_temp.save()
                type=temp_instance.record_type
                # Call auditing and authorization functions if needed
                is_audit = model_audit(request,APP_NAME,'OfficeExpense',temp_instance.pk)
                is_authorization = self_authorization(request,APP_NAME,'OfficeExpense', temp_instance.pk,type)

                model_name='OfficeExpense'
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
    except  OfficeExpenseTemp.DoesNotExist:
        return error('Instance does not exist')
    except ValidationError as e:
        return error(f"Validation Error: {e}")
    except Exception as e:
        return error(f"An error occurred: {e}")



def view_officeexpense(officeexpense_id=None):
    """
    Retrieves and serializes a OfficeExpense instance by its ID or all instances if ID is None.
    
    Args:
        OfficeExpense_id (int, optional): ID of the OfficeExpense to retrieve.

    Returns:
        dict: A success response with the serialized data if found,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if officeexpense_id is not None:
            record = OfficeExpenseTemp.objects.get(pk=officeexpense_id)
            serializer = OfficeExpenseTempSerializer(record)
        else:
            obj = OfficeExpenseLive.objects.filter(is_deactivate=False)
            obj_pa = get_temp_record(request,APP_NAME,'OfficeExpense').filter(~Q(status='unauthorized_sent'))
            print('object--',obj_pa)
            obj_wait_auth = get_record_for_authorize(str(request.user.pk))
            # records = NoSeriesLinesALive.objects.all()
            live_data = OfficeExpenseLiveSerializer(obj, many=True).data
            temp_data = OfficeExpenseTempSerializer(obj_pa, many=True).data
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


def view_officeexpense_single(code):
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
        

        record = OfficeExpenseLive.objects.get(pk=code)
        serializer = OfficeExpenseLiveSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")


def pa_officeexpense(officeexpense_id,model_name):
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
        
        record = OfficeExpenseTemp.objects.get(pk=officeexpense_id)
        serializer = OfficeExpenseTempPASerializer(record).data
        
        type=record.record_type
        get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
        serializers=ModelRegistrationSerializer(get_table_name).data

        workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
        serializers_data=WorkflowMappingSerializer(workflow_mapping).data

        data={
            'officeexpense':serializer,
            'table_data':serializers,
            'workflow_data':serializers_data
        }
        return success(data)
    
    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def delete_officeexpense(officeexpense_id,model_name):
    """
    Deletes a OfficeExpense instance with the given ID.
    
    Args:
        officeexpense_id (int): ID of the OfficeExpense to delete.

    Returns:
        dict: A success response if deletion is successful,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        if  is_have_permission(request,APP_NAME, 'OfficeExpense', officeexpense_id):
            type='delete'

            is_authorization = self_authorization_for_delete(request,APP_NAME,model_name, officeexpense_id,type)
            user_ids_resp=get_next_user_from_work_flow(request,model_name,temp_instance=officeexpense_id,type=type)
 
            sent_auth=WorkflowMapping.objects.get(table_name__model_name__iexact=model_name,workflow_type=type)
            
            record = OfficeExpenseLive.objects.get(pk=officeexpense_id)
            serializer = OfficeExpenseLiveViewSerializer(record).data

            # get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
            # serializers=ModelRegistrationSerializer(get_table_name).data

            get_table_name = ModelRegistration.objects.get(model_name=model_name)
            serializers=ModelRegistrationSerializer(get_table_name).data

            print('table name of current',get_table_name)
            
            workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
            serializers_data=WorkflowMappingSerializer(workflow_mapping).data

            if user_ids_resp is not None and sent_auth.send_to_authorized == 'False' and sent_auth.same_user_authorized == 'False':

                obj = delete_record(request,APP_NAME, 'OfficeExpense', officeexpense_id)
                return success("Successfully deleted")
            else:
                data={
                    'OfficeExpense':serializer,
                    'table_data':serializers,
                    'workflow_data':serializers_data
                }
                return success(data)
        else:
            return error('you have no permission to delete the record')
    
    except OfficeExpenseLive.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def view_officeexpense_tempdata(officeexpense_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = OfficeExpenseTemp.objects.get(code=officeexpense_id)
        serializer = OfficeExpenseTempSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")
    

def view_officeexpense_live(officeexpense_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = OfficeExpenseLive.objects.get(code=officeexpense_id)
        serializer = OfficeExpenseLiveViewSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def authorize_request_data_OfficeExpense(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=OfficeExpenseTemp.objects.get(pk=pk)
        work_flow_type=get_instance.record_type
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,work_flow_type)
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()

        return success(req)
    
    except OfficeExpenseTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def authorize_request_data_delete_OfficeExpense(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=OfficeExpenseLive.objects.get(pk=pk)
  
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,type='delete')
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()
        return success(req)
    
    except OfficeExpenseTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")





#add foreign key import model.


def create_assetmanagement(total_fixed_assets, depreciation, maintenance_costs, asset_utilization_rate, repairs_and_upgrades_cost, reported_date, new_assets_acquired, comments):
    """
    Creates a AssetManagement instance with the provided data.
        Args:
        total_fixed_assets, depreciation, maintenance_costs, asset_utilization_rate, repairs_and_upgrades_cost, reported_date, new_assets_acquired, comments: Keyword arguments for AssetManagement fields.

    Returns:
        dict: Success or error message.
        APP_NAME = __name__.split('.')[0]

    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        data={'total_fixed_assets': total_fixed_assets,
			'depreciation': depreciation,
			'maintenance_costs': maintenance_costs,
			'asset_utilization_rate': asset_utilization_rate,
			'repairs_and_upgrades_cost': repairs_and_upgrades_cost,
			'reported_date': reported_date,
			'new_assets_acquired': new_assets_acquired,
			'comments': comments,}
        data['code'] = generate_random_id('ABC')
        data_create = data.copy()
        data_create['code'] = generate_random_id('ABC')
        data_create['record_type']='create'
        # Initialize the serializer with the data
        serializer_temp = AssetManagementTempSerializer(data=data_create)
        serializer_live=AssetManagementLiveSerializer(data=data)
        
        # Validate and save the serializer data
        if serializer_live.is_valid() and serializer_temp.is_valid() :
            temp_instance = serializer_temp.save()
            type=temp_instance.record_type
            # Call auditing and authorization functions if needed
            is_audit = model_audit(request,APP_NAME,'AssetManagement',temp_instance.pk)
            is_authorization = self_authorization(request,APP_NAME,'AssetManagement', temp_instance.pk,type)
            
            model_name='AssetManagement'
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

def update_assetmanagement_temp(code,total_fixed_assets=None, depreciation=None, maintenance_costs=None, asset_utilization_rate=None, repairs_and_upgrades_cost=None, reported_date=None, new_assets_acquired=None, comments=None):
    """
    Updates a AssetManagement instance with the provided data.
    
    Args:
        assetmanagement_id (int): ID of the AssetManagement to update.
        total_fixed_assets=None, depreciation=None, maintenance_costs=None, asset_utilization_rate=None, repairs_and_upgrades_cost=None, reported_date=None, new_assets_acquired=None, comments=None: Keyword arguments for AssetManagement fields to update.

    Returns:
        dict: Success or error message.
    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if  is_have_permission(request,APP_NAME, 'AssetManagement',code):

            data={'total_fixed_assets': total_fixed_assets,
			'depreciation': depreciation,
			'maintenance_costs': maintenance_costs,
			'asset_utilization_rate': asset_utilization_rate,
			'repairs_and_upgrades_cost': repairs_and_upgrades_cost,
			'reported_date': reported_date,
			'new_assets_acquired': new_assets_acquired,
			'comments': comments,}
            data['code']=code

            data['record_type']='update'
            # Initialize the serializer with the data
            serializer_temp = AssetManagementTempSerializer(data=data)
            #serializer_live=AssetManagementLiveSerializer(data=data)
            
            # Validate and save the serializer data
            if serializer_temp.is_valid() :
                temp_instance = serializer_temp.save()
                type=temp_instance.record_type
                # Call auditing and authorization functions if needed
                is_audit = model_audit(request,APP_NAME,'AssetManagement',temp_instance.pk)
                is_authorization = self_authorization(request,APP_NAME,'AssetManagement', temp_instance.pk,type)

                model_name='AssetManagement'
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
    except  AssetManagementTemp.DoesNotExist:
        return error('Instance does not exist')
    except ValidationError as e:
        return error(f"Validation Error: {e}")
    except Exception as e:
        return error(f"An error occurred: {e}")



def view_assetmanagement(assetmanagement_id=None):
    """
    Retrieves and serializes a AssetManagement instance by its ID or all instances if ID is None.
    
    Args:
        AssetManagement_id (int, optional): ID of the AssetManagement to retrieve.

    Returns:
        dict: A success response with the serialized data if found,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if assetmanagement_id is not None:
            record = AssetManagementTemp.objects.get(pk=assetmanagement_id)
            serializer = AssetManagementTempSerializer(record)
        else:
            obj = AssetManagementLive.objects.filter(is_deactivate=False)
            obj_pa = get_temp_record(request,APP_NAME,'AssetManagement').filter(~Q(status='unauthorized_sent'))
            print('object--',obj_pa)
            obj_wait_auth = get_record_for_authorize(str(request.user.pk))
            # records = NoSeriesLinesALive.objects.all()
            live_data = AssetManagementLiveSerializer(obj, many=True).data
            temp_data = AssetManagementTempSerializer(obj_pa, many=True).data
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


def view_assetmanagement_single(code):
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
        

        record = AssetManagementLive.objects.get(pk=code)
        serializer = AssetManagementLiveSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")


def pa_assetmanagement(assetmanagement_id,model_name):
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
        
        record = AssetManagementTemp.objects.get(pk=assetmanagement_id)
        serializer = AssetManagementTempPASerializer(record).data
        
        type=record.record_type
        get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
        serializers=ModelRegistrationSerializer(get_table_name).data

        workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
        serializers_data=WorkflowMappingSerializer(workflow_mapping).data

        data={
            'assetmanagement':serializer,
            'table_data':serializers,
            'workflow_data':serializers_data
        }
        return success(data)
    
    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def delete_assetmanagement(assetmanagement_id,model_name):
    """
    Deletes a AssetManagement instance with the given ID.
    
    Args:
        assetmanagement_id (int): ID of the AssetManagement to delete.

    Returns:
        dict: A success response if deletion is successful,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        if  is_have_permission(request,APP_NAME, 'AssetManagement', assetmanagement_id):
            type='delete'

            is_authorization = self_authorization_for_delete(request,APP_NAME,model_name, assetmanagement_id,type)
            user_ids_resp=get_next_user_from_work_flow(request,model_name,temp_instance=assetmanagement_id,type=type)
 
            sent_auth=WorkflowMapping.objects.get(table_name__model_name__iexact=model_name,workflow_type=type)
            
            record = AssetManagementLive.objects.get(pk=assetmanagement_id)
            serializer = AssetManagementLiveViewSerializer(record).data

            # get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
            # serializers=ModelRegistrationSerializer(get_table_name).data

            get_table_name = ModelRegistration.objects.get(model_name=model_name)
            serializers=ModelRegistrationSerializer(get_table_name).data

            print('table name of current',get_table_name)
            
            workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
            serializers_data=WorkflowMappingSerializer(workflow_mapping).data

            if user_ids_resp is not None and sent_auth.send_to_authorized == 'False' and sent_auth.same_user_authorized == 'False':

                obj = delete_record(request,APP_NAME, 'AssetManagement', assetmanagement_id)
                return success("Successfully deleted")
            else:
                data={
                    'AssetManagement':serializer,
                    'table_data':serializers,
                    'workflow_data':serializers_data
                }
                return success(data)
        else:
            return error('you have no permission to delete the record')
    
    except AssetManagementLive.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def view_assetmanagement_tempdata(assetmanagement_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = AssetManagementTemp.objects.get(code=assetmanagement_id)
        serializer = AssetManagementTempSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")
    

def view_assetmanagement_live(assetmanagement_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = AssetManagementLive.objects.get(code=assetmanagement_id)
        serializer = AssetManagementLiveViewSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def authorize_request_data_AssetManagement(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=AssetManagementTemp.objects.get(pk=pk)
        work_flow_type=get_instance.record_type
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,work_flow_type)
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()

        return success(req)
    
    except AssetManagementTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def authorize_request_data_delete_AssetManagement(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=AssetManagementLive.objects.get(pk=pk)
  
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,type='delete')
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()
        return success(req)
    
    except AssetManagementTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")





#add foreign key import model.


def create_logisticsandfleetmanagement(total_vehicles, vehicles_in_use, fuel_costs, maintenance_costs, vehicle_insurance_expenses, reported_date, vehicle_replacement_value, fleet_utilization_rate, fleet_safety_compliance_rate, vehicle_acquisition_cost, comments):
    """
    Creates a LogisticsAndFleetManagement instance with the provided data.
        Args:
        total_vehicles, vehicles_in_use, fuel_costs, maintenance_costs, vehicle_insurance_expenses, reported_date, vehicle_replacement_value, fleet_utilization_rate, fleet_safety_compliance_rate, vehicle_acquisition_cost, comments: Keyword arguments for LogisticsAndFleetManagement fields.

    Returns:
        dict: Success or error message.
        APP_NAME = __name__.split('.')[0]

    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        data={'total_vehicles': total_vehicles,
			'vehicles_in_use': vehicles_in_use,
			'fuel_costs': fuel_costs,
			'maintenance_costs': maintenance_costs,
			'vehicle_insurance_expenses': vehicle_insurance_expenses,
			'reported_date': reported_date,
			'vehicle_replacement_value': vehicle_replacement_value,
			'fleet_utilization_rate': fleet_utilization_rate,
			'fleet_safety_compliance_rate': fleet_safety_compliance_rate,
			'vehicle_acquisition_cost': vehicle_acquisition_cost,
			'comments': comments,}
        data['code'] = generate_random_id('ABC')
        data_create = data.copy()
        data_create['code'] = generate_random_id('ABC')
        data_create['record_type']='create'
        # Initialize the serializer with the data
        serializer_temp = LogisticsAndFleetManagementTempSerializer(data=data_create)
        serializer_live=LogisticsAndFleetManagementLiveSerializer(data=data)
        
        # Validate and save the serializer data
        if serializer_live.is_valid() and serializer_temp.is_valid() :
            temp_instance = serializer_temp.save()
            type=temp_instance.record_type
            # Call auditing and authorization functions if needed
            is_audit = model_audit(request,APP_NAME,'LogisticsAndFleetManagement',temp_instance.pk)
            is_authorization = self_authorization(request,APP_NAME,'LogisticsAndFleetManagement', temp_instance.pk,type)
            
            model_name='LogisticsAndFleetManagement'
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

def update_logisticsandfleetmanagement_temp(code,total_vehicles=None, vehicles_in_use=None, fuel_costs=None, maintenance_costs=None, vehicle_insurance_expenses=None, reported_date=None, vehicle_replacement_value=None, fleet_utilization_rate=None, fleet_safety_compliance_rate=None, vehicle_acquisition_cost=None, comments=None):
    """
    Updates a LogisticsAndFleetManagement instance with the provided data.
    
    Args:
        logisticsandfleetmanagement_id (int): ID of the LogisticsAndFleetManagement to update.
        total_vehicles=None, vehicles_in_use=None, fuel_costs=None, maintenance_costs=None, vehicle_insurance_expenses=None, reported_date=None, vehicle_replacement_value=None, fleet_utilization_rate=None, fleet_safety_compliance_rate=None, vehicle_acquisition_cost=None, comments=None: Keyword arguments for LogisticsAndFleetManagement fields to update.

    Returns:
        dict: Success or error message.
    """
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if  is_have_permission(request,APP_NAME, 'LogisticsAndFleetManagement',code):

            data={'total_vehicles': total_vehicles,
			'vehicles_in_use': vehicles_in_use,
			'fuel_costs': fuel_costs,
			'maintenance_costs': maintenance_costs,
			'vehicle_insurance_expenses': vehicle_insurance_expenses,
			'reported_date': reported_date,
			'vehicle_replacement_value': vehicle_replacement_value,
			'fleet_utilization_rate': fleet_utilization_rate,
			'fleet_safety_compliance_rate': fleet_safety_compliance_rate,
			'vehicle_acquisition_cost': vehicle_acquisition_cost,
			'comments': comments,}
            data['code']=code

            data['record_type']='update'
            # Initialize the serializer with the data
            serializer_temp = LogisticsAndFleetManagementTempSerializer(data=data)
            #serializer_live=LogisticsAndFleetManagementLiveSerializer(data=data)
            
            # Validate and save the serializer data
            if serializer_temp.is_valid() :
                temp_instance = serializer_temp.save()
                type=temp_instance.record_type
                # Call auditing and authorization functions if needed
                is_audit = model_audit(request,APP_NAME,'LogisticsAndFleetManagement',temp_instance.pk)
                is_authorization = self_authorization(request,APP_NAME,'LogisticsAndFleetManagement', temp_instance.pk,type)

                model_name='LogisticsAndFleetManagement'
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
    except  LogisticsAndFleetManagementTemp.DoesNotExist:
        return error('Instance does not exist')
    except ValidationError as e:
        return error(f"Validation Error: {e}")
    except Exception as e:
        return error(f"An error occurred: {e}")



def view_logisticsandfleetmanagement(logisticsandfleetmanagement_id=None):
    """
    Retrieves and serializes a LogisticsAndFleetManagement instance by its ID or all instances if ID is None.
    
    Args:
        LogisticsAndFleetManagement_id (int, optional): ID of the LogisticsAndFleetManagement to retrieve.

    Returns:
        dict: A success response with the serialized data if found,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        if logisticsandfleetmanagement_id is not None:
            record = LogisticsAndFleetManagementTemp.objects.get(pk=logisticsandfleetmanagement_id)
            serializer = LogisticsAndFleetManagementTempSerializer(record)
        else:
            obj = LogisticsAndFleetManagementLive.objects.filter(is_deactivate=False)
            obj_pa = get_temp_record(request,APP_NAME,'LogisticsAndFleetManagement').filter(~Q(status='unauthorized_sent'))
            print('object--',obj_pa)
            obj_wait_auth = get_record_for_authorize(str(request.user.pk))
            # records = NoSeriesLinesALive.objects.all()
            live_data = LogisticsAndFleetManagementLiveSerializer(obj, many=True).data
            temp_data = LogisticsAndFleetManagementTempSerializer(obj_pa, many=True).data
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


def view_logisticsandfleetmanagement_single(code):
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
        

        record = LogisticsAndFleetManagementLive.objects.get(pk=code)
        serializer = LogisticsAndFleetManagementLiveSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")


def pa_logisticsandfleetmanagement(logisticsandfleetmanagement_id,model_name):
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
        
        record = LogisticsAndFleetManagementTemp.objects.get(pk=logisticsandfleetmanagement_id)
        serializer = LogisticsAndFleetManagementTempPASerializer(record).data
        
        type=record.record_type
        get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
        serializers=ModelRegistrationSerializer(get_table_name).data

        workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
        serializers_data=WorkflowMappingSerializer(workflow_mapping).data

        data={
            'logisticsandfleetmanagement':serializer,
            'table_data':serializers,
            'workflow_data':serializers_data
        }
        return success(data)
    
    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def delete_logisticsandfleetmanagement(logisticsandfleetmanagement_id,model_name):
    """
    Deletes a LogisticsAndFleetManagement instance with the given ID.
    
    Args:
        logisticsandfleetmanagement_id (int): ID of the LogisticsAndFleetManagement to delete.

    Returns:
        dict: A success response if deletion is successful,
              or an error response if an exception occurs.
    """
    
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        if  is_have_permission(request,APP_NAME, 'LogisticsAndFleetManagement', logisticsandfleetmanagement_id):
            type='delete'

            is_authorization = self_authorization_for_delete(request,APP_NAME,model_name, logisticsandfleetmanagement_id,type)
            user_ids_resp=get_next_user_from_work_flow(request,model_name,temp_instance=logisticsandfleetmanagement_id,type=type)
 
            sent_auth=WorkflowMapping.objects.get(table_name__model_name__iexact=model_name,workflow_type=type)
            
            record = LogisticsAndFleetManagementLive.objects.get(pk=logisticsandfleetmanagement_id)
            serializer = LogisticsAndFleetManagementLiveViewSerializer(record).data

            # get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
            # serializers=ModelRegistrationSerializer(get_table_name).data

            get_table_name = ModelRegistration.objects.get(model_name=model_name)
            serializers=ModelRegistrationSerializer(get_table_name).data

            print('table name of current',get_table_name)
            
            workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type=type)
            serializers_data=WorkflowMappingSerializer(workflow_mapping).data

            if user_ids_resp is not None and sent_auth.send_to_authorized == 'False' and sent_auth.same_user_authorized == 'False':

                obj = delete_record(request,APP_NAME, 'LogisticsAndFleetManagement', logisticsandfleetmanagement_id)
                return success("Successfully deleted")
            else:
                data={
                    'LogisticsAndFleetManagement':serializer,
                    'table_data':serializers,
                    'workflow_data':serializers_data
                }
                return success(data)
        else:
            return error('you have no permission to delete the record')
    
    except LogisticsAndFleetManagementLive.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def view_logisticsandfleetmanagement_tempdata(logisticsandfleetmanagement_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = LogisticsAndFleetManagementTemp.objects.get(code=logisticsandfleetmanagement_id)
        serializer = LogisticsAndFleetManagementTempSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")
    

def view_logisticsandfleetmanagement_live(logisticsandfleetmanagement_id):
  
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
    
        record = LogisticsAndFleetManagementLive.objects.get(code=logisticsandfleetmanagement_id)
        serializer = LogisticsAndFleetManagementLiveViewSerializer(record).data
        
        return success(serializer)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def authorize_request_data_LogisticsAndFleetManagement(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=LogisticsAndFleetManagementTemp.objects.get(pk=pk)
        work_flow_type=get_instance.record_type
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,work_flow_type)
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()

        return success(req)
    
    except LogisticsAndFleetManagementTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def authorize_request_data_delete_LogisticsAndFleetManagement(table_name,approval_user_id,pk):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_instance=LogisticsAndFleetManagementLive.objects.get(pk=pk)
  
        req = authorize_request(table_name, pk, request.user.pk, approval_user_id,type='delete')
        if req:
            get_instance.status='unauthorized_sent'
            get_instance.save()
        return success(req)
    
    except LogisticsAndFleetManagementTemp.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")





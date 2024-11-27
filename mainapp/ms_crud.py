from django.utils import timezone

from django.core.exceptions import ValidationError
from workflow.ms_crud import custom_checking
from workflow.serializers import WorkflowMappingSerializer
from .models import *
from .serializers import *
from .middleware import get_current_request
from .scripts import *

APP_NAME = __name__.split('.')[0]
#Create your views here.

def get_table_name(model_name):
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()
        serializers=ModelRegistrationSerializer(get_table_name).data

        workflow_mapping=WorkflowMapping.objects.get(table_name=get_table_name,workflow_type='create')
        serializers_data=WorkflowMappingSerializer(workflow_mapping).data

        data={
            'table_data':serializers,
            'workflow_data':serializers_data
        }
        return success(data)
    
    except ModelRegistration.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def authorize_data(pk,app_name,model_name,work_flow_type):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        ApprovalRecords.objects.filter(
            approval_user=request.user,
            model_name__model_name__iexact=model_name,  # Filtering on the model name in ModelRegistration
        ).update(status="approved", updated_at=timezone.now())
        #ApprovalRecords.objects.filter(approval_user=request.user,model_name__model_name__iexact=model_name).update(status="Approved",updated_at=timezone.now())

        # here write the logic to check whether all user has been approved or not?
        obj = AuthorizeRequest.objects.filter(table_name__model_name__iexact=model_name,workflow_type=work_flow_type).last()

        if obj is not None and obj.next_approval_user is not None:

        # if obj.next_approval_user is not None:
          
            res = custom_checking(model_name)
 
            current_index = res.index(obj.next_approval_user.pk)
            # ===== thi code is for sequencial approval start ============
            i = 0
            for j in res:
                print('i ', i)
                print('current_index ', current_index)
                if i == current_index:
                    approval_user = j
                    print('i ', i)
                    print('i ', len(res))
                    if i+1 == len(res):
                        next_approval_user = None
                    else:
                        next_approval_user = res[i+1]
                    obj.approval_user_id = approval_user
                    obj.next_approval_user_id = next_approval_user
                    obj.save()
                    break
                i+=1
        
        move_temp_live = move_record_temp_to_live(request,app_name,model_name, pk)
        return success(move_temp_live)
    
    except Exception as e:
        return error(f"An error occurred: {e}")
    


def authorize_data_for_delete(pk,app_name,model_name):

    try:
       
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
      
        ApprovalRecords.objects.filter(
            approval_user=request.user,
            model_name__model_name__iexact=model_name,  # Filtering on the model name in ModelRegistration
        ).update(status="approved")

        # here write the logic to check whether all user has been approved or not?
        sent_auth=WorkflowMapping.objects.get(table_name__model_name__iexact=model_name,workflow_type='delete')

        if sent_auth.same_user_authorized == True :
            obj = delete_record(request,app_name, model_name, pk)
            return success('record deleted successfully')
        return success('data not be deleted')
    
    except Exception as e:
        return error(f"An error occurred: {e}")


def check_with_data(pk,model_name):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        is_cheker_valid = maker_checker_validation(request, model_name, pk)
        return success(is_cheker_valid)
    
    except Exception as e:
        return error(f"An error occurred: {e}")


def auth_request_data_with_obj(pk,app_name):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        auth_request = AuthorizeRequest.objects.get(pk=pk)
        record_id = auth_request.record_id
        table_name = auth_request.table_name
        print('im here.. ', record_id)

        work_flow_type=auth_request.workflow_type
        
        record_details = get_record_various_models_by_pk(app_name,table_name, record_id, output_as_dict=True,type=work_flow_type)
        serializers=AuthorizeRequestSerializer(auth_request).data
        data={
            'record_details':record_details,
            'record_id':serializers
        }     
        return success(data)
    
    except AuthorizeRequest.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")
    

def get_record_various_models_by_pk_data(pk,id,app_name,model_name):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')

        ApprovalRecords.objects.filter(
            approval_user=request.user,
            model_name__model_name__iexact=model_name,record_id=pk  # Filtering on the model name in ModelRegistration
        ).update(status="approved")

        # here write the logic to check whether all user has been approved or not?
        obj = AuthorizeRequest.objects.get(pk=id)
   
        work_flow_type=obj.workflow_type
        if obj is not None and obj.next_approval_user is not None:
         
            res = custom_checking(model_name)
            print(res)
            print('user of index : ',res.index(obj.next_approval_user.pk))
            current_index = res.index(obj.next_approval_user.pk) 
            # ===== thi code is for sequencial approval start ============
            i = 0
            for j in res:
                print('i ', i)
                print('current_index ', current_index)
                if i == current_index:
                    approval_user = j
                    print('i ', i)
                    print('i ', len(res))
                    if i+1 == len(res):
                        next_approval_user = None
                    else:
                        next_approval_user = res[i+1]
                    obj.approval_user_id = approval_user
                    obj.next_approval_user_id = next_approval_user
                    obj.save()
                    break
                i+=1
        else:
            if work_flow_type == 'delete':
             
                record = delete_record(request,app_name,model_name, obj.record_id)
            else:
                move_temp_live = move_record_temp_to_live(request,app_name,model_name, pk)

        if obj.next_approval_user is None:
            obj.is_authorized = True
            obj.save()

        serializers=AuthorizeRequestSerializer(obj).data
        return success(serializers)
    
    except AuthorizeRequest.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def have_permission(code,app_name,model_name):
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        if not is_have_permission(request,app_name, model_name, code):
            return success(False)
        else:
            return success(True)
    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")


# def unauthorized_return(notes,record_id,app_name,model_name,pk):
#     try:
#         request = get_current_request()
#         if not request.user.is_authenticated:
#             return error('Login required')
#         obj = get_record_various_models_by_pk(app_name,model_name, record_id, output_as_dict=False)
#         obj.status = 'unauthorized_return'
#         obj.notes = notes
#         obj.save()
#         # update status into the AuthorizeRequest table
#         obj_ar = AuthorizeRequest.objects.get(pk=pk)
#         obj_ar.is_authorized_return = True
#         obj_ar.save()

#         return success('unauthorized request returned sucessfully')
#     except Exception as e:
#         # Return an error response with the exception message
#         return error(f"An error occurred: {e}")


def unauthorized_return(notes,record_id,app_name,model_name,pk):
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        obj_ar = AuthorizeRequest.objects.get(pk=pk)
        obj_ar.is_authorized_return = True
        obj_ar.save()
        work_flowtype=obj_ar.workflow_type
        obj = get_record_various_models_by_pk(app_name,model_name, record_id,work_flowtype, output_as_dict=False)
        obj.status = 'unauthorized_return'
        obj.notes = notes
        obj.save()
        # update status into the AuthorizeRequest table
        # obj_ar = AuthorizeRequest.objects.get(pk=pk)
        # obj_ar.is_authorized_return = True
        # obj_ar.save()

        return success('unauthorized request returned sucessfully')
    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")



def get_record_from_the_various_models(app_name,model_name,code):
    try:
        record_details = get_record_various_models_by_pk(app_name,model_name, code, output_as_dict=True, model_suffix="Live")
        return success(record_details)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")


def delegate_user_data(user_id,model_name,pk):
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        model_get = ModelRegistration.objects.filter(model_name=model_name).last()

        resp = delegate_users(user_id, model_get.pk, pk)
        return success(resp)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")
    

def get_next_user_from_work_flow(request,model_name,type,temp_instance):
    try:
        get_table_name = ModelRegistration.objects.filter(model_name=model_name).first()

        approver_ids = custom_checking(model_name,type)
    
        approval_records = []
        if approver_ids is not None:
            for approver_id in approver_ids:
                approval_record = ApprovalRecords(model_name=get_table_name,record_id=temp_instance,approval_user_id=approver_id,status='pending')
                approval_records.append(approval_record)

            ApprovalRecords.objects.bulk_create(approval_records)
            user_ids_resp = custom_checking(model_name,type)
            
            next_approval_user_id = None  
            if user_ids_resp is not None:
                if len(user_ids_resp) == 1:
                    approval_user_id = user_ids_resp[0]
                 
                else:
                    approval_user_id = user_ids_resp[0]
              
                    next_approval_user_id = user_ids_resp[1]
                
                req = authorize_request(get_table_name.pk, temp_instance, request.user.pk, approval_user_id,type=type,next_approval_user=next_approval_user_id)
            return None
        return None
    except Exception as e:
        return error(f"An error occurred: {e}")
        
    
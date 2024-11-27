from mainapp.middleware import get_current_request
from .models import *
from mainapp.models import AuthorizeRequest
from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Max
from django.http import JsonResponse
from .scripts import id_generation
from .field_validation import *
from mainapp.scripts import *
from .serializers import *

def get_workflow_setup(model_name,type=None):
    """
    This function is responsible to check whether given model name is mapped with workflow setup or not.\
    Args:
        model_name:  str type, pass name of the models that already registered

    Returns: setup_id if found else None

    """

    try:
        obj = WorkflowMapping.objects.filter(table_name__model_name__iexact=model_name)
        print('data is comming or not',obj)
        print('work flow type',type)
        if obj.exists():
            if type:
                print('type is commming',type)
                data=obj.get(workflow_type=type)
                if data.workflow is not None:
                    print('delete data is comming',data)
                    print('delete work pk',data.workflow.pk)
                    return data.workflow.pk
                else:
                    None
            else:
                latest_mapped = obj.last()
                return latest_mapped.workflow.pk
        else:
            return None
    except Exception as error:
        print('Error Function Name : get_workflow_setup : Error Is : ',error)
        return None


def get_workflow_setup_details(workflow_setup_id):
    """
    this function is responsible for check and if records is existing then it will return the records details else None.
    Args:
        workflow_setup_id: str type

    Returns: It will return the models objects if founds else None

    """

    try:
        obj = WorkflowSetup.objects.get(pk=workflow_setup_id)
        return obj
    except Exception as error:
        print('Error Function Name : workflow_setup_id : Error Is : ', error)
        return None
    
def approve_details_of_workflow_group(group_id):
    """

    Args:
        group_id: to get the list of user in sequence that added into this group

    Returns: list of user else None

    """

    try:
        obj = WorkflowUserGroupMapping.objects.filter(workflow_group_id=group_id).order_by('sequence')
        user_list = []
        if obj.exists():
            for data in obj:
                user_list.append(data.user.pk)
            return user_list
        else:
            return None

    except Exception as error:

        print('Error Function Name : approve_details_of_workflow_group : Error Is : ', error)
        return None

def send_authorized_request_custom(table_name_id,record_id,sender_user,approval_user_id):
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
                return error('Login required')
        obj = AuthorizeRequest(
            table_name_id=table_name_id,
            record_id=record_id,
            sender_user_id=sender_user,
            approval_user_id=approval_user_id,
        )

        obj.save()
        return success('Request Sucessfully Saved')

    except Exception as error:
        print('Error Function Name : send_authorized_request_custom : Error Is : ', error)
        return None



def approval_count(model_name):
    try:
        """
        Calculate the approval count based on approver details and type.
        Args:
            model_name (str): The name of the model to calculate approval count for.

        Returns:
            int: Approval count required for the given model's workflow setup.
        """
        workflow_setup_id = get_workflow_setup(model_name)
        
        if workflow_setup_id:
            setup_details = get_workflow_setup_details(workflow_setup_id)
            
            if setup_details:
                approver_type = setup_details.approver_type
                approver_limit_type = setup_details.approver_limit_type

                if approver_type == 'Approver' and approver_limit_type == 'Specific_Approver':
                    return 1  

                if approver_type == 'Workflow_User_Group' and approver_limit_type == 'Group_Approver':
                    # Use workflow user group ID to get approvers in the group
                    group_id = setup_details.user_group_mapping.pk
                    approval_details = approve_details_of_workflow_group(group_id)
                    return success(len(approval_details) if approval_details else 0)

        return success(0) 
    except Exception as e:
        return error(f"An error occurred: {e}")


def custom_checking(model_name,type=None):
    try:
        get_workflow_setup_resp = get_workflow_setup(model_name,type)
        print('get workflow setup',get_workflow_setup_resp)
        if get_workflow_setup_resp is not None:
            wfsd = get_workflow_setup_details(get_workflow_setup_resp)
            print('data is comming',wfsd)
            if wfsd is not None:
                approver_type = wfsd.approver_type
                approver_limit_type = wfsd.approver_limit_type
                print('approver_type ', approver_type)
                print('approver_limit_type ', approver_limit_type)
                approver_ids = []
                if approver_type == 'Approver' and approver_limit_type == 'Specific_Approver':
                    approver_id = wfsd.approver_id.pk
                    print('approver_id', approver_id)
                    approver_ids.append(approver_id)
                    print('approver_ids', approver_ids)
                    return approver_ids
            
                if approver_type == 'Workflow_User_Group' and approver_limit_type == 'Group_Approver':
                    group_id = wfsd.user_group_mapping.pk
                    approval_details = approve_details_of_workflow_group(group_id)
                    print('approval_details ', approval_details)
                    if approval_details is not None:
                        return approval_details
            else:
                return None
        return None
    except Exception as e:
        return error(f"An error occurred: {e}")


#===============================MS=================================



# ==================== Sequence =======================

def sequence_list(pk=None):
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
                return error('Login required')
        if pk is not None:
            sequences = Sequence.objects.get(pk=pk)
            serializers=SequenceSerializer(sequences)
        else:
            sequences = Sequence.objects.all()
            serializers=SequenceSerializer(sequences,many=True)
        
        return success(serializers.data)
    except Sequence.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")

def sequence_create(sequence_series,description):
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        instance = Sequence.objects.create(
            sequence_series=sequence_series,
            description=description,
            created_by=request.user
        )
        return success(f'Successfully created {instance} ')
    
    except Sequence.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def sequence_update(pk,sequence_series,description):
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        instance = Sequence.objects.get(pk=pk)
        instance.sequence_series=sequence_series
        instance.description=description
        instance.updated_by=request.user
        instance.save()
        return success(f'Successfully Updated {instance} ')
    
    except Sequence.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")
    

def sequence_delete(pk):
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        instance = Sequence.objects.get(pk=pk)
        instance.delete()
           
        return success(f'Successfully deleted {instance} ')
    
    except Sequence.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")




 # ====================Workflow Category =======================

def workflow_category_list(pk=None):
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
                return error('Login required')
        if pk is not None:
            instances=WorkflowCategory.objects.get(pk=pk)
            serializers=WorkflowCategorySerializer(instances)
        else:
            instances = WorkflowCategory.objects.all()
            serializers=WorkflowCategorySerializer(instances,many=True)
        return success(serializers.data)
    except WorkflowCategory.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")

def workflow_category_create(code,description=None):
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        instance = WorkflowCategory.objects.create(
            code=code,
            description=description,
            created_by=request.user
        )
        return success(f'Successfully created {instance} ')
    
    except WorkflowCategory.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")
   
def workflow_category_update(pk,code,description=None):
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        instance = WorkflowCategory.objects.get(pk=pk)
        instance.code=code
        instance.description=description
        instance.updated_by=request.user
        instance.save()
        return success(f'Successfully Updated {instance} ')
    
    except WorkflowCategory.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")

def workflow_category_delete(pk):
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        instance = WorkflowCategory.objects.get(pk=pk)
        instance.delete()           
        return success(f'Successfully deleted {instance} ')
    
    except WorkflowCategory.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")

# =============Workflow Group =============================

def workflow_group_list(pk=None):
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
                return error('Login required')
        if pk is not None:
            instances=WorkflowGroup.objects.get(pk=pk)
            serializers=WorkflowGroupSerializer(instances)
        instances = WorkflowGroup.objects.all()
        serializers=WorkflowGroupSerializer(instances,many=True)
    
        return success(serializers.data)
    except WorkflowGroup.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def workflow_group_create(code,description=None):
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        instance = WorkflowGroup.objects.create(
            code=code,
            description=description,
            created_by=request.user
        )
        return success(f'Successfully created {instance} ')
    
    except WorkflowGroup.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")

def workflow_group_update(pk,code,description=None):
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        instance = WorkflowGroup.objects.get(pk=pk)
        instance.code=code
        instance.description=description
        instance.updated_by=request.user
        instance.save()
        return success(f'Successfully Updated {instance} ')
    
    except WorkflowGroup.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")

   
def workflow_group_delete(pk):
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        instance = WorkflowGroup.objects.get(pk=pk)
        instance.delete()
           
        return success(f'Successfully deleted {instance} ')
    
    except WorkflowGroup.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")
   

# ============== Workflow User Group mapping ====================

def workflow_user_group_mapping_list(pk=None):
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
                return error('Login required')
        if pk is not None:
            instances=WorkflowUserGroupMapping.objects.get(pk=pk)
            serializers=WorkflowUserGroupMappingSerializer(instances)
        else:
            instances = WorkflowUserGroupMapping.objects.all()
            serializers=WorkflowUserGroupMappingSerializer(instances,many=True)
        
        return success(serializers.data)
    except WorkflowUserGroupMapping.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")



def workflow_user_group_mapping_create(workflow_group,user,sequence):
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')

        workflow_group=WorkflowGroup.objects.get(code=workflow_group)

        sequence=Sequence.objects.get(sequence_series=sequence)
  
        instance = WorkflowUserGroupMapping.objects.create(
            workflow_group=workflow_group,
            user_id=user,
            sequence=sequence,
            created_by=request.user
        )
        return success(f'Successfully created {instance} ')
    
    except WorkflowUserGroupMapping.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")
   

def workflow_user_group_mapping_update(pk,workflow_group,user,sequence):
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        sequence=Sequence.objects.get(id=sequence)
        workflow_group=WorkflowGroup.objects.get(code=workflow_group)
        instance = WorkflowUserGroupMapping.objects.get(pk=pk)
        instance.workflow_group=workflow_group
        instance.user_id=user
        instance.sequence=sequence
        instance.updated_by=request.user
        instance.save()
        return success(f'Successfully Updated {instance} ')
    
    except WorkflowUserGroupMapping.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")



def workflow_user_group_mapping_delete(pk):
    try:
        # Fetch the mapping to be deleted
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        mapping = WorkflowUserGroupMapping.objects.get(pk=pk)
        
        # Capture the workflow group and sequence series before deletion
        workflow_group = mapping.workflow_group
        deleted_sequence_series = mapping.sequence.sequence_series
        
        # Delete the mapping
        mapping.delete()

        # Shift the remaining mappings for the same workflow group
        mappings_to_update = WorkflowUserGroupMapping.objects.filter(
            workflow_group=workflow_group,
            sequence__sequence_series__gt=deleted_sequence_series
        ).order_by('sequence__sequence_series')

        # Loop through each mapping and decrease the sequence_series by 1
        for map_item in mappings_to_update:
            map_item.sequence.sequence_series -= 1
            map_item.sequence.save()  # Save the updated sequence for each mapping
        
        return success(f'Successfully deleted {mapping} ')
    except WorkflowUserGroupMapping.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")
   
# -------------------------- dropdown option within db limit


def get_next_sequence(workflow_group_id):
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
                return error('Login required')  
        last_mapping = WorkflowUserGroupMapping.objects.filter(workflow_group_id=workflow_group_id).order_by('-sequence__sequence_series').first()
        
        max_sequence = Sequence.objects.aggregate(Max('sequence_series'))['sequence_series__max']
        
        if last_mapping:
            last_sequence = last_mapping.sequence.sequence_series
            next_sequences = []
            for seq in range(last_sequence + 1, last_sequence + 6):
                if seq <= max_sequence:
                    next_sequences.append(seq)
                else:
                    break
        else:
            # Starting from 1 if no previous sequence exists, but limited by max_sequence
            next_sequences = list(range(1, min(6, max_sequence + 1)))
            print('next sdepp--',next_sequences)
        return success({'next_sequences': next_sequences})
    
    except Exception as e:
        return error(f"An error occurred: {e}")


# ================== Workflow Setup ==================================


def workflow_setup_list(pk=None):
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
                return error('Login required')
        print('data is comming',pk)
        if pk is not None:
            instances=WorkflowSetup.objects.get(pk=pk)
            serializers=WorkflowSetupSerializer(instances)
        else:
            instances = WorkflowSetup.objects.all()
            serializers=WorkflowSetupSerializer(instances,many=True)
        return success(serializers.data)
    except WorkflowSetup.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")
  

def workflow_setup_create(code,category,enabled,approver_type,approver_limit_type,description=None,approver_id=None,user_group_mapping=None):
    
    try:
        if user_group_mapping:
            user_group=WorkflowGroup.objects.get(code=user_group_mapping)
        else:
            user_group=None
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        instance = WorkflowSetup.objects.create(
            code=code,
            description=description,
            category_id=category,
            enabled=enabled,
            approver_type=approver_type,
            approver_limit_type=approver_limit_type,
            approver_id_id=approver_id,
            user_group_mapping=user_group,
            created_by=request.user
        )
        return success(f'Successfully created {instance} ')
    
    except WorkflowSetup.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")
    

def workflow_setup_update(pk,code,category,enabled,approver_type,approver_limit_type,description=None,approver_id=None,user_group_mapping=None):
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        if user_group_mapping:
            user_group=WorkflowGroup.objects.get(code=user_group_mapping)
        else:
            user_group=None
        instance = WorkflowSetup.objects.get(pk=pk)
        instance.code=code
        instance.description=description
        instance.updated_by=request.user
        instance.category_id=category
        instance.enabled=enabled
        instance.approver_type=approver_type
        instance.approver_limit_type=approver_limit_type
        instance.approver_id_id=approver_id
        instance.user_group_mapping=user_group
        instance.updated_by=request.user
        instance.save()
        return success(f'Successfully Updated {instance} ')
    
    except WorkflowSetup.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def workflow_setup_delete(pk):
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        instance = WorkflowSetup.objects.get(pk=pk)
        instance.delete()
           
        return success(f'Successfully deleted {instance} ')
    
    except WorkflowGroup.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


# ================ User Approval limits =======================

def user_approval_limit_list():
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
                return error('Login required')
        instances = UserApprovalLimit.objects.all()
        serializers=UserApprovalLimitSerializer(instances,many=True)
    
        return success(serializers.data)
    except UserApprovalLimit.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")
 

def user_approval_limit_create(approval_limit_code,mode,value,limit_mode,limit_value,user):
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        instance = UserApprovalLimit.objects.create(
            approval_limit_code=approval_limit_code,
            mode=mode,
            value=value,
            limit_mode=limit_mode,
            limit_value=limit_value,
            user_id=user,
            created_by=request.user
        )
        return success(f'Successfully created {instance} ')
    
    except UserApprovalLimit.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")
   

def user_approval_limit_update(pk,approval_limit_code,mode,value,limit_mode,limit_value,user):
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        instance = UserApprovalLimit.objects.get(pk=pk)
        instance.approval_limit_code=approval_limit_code
        instance.mode=mode
        instance.value=value
        instance.limit_mode=limit_mode
        instance.limit_value=limit_value
        instance.user_id=user
        instance.updated_by=request.user
        instance.save()
        return success(f'Successfully Updated {instance} ')
    
    except UserApprovalLimit.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")
    

def user_approval_limit_delete(pk):
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        
        instance = UserApprovalLimit.objects.get(pk=pk)
        instance.delete()
           
        return success(f'Successfully deleted {instance} ')
    
    except UserApprovalLimit.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")
 


# ----------------------- Workflow Mapping  ------------------------------

def workflow_model_list(pk=None):
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
                return error('Login required')
        if pk is not None:
            instances=ModelRegistration.objects.get(pk=pk)
            serializers=ModelRegistrationSerializer(instances)
        else:
            instances = ModelRegistration.objects.all()
            serializers=ModelRegistrationSerializer(instances,many=True)
        
        return success(serializers.data)
    except ModelRegistration.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")
 
def workflow_mapping_list(pk):
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
                return error('Login required')

        instances=WorkflowMapping.objects.filter(table_name=pk)
        serializers=WorkflowMappingSerializer(instances,many=True)
        return success(serializers.data)
    except WorkflowMapping.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def workflow_mapping_update(pk,model_id,self_authorized,same_user_authorized,send_to_authorize,workflow_authorize,workflow=None):
    try:
        print('data is comming',pk)
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        if workflow:
            workflow=WorkflowSetup.objects.get(pk=workflow)
        else:
            workflow=None
        instance = WorkflowMapping.objects.get(pk=pk)
        instance.table_name_id=model_id
        instance.self_authorized=self_authorized
        instance.same_user_authorized=same_user_authorized
        instance.send_to_authorized=send_to_authorize
        instance.workflow_authorize=workflow_authorize
        instance.workflow=workflow
        instance.save()
        return success(f'Successfully Updated {instance} ')
    
    except WorkflowMapping.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


# def workflow_mapping_delete(pk):
#     try:
#         request = get_current_request()
#         if not request.user.is_authenticated:
#             return error('Login required')
        
#         instance = WorkflowModelRegistration.objects.get(pk=pk)
#         instance.delete()
           
#         return success(f'Successfully deleted {instance} ')
    
#     except WorkflowModelRegistration.DoesNotExist:
#         return error('Instance does not exist')
#     except Exception as e:
#         return error(f"An error occurred: {e}")
    
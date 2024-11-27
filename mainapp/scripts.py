from .models import *
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.db.models import Q
from django.forms.models import model_to_dict
import random
import string

def id_generation(prefix=None):
    print('prefix ', prefix)
    if prefix is not None:
        return str(str(prefix) + '-' + str(random.randint(1111, 9999)))
    else:
        return str('NA' + '-' + str(random.randint(1111, 9999)))

def simple_unique_id_generation(pre,obj):
    # Calculating the total number of* records and incrementing by 1
    if obj:
        tot_rec_count=obj + 1
    else:
        tot_rec_count=1
     # Creating a unique ID b   ased on the total record count and the provided prefix
    if len(str(tot_rec_count)) == 1:
        id=pre+'000'+str(tot_rec_count)
    elif  len(str(tot_rec_count)) == 2:
        id=pre+'00'+str(tot_rec_count)
    else: 
        id=pre+str(tot_rec_count)
    return id


counter = 1

def new_simple_unique_id_generation(pre):
    global counter
    # Create a unique ID based on the counter and the provided prefix
    if len(str(counter)) == 1:
        unique_id = pre + '000' + str(counter)
    elif len(str(counter)) == 2:
        unique_id = pre + '00' + str(counter)
    elif len(str(counter)) == 3:
        unique_id = pre + '0' + str(counter)
    else:
        unique_id = pre + str(counter)
    
    # Increment the counter for the next unique ID
    counter += 1
    return unique_id

def generate_random_id(prefix, length=8):
    # Generate a random string of the specified length using letters and digits
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    
    # Combine the prefix and random string
    random_id = prefix + random_part
    return random_id

def record_history(request,app_name,model_name, record_id):
    """
    Moves a specific record from the source model to the history model and deletes the original record.

    Args:
        source_model_name (str): The name of the model from which records are to be moved.
        history_model_name (str): The name of the model where the record should be archived.
        record_id (int): The primary key of the record to be moved.
        is_deleted (None):

    Returns:
        bool: True if the operation was successful, False otherwise.

    Raises:
        Exception: Any error encountered during the process is caught and logged.
    """
    try:
        # Dynamically retrieve the models using Django's apps registry
        source_model = apps.get_model(app_name, f'{model_name}Live')
        history_model = apps.get_model(app_name, f'{model_name}History')

        # Fetch the specific record by primary key
        source_records = source_model.objects.filter(pk=record_id)

        if source_records.exists():
            for record in source_records:
                aa=record
                custom_id = generate_custom_record_id(record.pk)
                record_count = history_model.objects.filter(code=record.pk).count()
                if record_count==0:
                    audit_status = 'created'
                else:
                    audit_status='updated'
                
                if aa.is_deactivate:
                    record_count -= 1
                    audit_status='deleted'

                fields_and_values = {
                    field.name: getattr(record, field.name)
                    for field in record._meta.fields
                }
                # Create a new record in the history model, copying all fields except the primary key
                history_record = history_model.objects.create(
                    custom_record_id=custom_id,
                    version=record_count,
                    **fields_and_values,
                )
                history_record.save()
             
                model_audit(request,app_name,model_name,record_id,audit_status)
            return True
        else:
            print('record_history raised error: record not found')
            return False
    except Exception as error:
        print('record_history function raised an error:', error)
        return False


# def move_record_temp_to_live(request,app_name,model_name, record_id, exclude_fields=['status', 'notes','record_type']):
    
#     print('move record temp to live three',request,app_name,model_name,record_id)
#     """
#     Moves a specific record from a temporary model to a live model and deletes the temp record.

#     Args:
#         temp_model_name (str): The name of the temporary model from which records are to be moved.
#         live_model_name (str): The name of the live model where the record should be moved.
#         history_model_name (str): The name of the history model where the history should be recorded.
#         record_id (int): The primary key of the record to be moved.
#         exclude_fields (list): A list of field names to exclude from the copy operation.

#     Returns:
#         bool: True if the operation was successful, False otherwise.

#     Raises:
#         Exception: Any error encountered during the process is caught and logged.
#     """
#     try:
#         # Dynamically retrieve the models using Django's apps registry
#         temp_model = apps.get_model(app_name, f'{model_name}Temp')
#         live_model = apps.get_model(app_name, f'{model_name}Live')

#         # Fetch the specific record by primary key from the temporary model
#         temp_record = temp_model.objects.get(pk=record_id)

#         # Create a new record in the live model, copying all fields except the primary key and excluded fields
#         fields_and_values = {
#             field.name: getattr(temp_record, field.name)
#             for field in temp_record._meta.fields
#             if field.name not in exclude_fields
#         }
#         obj_live = live_model.objects.filter(pk=record_id).first()
#         if obj_live:
#             # Update the existing record
#             for field, value in fields_and_values.items():
#                 setattr(obj_live, field, value)
#             obj_live.save()
#             # Record the history
#             record_history(request,app_name,model_name, obj_live.pk)

#             # Optionally delete the record from the temporary model after moving
#             temp_record.delete()
#             return True
#         else:
#             live_record = live_model.objects.create(**fields_and_values)
#             # Record the history
#             record_history(request,app_name,model_name, live_record.pk)

#             # Optionally delete the record from the temporary model after moving
#             temp_record.delete()

#             return True
#     except temp_model.DoesNotExist:
#         print('move_record_temp_to_live raised error: record not found')
#         return False
#     except Exception as error:
#         print('move_record_temp_to_live move_record_123_temp_to_live function raised an error:', error)
#         return False


def move_record_temp_to_live(request,app_name,model_name, record_id, exclude_fields=['status', 'notes','record_type']):
    
    print('move record temp to live three',request,app_name,model_name,record_id)
    """
    Moves a specific record from a temporary model to a live model and deletes the temp record.

    Args:
        temp_model_name (str): The name of the temporary model from which records are to be moved.
        live_model_name (str): The name of the live model where the record should be moved.
        history_model_name (str): The name of the history model where the history should be recorded.
        record_id (int): The primary key of the record to be moved.
        exclude_fields (list): A list of field names to exclude from the copy operation.

    Returns:
        bool: True if the operation was successful, False otherwise.

    Raises:
        Exception: Any error encountered during the process is caught and logged.
    """
    try:
        # Dynamically retrieve the models using Django's apps registry
        temp_model = apps.get_model(app_name, f'{model_name}Temp')
        live_model = apps.get_model(app_name, f'{model_name}Live')


        # Retrieve the temp_record
        temp_record = temp_model.objects.get(pk=record_id)

        # Get regular fields and their values
        fields_and_values = {
            field.name: getattr(temp_record, field.name)
            for field in temp_record._meta.fields
            if field.name not in exclude_fields
        }
        print('fields_and_values:', fields_and_values)

        many_to_many_values = {}
        for m2m_field in temp_record._meta.many_to_many:
            if m2m_field.name not in exclude_fields:
                # Get the related model
                related_manager = getattr(temp_record, m2m_field.name)
                related_model = related_manager.model

                # Determine the primary key field to use ('code' or fallback to the first available field)
                primary_key_field = (
                    'code' if 'code' in [field.name for field in related_model._meta.fields] else related_model._meta.pk.name
                )

                # Safely fetch values for the ManyToManyField
                many_to_many_values[m2m_field.name] = list(
                    related_manager.values_list(primary_key_field, flat=True)
                ) if related_manager.exists() else []

        # Find the live record
        obj_live = live_model.objects.filter(pk=record_id).first()
        if obj_live:
            # Update regular fields
            for field, value in fields_and_values.items():
                setattr(obj_live, field, value)
            obj_live.save()

            # Update ManyToManyField relationships
            for m2m_field, value in many_to_many_values.items():
                related_manager = getattr(obj_live, m2m_field)

                if value:  # Only update if the list is not empty
                    related_objects = (
                        related_manager.model.objects.filter(code__in=value)
                        if 'code' in [field.name for field in related_manager.model._meta.fields]
                        else related_manager.model.objects.filter(id__in=value)
                    )
                    related_manager.set(related_objects)  # Update relationships
                else:
                # If the list is empty, clear the relationships
                    related_manager.clear()

            # Record the history
            record_history(request, app_name, model_name, obj_live.pk)

            # Optionally delete the record from the temporary model after moving
            temp_record.delete()
            return True
        else:
            # Create a new record
            live_record = live_model.objects.create(**fields_and_values)

            # Set ManyToManyField relationships
            for m2m_field, value in many_to_many_values.items():
                related_manager = getattr(live_record, m2m_field)
               
                related_objects = (
                    related_manager.model.objects.filter(code__in=value)
                    if 'code' in [field.name for field in related_manager.model._meta.fields]
                    else related_manager.model.objects.filter(id__in=value)
                )
                related_manager.set(related_objects)

            # Record the history
            record_history(request, app_name, model_name, live_record.pk)

            # Optionally delete the record from the temporary model after moving
            temp_record.delete()
            return True

    except temp_model.DoesNotExist:
        print('move_record_temp_to_live raised error: record not found')
        return False
    except Exception as error:
        print('move_record_temp_to_live move_record_123_temp_to_live function raised an error:', error)
        return False


# def move_record_temp_to_live(request,app_name,model_name, record_id, exclude_fields=['status', 'notes','record_type']):
    
#     print('move record temp to live three',request,app_name,model_name,record_id)
#     """
#     Moves a specific record from a temporary model to a live model and deletes the temp record.

#     Args:
#         temp_model_name (str): The name of the temporary model from which records are to be moved.
#         live_model_name (str): The name of the live model where the record should be moved.
#         history_model_name (str): The name of the history model where the history should be recorded.
#         record_id (int): The primary key of the record to be moved.
#         exclude_fields (list): A list of field names to exclude from the copy operation.

#     Returns:
#         bool: True if the operation was successful, False otherwise.

#     Raises:
#         Exception: Any error encountered during the process is caught and logged.
#     """
#     try:
#         # Dynamically retrieve the models using Django's apps registry
#         temp_model = apps.get_model(app_name, f'{model_name}Temp')
#         live_model = apps.get_model(app_name, f'{model_name}Live')

#         # Fetch the specific record by primary key from the temporary model
#         temp_record = temp_model.objects.get(pk=record_id)
        
#         fields_and_values = {
#             field.name: getattr(temp_record, field.name)
#             for field in temp_record._meta.fields
#             if field.name not in exclude_fields
#         }

#         # Handle ManyToManyField relationships separately
#         many_to_many_values = {}
#         for m2m_field in temp_record._meta.many_to_many:
#             if m2m_field.name not in exclude_fields:
#                 primary_key_field = 'code' if hasattr(getattr(temp_record, m2m_field.name).first(), 'code') else 'id'
#                 many_to_many_values[m2m_field.name] = list(
#                     getattr(temp_record, m2m_field.name).values_list(primary_key_field, flat=True)
#                 )
        
#         obj_live = live_model.objects.filter(pk=record_id).first()
#         if obj_live:
#             # Update the existing record
#             for field, value in fields_and_values.items():
#                 setattr(obj_live, field, value)  # Only set regular fields
#             obj_live.save()

#             # Update ManyToManyField relationships
#             for m2m_field, value in many_to_many_values.items():
#                 related_manager = getattr(obj_live, m2m_field)
              
#                 related_objects = (
#                     related_manager.model.objects.filter(code__in=value)
#                     if 'code' in [field.name for field in related_manager.model._meta.fields]
#                     else related_manager.model.objects.filter(id__in=value)
#                 )
#                 related_manager.set(related_objects)

#             # Record the history
#             record_history(request, app_name, model_name, obj_live.pk)

#             # Optionally delete the record from the temporary model after moving
#             temp_record.delete()
#             return True
#         else:
#             # Create a new record
#             live_record = live_model.objects.create(**fields_and_values)

#             # Set ManyToManyField relationships
#             for m2m_field, value in many_to_many_values.items():
#                 related_manager = getattr(live_record, m2m_field)
               
#                 related_objects = (
#                     related_manager.model.objects.filter(code__in=value)
#                     if 'code' in [field.name for field in related_manager.model._meta.fields]
#                     else related_manager.model.objects.filter(id__in=value)
#                 )
#                 related_manager.set(related_objects)

#             # Record the history
#             record_history(request, app_name, model_name, live_record.pk)

#             # Optionally delete the record from the temporary model after moving
#             temp_record.delete()
#             return True

#     except temp_model.DoesNotExist:
#         print('move_record_temp_to_live raised error: record not found')
#         return False
#     except Exception as error:
#         print('move_record_temp_to_live move_record_123_temp_to_live function raised an error:', error)
#         return False


# def move_record_temp_to_live(request,app_name,model_name, record_id, exclude_fields=['status', 'notes','record_type']):
    
#     print('move record temp to live three',request,app_name,model_name,record_id)
#     """
#     Moves a specific record from a temporary model to a live model and deletes the temp record.

#     Args:
#         temp_model_name (str): The name of the temporary model from which records are to be moved.
#         live_model_name (str): The name of the live model where the record should be moved.
#         history_model_name (str): The name of the history model where the history should be recorded.
#         record_id (int): The primary key of the record to be moved.
#         exclude_fields (list): A list of field names to exclude from the copy operation.

#     Returns:
#         bool: True if the operation was successful, False otherwise.

#     Raises:
#         Exception: Any error encountered during the process is caught and logged.
#     """
#     try:
#         # Dynamically retrieve the models using Django's apps registry
#         temp_model = apps.get_model(app_name, f'{model_name}Temp')
#         live_model = apps.get_model(app_name, f'{model_name}Live')

#         # Fetch the specific record by primary key from the temporary model
#         temp_record = temp_model.objects.get(pk=record_id)
        
#         fields_and_values = {
#             field.name: getattr(temp_record, field.name)
#             for field in temp_record._meta.fields
#             if field.name not in exclude_fields
#         }

#         # Handle ManyToManyField relationships separately
#         many_to_many_values = {}
#         for m2m_field in temp_record._meta.many_to_many:
#             if m2m_field.name not in exclude_fields:
#                 primary_key_field = 'code' if hasattr(getattr(temp_record, m2m_field.name).first(), 'code') else 'id'
#                 many_to_many_values[m2m_field.name] = list(
#                     getattr(temp_record, m2m_field.name).values_list(primary_key_field, flat=True)
#                 )

#         obj_live = live_model.objects.filter(pk=record_id).first()
#         if obj_live:
#             # Update the existing record
#             for field, value in fields_and_values.items():
#                 setattr(obj_live, field, value)  # Only set regular fields
#             obj_live.save()

#             # Update ManyToManyField relationships
#             for m2m_field, value in many_to_many_values.items():
#                 related_manager = getattr(obj_live, m2m_field)
#                 related_objects = (
#                     related_manager.model.objects.filter(code__in=value)
#                     if 'code' in related_manager.model._meta.get_fields()[0].name
#                     else related_manager.model.objects.filter(id__in=value)
#                 )
#                 related_manager.set(related_objects)

#             # Record the history
#             record_history(request, app_name, model_name, obj_live.pk)

#             # Optionally delete the record from the temporary model after moving
#             temp_record.delete()
#             return True
#         else:
#             # Create a new record
#             live_record = live_model.objects.create(**fields_and_values)

#             # Set ManyToManyField relationships
#             for m2m_field, value in many_to_many_values.items():
#                 related_manager = getattr(live_record, m2m_field)
               
#                 related_objects = (
#                     related_manager.model.objects.filter(code__in=value)
#                     if 'code' in [field.name for field in related_manager.model._meta.fields]
#                     else related_manager.model.objects.filter(id__in=value)
#                 )
#                 related_manager.set(related_objects)

#             # Record the history
#             record_history(request, app_name, model_name, live_record.pk)

#             # Optionally delete the record from the temporary model after moving
#             temp_record.delete()
#             return True

#     except temp_model.DoesNotExist:
#         print('move_record_temp_to_live raised error: record not found')
#         return False
#     except Exception as error:
#         print('move_record_temp_to_live move_record_123_temp_to_live function raised an error:', error)
#         return False



# def move_record_temp_to_live_for_multivalue(request,app_name,main_model_name, record_id, sub_models_name, field_name, exclude_fields=['status', 'notes']):
#     """
#     Moves a specific record from a temporary model to a live model and deletes the temp record.

#     Args:
#         temp_model_name (str): The name of the temporary model from which records are to be moved.
#         live_model_name (str): The name of the live model where the record should be moved.
#         history_model_name (str): The name of the history model where the history should be recorded.
#         record_id (int): The primary key of the record to be moved.
#         exclude_fields (list): A list of field names to exclude from the copy operation.

#     Returns:
#         bool: True if the operation was successful, False otherwise.

#     Raises:
#         Exception: Any error encountered during the process is caught and logged.
#     """
#     try:
#         # Dynamically retrieve the models using Django's apps registry
#         temp_model = apps.get_model(app_name, f'{main_model_name}Temp')
#         live_model = apps.get_model(app_name, f'{main_model_name}Live')

#         # Fetch the specific record by primary key from the temporary model
#         temp_record = temp_model.objects.get(pk=record_id)

#         # Create a new record in the live model, copying all fields except the primary key and excluded fields
#         fields_and_values = {
#             field.name: getattr(temp_record, field.name)
#             for field in temp_record._meta.fields
#             if field.name not in exclude_fields
#         }
        
#         obj_live = live_model.objects.filter(pk=record_id).first()
#         if obj_live:
#             # Update the existing record
#             for field, value in fields_and_values.items():
#                 setattr(obj_live, field, value)
#             obj_live.save()
#             # Record the history
#             record_history(request,app_name,main_model_name, obj_live.pk)

#             # Optionally delete the record from the temporary model after moving
            
#             main_id=obj_live.pk
#             # return True
#         else:
#             live_record = live_model.objects.create(**fields_and_values)
#             # Record the history
#             record_history(request,app_name,main_model_name, live_record.pk)
#             main_id=live_record.pk

#             # Optionally delete the record from the temporary model after moving
#             # temp_record.delete()

#         for sub_module in sub_models_name:
    
#             temp_model = apps.get_model(app_name, f'{sub_module}Temp')
       
#             live_model = apps.get_model(app_name, f'{sub_module}Live')
      

#             # Fetch the specific record by primary key from the temporary model
#             filter_filter = {
#                 f'{field_name}_id' : main_id
#             }
           
#             sub_temp_records = temp_model.objects.filter(**filter_filter)
         
#             for sub_temp_record in sub_temp_records:

#                 # Create a new record in the live model, copying all fields except the primary key and excluded fields
#                 sub_fields_and_values = {
#                     field.name: getattr(sub_temp_record, field.name)
#                     for field in sub_temp_record._meta.fields
#                     if field.name not in exclude_fields
#                 }
#                 sub_fields_and_values[f'{field_name}_id']=main_id
#                 del sub_fields_and_values[f"{field_name}"]
               
#                 sub_obj_live = live_model.objects.filter(pk=record_id).first()
#                 if sub_obj_live:
#                     # Update the existing record
#                     for field, value in sub_fields_and_values.items():
#                         setattr(sub_obj_live, field, value)
#                     sub_obj_live.save()
#                     # Record the history
#                     record_history(request,app_name,sub_module, sub_obj_live.pk)

#                     # Optionally delete the record from the temporary model after moving
#                     sub_temp_record.delete()
#                     # return True
#                 else:
#                     live_record = live_model.objects.create(**sub_fields_and_values)
#                     # Record the history
#                     record_history(request,app_name,sub_module, live_record.pk)

#                     # Optionally delete the record from the temporary model after moving
#                     sub_temp_record.delete()
#         temp_record.delete()
#         return True
#     except temp_model.DoesNotExist:
#         print('move_record_temp_to_live raised error: record not found')
#         return False
#     except Exception as error:
#         print('move_record_temp_to_live function raised an error:', error)
#         return False



def move_record_temp_to_live_for_multivalue(request,app_name,main_model_name, record_id, sub_models_name, field_name, exclude_fields=['status', 'notes','record_type']):
    print("app_name56789o",app_name,record_id,sub_models_name,field_name)
    """
    Moves a specific record from a temporary model to a live model and deletes the temp record.

    Args:
        temp_model_name (str): The name of the temporary model from which records are to be moved.
        live_model_name (str): The name of the live model where the record should be moved.
        history_model_name (str): The name of the history model where the history should be recorded.
        record_id (int): The primary key of the record to be moved.
        exclude_fields (list): A list of field names to exclude from the copy operation.

    Returns:
        bool: True if the operation was successful, False otherwise.

    Raises:
        Exception: Any error encountered during the process is caught and logged.
    """
    print("main_model_name456789",main_model_name)
    try:
        # Dynamically retrieve the models using Django's apps registry
        temp_model = apps.get_model(app_name, f'{main_model_name}Temp')
        print("temp_model34567i",temp_model)
        live_model = apps.get_model(app_name, f'{main_model_name}Live')

        # Fetch the specific record by primary key from the temporary model
        temp_record = temp_model.objects.get(pk=record_id)
        print("temp_record345678",temp_record)
        # # Create a new record in the live model, copying all fields except the primary key and excluded fields
        # fields_and_values = {
        #     field.name: getattr(temp_record, field.name)
        #     for field in temp_record._meta.fields
        #         if field.name not in exclude_fields
        # }
                # Exclude fields while preparing the fields_and_values dictionary
        fields_and_values = {}
        for field in temp_record._meta.fields:
            print("field4567",field.name)
            if field.name not in exclude_fields:
                fields_and_values[field.name] = getattr(temp_record, field.name)

        print("fields_and_valuesrtyui:", fields_and_values)

        obj_live = live_model.objects.filter(pk=record_id).first()
        print("obj_live567890op",obj_live)
        if obj_live:
            # Update the existing record
            for field, value in fields_and_values.items():
                setattr(obj_live, field, value)
            obj_live.save()
            # Record the history
            record_history(request,app_name,main_model_name, obj_live.pk)

            # Optionally delete the record from the temporary model after moving
            
            main_id=obj_live.pk
            # return True
        else:
            live_record = live_model.objects.create(**fields_and_values)
            # Record the history
            record_history(request,app_name,main_model_name, live_record.pk)
            main_id=live_record.pk

            # Optionally delete the record from the temporary model after moving
            # temp_record.delete()
        
        for sub_module in sub_models_name:
            print("sub_module4567",sub_module)
            temp_model = apps.get_model(app_name, f'{sub_module}Temp')
       
            live_model = apps.get_model(app_name, f'{sub_module}Live')
      

            # Fetch the specific record by primary key from the temporary model
            filter_filter = {
                f'{field_name}_id' : main_id
            }
            print('filter_filter',filter_filter)
            sub_temp_records = temp_model.objects.filter(**filter_filter)
            print('sub_temp_records',sub_temp_records)
            for sub_temp_record in sub_temp_records:
                print('sub_temp_record',sub_temp_record)
                # Create a new record in the live model, copying all fields except the primary key and excluded fields
                sub_fields_and_values = {
                    field.name: getattr(sub_temp_record, field.name)
                    for field in sub_temp_record._meta.fields
                    if field.name not in exclude_fields
                }
                sub_fields_and_values[f'{field_name}_id']=main_id
                del sub_fields_and_values[f"{field_name}"]
               # Dynamically construct the filter keyword
                filter_kwargs = {f"{field_name}_id": record_id}
                sub_obj_live = live_model.objects.filter(**filter_kwargs).first()
                print('sub_obj_live',sub_obj_live)
                if sub_obj_live:
                    # Update the existing record
                    for field, value in sub_fields_and_values.items():
                        setattr(sub_obj_live, field, value)
                    sub_obj_live.save()
                    # Record the history
                    record_history(request,app_name,sub_module, sub_obj_live.pk)

                    # Optionally delete the record from the temporary model after moving
                    sub_temp_record.delete()
                    # return True
                else:
                    live_record = live_model.objects.create(**sub_fields_and_values)
                    print('live_record',live_record)
                    # Record the history
                    record_history(request,app_name,sub_module, live_record.pk)

                    # Optionally delete the record from the temporary model after moving
                    sub_temp_record.delete()
        temp_record.delete()
        return True
    except temp_model.DoesNotExist:
        print('move_record_temp_to_live raised error: record not found')
        return False
    except Exception as error:
        print('move_record_temp_to_live function raised an error:', error)
        return False



def maker_checker_validation(request, model_name, pk):
    """
    Validates if a specific record from a temporary model can be moved to a live model based on maker-checker rules.

    Args:
        request: The HTTP request object containing the user information.
        model_name (str): The base name of the model (without 'Temp' or 'Audit' suffixes).
        pk (int): The primary key of the record in the temporary model to be validated.

    Returns:
        bool: True if the validation is successful and the checker is authorized, False otherwise.

    Raises:
        Exception: Catches and logs any error encountered during the process.
    """
    try:
        # Dynamically retrieve the models using Django's apps registry
        temp_model = apps.get_model('mainapp', f'{model_name}Temp')
        audit_model = apps.get_model('mainapp', f'{model_name}Audit')

        # Fetch the specific record by primary key from the temporary model
        temp_instance = temp_model.objects.filter(pk=pk)
        if not temp_instance.exists():
            print('Data does not exist')
            return False

        temp_obj = temp_instance.last()

        # Fetch the corresponding audit record using a common attribute (e.g., code)
        audit_instance = audit_model.objects.filter(code=temp_obj.code)
        if not audit_instance.exists():
            print('Audit data does not exist')
            return False

        # Retrieve the maker of the specific record
        maker = audit_instance.last().created_by

        # Check if the current user is an authorized checker for the maker
        checkers = MakerCheckerMapping.objects.filter(maker=maker, checker=request.user)
        if checkers.exists():
            return True
        else:
            print("Checker does not exist for this user")
            return False

    except ObjectDoesNotExist as e:
        print(f"ObjectDoesNotExist error: {e}")
        return False
    except Exception as error:
        print(f'maker_checker_validation function raised an error: {error}')
        return False


def checker_temp_records(request, model_name):
    """
    Validates if specific records from a temporary model can be moved to a live model based on maker-checker rules.

    Args:
        request: The HTTP request object containing the user information.
        model_name (str): The base name of the model (without 'Temp' or 'Audit' suffixes).

    Returns:
        bool: True if the validation is successful and the checker is authorized, False otherwise.

    Raises:
        Exception: Catches and logs any error encountered during the process.
    """
    try:
        # Dynamically retrieve the models using Django's apps registry
        temp_model = apps.get_model('mainapp', f'{model_name}Temp')
        audit_model = apps.get_model('mainapp', f'{model_name}Audit')

        # Fetch all codes from the temporary model
        temp_model_codes = temp_model.objects.values_list('code', flat=True)

        # Fetch audit records created by the current user with matching codes
        audit_instance_codes = audit_model.objects.filter(code__in=temp_model_codes,
                                                          created_by=request.user).values_list('code', flat=True)
  
        # Check if there are any matching records
        if temp_model.objects.filter(code__in=audit_instance_codes).exists():
            return True
        else:
            return False

    except ObjectDoesNotExist as e:
        print(f"ObjectDoesNotExist error: {e}")
        return False
    except Exception as error:
        print(f'checker_temp_records function raised an error: {error}')
        return False


def generate_custom_record_id(record_pk):
    # Get the current datetime
    now = datetime.datetime.now()

    # Convert to milliseconds since epoch
    current_time_millis = int(now.timestamp() * 1000)

    # Create the custom ID
    custom_record_id = f"{str(record_pk)}*{current_time_millis}"

    return custom_record_id


def self_authorization(request,app_name,model_name, record_id,type, exclude_fields=['status', 'notes','record_type']):
    """
    Moves a specific record from a temporary model to a live model and deletes the temp record.

    Args:
        temp_model_name (str): The name of the temporary model from which records are to be moved.
        live_model_name (str): The name of the live model where the record should be moved.
        history_model_name (str): The name of the history model where the history should to recorded.
        record_id (int): The primary key of the record to be moved.

    Returns:
        bool: True if the operation was successful, False otherwise.

    Raises:
        Exception: Any error encountered during the process is caught and logged.
    """
    try:
        model_reg = ModelRegistration.objects.filter(model_name=model_name).last()
        if model_reg:
            model=WorkflowMapping.objects.get(workflow_type=type,table_name=model_reg)
            if model.self_authorized:
                move_temp_live = move_record_temp_to_live(request,app_name,model_name,record_id,exclude_fields)
                return move_temp_live
           
            # model=WorkflowMapping.objects.get(workflow_type='update',table_name=model_reg)
            # if model.self_authorized:
            #     move_temp_live = move_record_temp_to_live(request,app_name,model_name, record_id, exclude_fields)
            #     return move_temp_live
            return True
        else:
            print("Model is not register")
            return False
    except Exception as error:
        print('move_record_temp_to_live in self authorization function raised an error:', error)
        return False

def self_authorization_for_multivalue(request,app_name,model_name, record_id,type, sub_models_name, field_name, exclude_fields=['status', 'notes']):
    """
    Moves a specific record from a temporary model to a live model and deletes the temp record.

    Args:
        temp_model_name (str): The name of the temporary model from which records are to be moved.
        live_model_name (str): The name of the live model where the record should be moved.
        history_model_name (str): The name of the history model where the history should to recorded.
        record_id (int): The primary key of the record to be moved.

    Returns:
        bool: True if the operation was successful, False otherwise.

    Raises:
        Exception: Any error encountered during the process is caught and logged.
    """
    try:
        model_reg = ModelRegistration.objects.filter(model_name=model_name).last()
        if model_reg:
            model=WorkflowMapping.objects.get(workflow_type=type,table_name=model_reg)
            if model.self_authorized:
                move_temp_live = move_record_temp_to_live_for_multivalue(request,app_name,model_name, record_id, sub_models_name, field_name, exclude_fields)
                return move_temp_live
           
            # model=WorkflowMapping.objects.get(workflow_type='update',table_name=model_reg)
            # if model.self_authorized:
            #     move_temp_live = move_record_temp_to_live_for_multivalue(request,app_name,model_name, record_id, sub_models_name, field_name, exclude_fields)
            #     return move_temp_live
            return True
        else:
            print("Model is not register")
            return False
    except Exception as error:
        print('move_record_temp_to_live function raised an error:', error)
        return False

def delete_record(request,app_name, model_name, pk):
    live_model = apps.get_model(app_name, f'{model_name}Live')
    live_record = live_model.objects.filter(pk=pk).last()
    if live_record:
        live_record.is_deactivate = True
        live_record.save()
        history = record_history(request,app_name,model_name, pk)
       
        if history:
            return True
        else:
            return False
    else:
        return False


def authorize_request(table_name_id, record_id, sender_user_id, approval_user_id,type=None,next_approval_user=None):
    try:
   
        obj = AuthorizeRequest(
            table_name_id=str(table_name_id),
            record_id=str(record_id),
            sender_user_id=str(sender_user_id),
            approval_user_id=str(approval_user_id),
            next_approval_user_id=next_approval_user if next_approval_user is None else str(next_approval_user),
            workflow_type=type if type is None else str(type)
        )
        obj.save()
        return True
    except Exception as error:
        print('new_authorize_request function raised error ', error)
        return False


def get_record_for_authorize(user_id):
    try:
        obj = AuthorizeRequest.objects.filter(
            Q(approval_user_id=user_id) & Q(is_authorized_return=False)
        )
        
        return obj
    except Exception as error:
        print('new_authorize_request function raised error ', error)
        return False


def convert_query_set_to_dict(obj):
    if obj:
        obj_dict = model_to_dict(obj)  # Convert the model instance to a dictionary
        obj_dict.pop('status', None)
        obj_dict.pop('notes', None)
        obj_dict.pop('is_deactivate', None)
    else:
        obj_dict = {}

    return obj_dict


def get_record_various_models_by_pk(app_name,model_name, record_id,type,output_as_dict=False,model_suffix="Temp"):
    try:
        if type == 'create' or type == 'update':
            temp_model_name = apps.get_model(app_name, f'{model_name}{model_suffix}')

            obj = temp_model_name.objects.get(pk=record_id)
        else:
            temp_model_name = apps.get_model(app_name, f'{model_name}Live')
            obj = temp_model_name.objects.get(pk=record_id)
  
        if output_as_dict:
            query_set_dict = convert_query_set_to_dict(obj)
            return query_set_dict
        else:
            return obj
    except Exception as error:
        print('get_record_various_models_by_pk ', error)
        return False


def delegate_users(user_id, table_name, record_id):
    try:
        obj = DelegateRecords(
            custom_record_id=generate_custom_record_id(record_id),
            table_name_id=table_name,
            delegate_to_id=user_id
        )
        obj.save()
        return True
    except Exception as error:
        print('Error ', error)
        return False

def is_have_permission(request,app_name,model_name,record_id):
    try:
        delegate = DelegateRecords.objects.filter(custom_record_id__startswith=record_id,table_name__model_name=model_name)
        if delegate.exists():
            user = delegate.last().delegate_to
        else:
            audit_model_name = apps.get_model(app_name, f'{model_name}Audit')
            query_set_dict = audit_model_name.objects.filter(code=record_id)
            if query_set_dict.exists():
                user = query_set_dict.first().created_by
            else:
                return False
        if user == request.user:
            return True
        else:
            return False
    except Exception as error:
        print('error ', error)
        return False
    
def get_temp_record(request,app_name,model_name):
    try:

        temp_model_name = apps.get_model(app_name, f'{model_name}Temp')
        audit_model_name = apps.get_model(app_name, f'{model_name}Audit')
        temp_record = temp_model_name.objects.all()
        code_list=[]
        for data in temp_record:
            audit_records=audit_model_name.objects.filter(code=data.code,status='in_temp').last()
            if audit_records:
                if audit_records.created_by == request.user:
                    code_list.append(data.code)
        temp_records = temp_model_name.objects.filter(code__in=code_list)
        return temp_records
    except Exception as error:
        print(f'get_temp_record getting {error}')
        return False

def model_audit(request,app_name,model_name,record_id,status='in_temp'):
    try:
      
        if status == 'in_temp':
            record = apps.get_model(app_name, f'{model_name}Temp')
        elif status == 'created' or status == 'updated' or status == 'deleted':
            record = apps.get_model(app_name, f'{model_name}Live')
        else:
            return False
        audit_model_name = apps.get_model(app_name, f'{model_name}Audit')
        obj = record.objects.get(pk=record_id)
        exclude_fields=['status','notes','is_deactivate','record_type']
        fields_and_values = {
            field.name: getattr(obj, field.name)
            for field in obj._meta.fields
            if field.name not in exclude_fields
        }
        audit_model_name.objects.create(
            custom_record_id=generate_custom_record_id(record_id),
            created_by=request.user,
            updated_by=request.user,
            **fields_and_values,
            status=status,
        )
        return True
    except Exception as error:
        print(f'get_temp_record getting {error}')
        return False
    

def self_authorization_for_delete(request,app_name,model_name, record_id,type):
    """
    Moves a specific record from a temporary model to a live model and deletes the temp record.

    Args:
        temp_model_name (str): The name of the temporary model from which records are to be moved.
        live_model_name (str): The name of the live model where the record should be moved.
        history_model_name (str): The name of the history model where the history should to recorded.
        record_id (int): The primary key of the record to be moved.

    Returns:
        bool: True if the operation was successful, False otherwise.

    Raises:
        Exception: Any error encountered during the process is caught and logged.
    """
    try:
        model_reg = ModelRegistration.objects.filter(model_name=model_name).last()
        if model_reg:
            model=WorkflowMapping.objects.get(workflow_type=type,table_name=model_reg)
        
            if model.self_authorized:
                obj = delete_record(request,app_name,model_name, record_id)
                return obj
            return True
        else:
            print("Model is not register")
            return False
    except Exception as error:
        print('move_record_temp_to_live delete function raised an error:', error)
        return False



#Create your views here.
def success(msg):
    # Create a dictionary named 'response' with two key-value pairs
    response={
        'status_code':0, # Key 'status_code' with value 0
        'data':msg       # Key 'data' with value 'msg' (the input parameter)
    }
    # Return the 'response' dictionary
    return response

def error(msg):
    # Create a dictionary with error details
    response={
        'status_code':1, # Status code indicating error
        'data':msg  # Error message
    }
    # Return the 'response' dictionary
    return response
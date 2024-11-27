from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import importlib
from .serializers import*
from django.shortcuts import render,redirect
import inspect
from datetime import datetime
from rest_framework import permissions
from user_management.serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import json
from mainapp.scripts import *

# MS setup views
def common_response(status_code=0,message=None):
    response = {    
        'status_code':status_code,
        'data':f"""{message}""",
    }
    return response

def check_ms_id_exists_or_not(ms_id):
    try:   
        obj = MSRegistration.objects.get(mservice_id=ms_id) 
        return 'valid_ms_id'
    except MSRegistration.DoesNotExist:
        print('not exits')
        return common_response(status_code=0,message="Invalid micro service id")
    except Exception as error:
        print('Error',error)
        return common_response(status_code=0,message=error)


def get_module(function_name):
    print('FUNCTION NAME ',function_name)
    module = inspect.getmodule(function_name)
    print('module ',module)
    return module.__name__


def call_all_function(module_name, function_name):
    try:
        # Dynamically import the module containing the function
        module = importlib.import_module(module_name)

        # Get the function object from the module
        function = getattr(module, function_name)

        return function

    except ImportError:
        print(f"Failed to import module: {module_name}")

    except AttributeError:
        print(f"Function not found in module: {function_name}")

    except Exception as e:
        print(f"Error occurred while importing function {function_name} from module {module_name}: {e}")

def check_ms_id_exists_or_not(ms_id):
    try:   
        obj = MSRegistration.objects.get(mservice_id=ms_id) 
        return 'valid_ms_id'
    except MSRegistration.DoesNotExist:
        print('not exits')
        return common_response(status_code=0,message="Invalid micro service id")
    except Exception as error:
        print('Error',error)
        return common_response(status_code=0,message=error)
    
def payload_key_validation(ms_id,payload):
    try:
        obj = MSRegistration.objects.get(mservice_id=ms_id)
        mservice_name = obj.mservice_name
        arguments_list = obj.arguments_list
        payload_key = payload.keys()
        for key in payload_key:
            if key not in arguments_list:
                return False
        else:
            return True                
    except MSRegistration.DoesNotExist:
        return common_response(status_code=0,message='micro services id does not exists')
    
def get_module_msid_wise(ms_id):
    try:
        obj = MsToModuleMapping.objects.get(mservice_id=ms_id)  
        print('obj.module_id.module_name',obj.module_id.module_name)    
        return obj.module_id.module_name     
    except MsToModuleMapping.DoesNotExist:
        return common_response(status_code=0,message='micro services id does not exists')


@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    print('email',email)
    password = request.data.get('password')

    user = authenticate(email=email, password=password)

    if user is not None:
        # Generate tokens using SimpleJWT
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        serializers=UserSerializer(user).data
        # Include user details along with the tokens
        user_data = {
            'user_data': serializers,
            'access_token': access_token,
            'refresh_token': str(refresh)
        }
        
        return Response(user_data)
    else:
        return Response({'error': 'Invalid credentials'}, status=400)



class MSAPIModule(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MSSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializers = MSSerializer(data=request.data)
            if serializers.is_valid():
                ms_id = serializers.data['ms_id']
                ms_payload = serializers.data['ms_payload']
                file = request.data.get('files')
                if file:
                    ms_payload['attachment'] = file
                get_response = check_ms_id_exists_or_not(ms_id)
                get_ms_payload = payload_key_validation(ms_id, ms_payload)
                if get_response == 'valid_ms_id':
                    get_obj = MSRegistration.objects.get(mservice_id=ms_id)
                    ms_function = get_obj.mservice_name
                    get_module_name = get_module_msid_wise(ms_id)
                    my_function = call_all_function(get_module_name, str(ms_function))
                    if my_function:
                        try:
                            fun_response = my_function(**ms_payload)
                            print('fun_response', fun_response)
                            if fun_response['status_code'] == 0:
                                data = fun_response['data']
                                if not isinstance(data, list):
                                    data = [data]
                                return Response(data=data, status=status.HTTP_200_OK)
                            else:
                                return Response(data=fun_response['data'], status=status.HTTP_403_FORBIDDEN)
                        except Exception as error:
                            print('error in function call:', error)
                            return Response({'error': str(error)}, status=status.HTTP_404_NOT_FOUND)
                    else:
                        print('Function Import Error')
                        return Response({'error': 'Function Import Error'}, status=status.HTTP_404_NOT_FOUND)
                else:
                    print('get_response', get_response)
                    return Response({'error': get_response}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print('error in main exception:', error)
            return Response({'error': str(error)}, status=status.HTTP_404_NOT_FOUND)

def success_page(request):
    return render(request,'success.html')

def app_and_model_registration(request):
    try:
        config_path='config/model_config.json'
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
            app, model_instances = save_app_and_models(config)
        return redirect('success_page')
    except Exception as errors:
        print('app_and_model_registration',errors)


def save_app_and_models(data):
    """
    Save AppRegistration and ModelRegistration from a dictionary.

    :param data: Dictionary containing app and model data
    :type data: dict
    :return: Tuple of (app_instance, list of model_instances)
    """
    # Extract and save AppRegistration
    app_data = data.get('app_registration', {})
    app_name = app_data.get('app_name')
    
    if not app_name:
        raise ValueError("App name is required in app_registration data")
    
    app, created = AppRegistration.objects.get_or_create(app_name=app_name)
    
    # Extract and save ModelRegistrations
    model_data_list = data.get('model_registrations', [])
    model_instances = []
    
    for model_data in model_data_list:
        model_name = model_data.get('model_name')
        self_authorized = model_data.get('self_authorized', False)
        same_user_authorized = model_data.get('same_user_authorized', False)
        #send_to_authorized = model_data.get('send_to_authorized', False)

        if model_name:
            if not ModelRegistration.objects.filter(app_name=app,model_name=model_name).exists():
                model_instance = ModelRegistration(
                    app_name=app,
                    model_name=model_name,
                )
                model_instance.save()
                model_instances.append(model_instance)
                create=workflow_mapping(model_instance,self_authorized,same_user_authorized,workflow_type='create')

                update= workflow_mapping(model_instance,self_authorized,same_user_authorized,workflow_type='update')
              
                delete= workflow_mapping(model_instance,self_authorized,same_user_authorized,workflow_type='delete')
                
        else:
            raise ValueError("Model name is required in model_registrations data")

    return app, model_instances


def workflow_mapping(model_instance,self_authorized,same_user_authorized,workflow_type):
    try:
        instance=WorkflowMapping.objects.create(
        table_name=model_instance,
        self_authorized=self_authorized,
        same_user_authorized=same_user_authorized,
        workflow_type=workflow_type
        )
        return success(f'{instance} Sucessfully Saved')

    except ModelRegistration.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")
    

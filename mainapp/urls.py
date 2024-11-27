from django.urls import path
from .views import *

urlpatterns = [
    path("micro-service/",MSAPIModule.as_view(), name="MS"),
    path('',app_and_model_registration,name='function_setup'),
    path('success/',success_page,name='success_page')
]
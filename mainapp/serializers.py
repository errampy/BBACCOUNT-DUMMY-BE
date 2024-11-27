from rest_framework import serializers
from .models import *

#  ms setup serializer
class MSSerializer(serializers.Serializer):
    ms_id = serializers.CharField(max_length=100)
    ms_payload = serializers.JSONField(initial=dict)


class AuthorizeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorizeRequest
        fields = "__all__"

  
class ModelRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelRegistration
        fields = "__all__"
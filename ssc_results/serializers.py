from rest_framework import serializers
from .models import SSCResult

class SSCResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SSCResult
        fields = '__all__'  # Return all fields




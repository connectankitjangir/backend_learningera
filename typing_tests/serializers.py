from rest_framework import serializers
from .models import TypingPassage

class TypingPassageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypingPassage
        fields = '__all__'


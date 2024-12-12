#create serializers for answer key
from rest_framework import serializers
from .models import answer_key_generator,original_candidates_data

class AnswerKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = answer_key_generator
        fields = ['button_name']

class OriginalCandidatesDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = original_candidates_data
        fields = '__all__'
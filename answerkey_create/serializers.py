#create serializers for answer key
from rest_framework import serializers
from .models import answer_key_generator,original_candidates_data,ssc_cgl_2024_answerkey

class AnswerKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = answer_key_generator
        fields = ['button_name']

class OriginalCandidatesDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = original_candidates_data
        fields = '__all__'


class SSC_CGL_2024_AnswerKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = ssc_cgl_2024_answerkey
        fields = '__all__'




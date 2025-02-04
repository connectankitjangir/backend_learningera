from rest_framework import serializers
from .models import exam_review, exam_review_store_data

class ExamReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = exam_review
        fields = '__all__'

class ExamReviewStoreDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = exam_review_store_data
        fields = '__all__'




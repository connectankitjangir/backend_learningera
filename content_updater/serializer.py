from rest_framework import serializers
from .models import news_bar, Feedback
class NewsBarSerializer(serializers.ModelSerializer):
    class Meta:
        model = news_bar
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'


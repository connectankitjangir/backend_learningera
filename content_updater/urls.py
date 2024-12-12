from django.urls import path
from . import views
from .serializer import NewsBarSerializer, FeedbackSerializer
urlpatterns = [
    path('api/newsbar/', views.news_bar_list, name='news_bar_list'),
    path('api/feedback/', views.feedback_list, name='feedback_list'),
    # path('feedback/', views.feedback, name='feedback'),
]

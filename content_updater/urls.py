from django.urls import path
from . import views
from .serializer import NewsBarSerializer, FeedbackSerializer
urlpatterns = [
    path('newsbar/', views.news_bar_list, name='news_bar_list'),
    path('feedback/', views.feedback_list, name='feedback_list'),
    # path('feedback/', views.feedback, name='feedback'),
]

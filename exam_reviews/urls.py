from . import views
from django.urls import path

urlpatterns = [
    path('', views.ExamReviewAPIView.as_view(), name='exam_review_api'),
    path('data/', views.ExamReviewStoreDataAPIView.as_view(), name='exam_review_store_data_api'),
    # path('<str:url_slug>/', views.exam_review_page, name='exam_review'),
]
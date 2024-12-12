
from django.urls import path
from . import views

urlpatterns = [
    path('', views.AnswerKeyGeneratorAPIView.as_view(), name='answer_key_generator_api'),
    path('calculate/', views.FormAPIView.as_view(), name='answerkey form'),
    path('result/', views.ResultAPIView.as_view(), name='result'),
    # path('<str:url_slug>', views.form, name='answerkey_form'),
    # path('<str:url_slug>/result/', views.result, name='result'),
    # path('answerkey/<str:url_slug>', views.form, name='answerkey_form'),
    # path('answerkey/<str:url_slug>/result/', views.result, name='result'),
    # path('fetch-questions/', views.fetch_questions, name='fetch_questions'),
    # path('ssc-cgl-2024-tier-1-candidate-form/', views.ssc_cgl_2024_tier_1_candidate_form, name='ssc_cgl_2024_tier_1_candidate_form'),
    # path('ssc-mts-2024-tier-1-candidate-form/', views.ssc_mts_2024_tier_1_candidate_form, name='ssc_mts_2024_tier_1_candidate_form'),
]
# Create your views here.
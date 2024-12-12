# typing_tests/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.typing_home, name='typing_home'),
    
    path('test/<int:passage_id>/', views.typing_test, name='typing_test'),
    path('result/<int:passage_id>/', views.typing_result, name='typing_result'),
]

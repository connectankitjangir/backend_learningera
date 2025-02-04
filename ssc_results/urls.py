from django.urls import path
from .views import SSCResultPostView

urlpatterns = [
    path('ssc-cgl-2024/', SSCResultPostView.as_view(), name='ssc-result-post'),
 
]

"""
URL configuration for learningera project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('ajhm/', admin.site.urls),
    # path('', views.home, name='home'),
    # path('aboutus/', views.aboutus, name='aboutus'),
    path('answerkey/', include('answerkey_create.urls')),
    # path('marks-calculator/', include('answerkey_create.urls')),
    path('exam-review/', include('exam_reviews.urls')),
    path('ssc-results/', include('ssc_results.urls')),
    path('typing_tests/', include('typing_tests.urls')),
    # path('testseries/', include('testseries.urls')),
    #define quiz
    # path('quizzes/', include('quizzes.urls')),


   

    path('content-updater/', include('content_updater.urls')),
   
]

if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

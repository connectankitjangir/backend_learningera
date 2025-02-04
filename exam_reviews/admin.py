from django.contrib import admin
from .models import exam_review, exam_review_store_data

# Register your models here.
admin.site.register(exam_review)
admin.site.register(exam_review_store_data)

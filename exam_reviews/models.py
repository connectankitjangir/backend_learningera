from django.db import models

# Create your models here.
class exam_review(models.Model):
    button_name = models.CharField(max_length=200)
    exam_review_order = models.IntegerField(default=0)
    
    exam_days = models.JSONField(default=["09-09-2024", "10-09-2024", "11-09-2024"])
    exam_shifts = models.IntegerField(default=1)
    gender = models.BooleanField(default=False)
    category = models.BooleanField(default=False)
    english_attempts = models.BooleanField(default=False)
    maths_attempts = models.BooleanField(default=False)
    reasoning_attempts = models.BooleanField(default=False)
    gk_attempts = models.BooleanField(default=False)
    computer_attempts = models.BooleanField(default=False)
    exam_review = models.BooleanField(default=False)
    
    
    
    def __str__(self):
        return self.button_name
    
class exam_review_store_data(models.Model):
    exam_review = models.ForeignKey(exam_review, on_delete=models.CASCADE)
    exam_day = models.CharField(max_length=200, null=True, blank=True)
    exam_shift = models.IntegerField(default=0, null=True, blank=True)
    #gender choise male female other
    
    gender = models.CharField(max_length=50, null=True, blank=True)
    #category choise
    
    category = models.CharField(max_length=50, null=True, blank=True)
    english_attempts = models.CharField(max_length=50, null=True, blank=True)
    maths_attempts = models.CharField(max_length=50, null=True, blank=True)
    reasoning_attempts = models.CharField(max_length=50, null=True, blank=True)
    gk_attempts = models.CharField(max_length=50, null=True, blank=True)
    computer_attempts = models.CharField(max_length=50, null=True, blank=True)
    exam_review_data = models.TextField(default="", null=True, blank=True)


from django.db import models

# Create your models here.
from django.db import models

class SSCResult(models.Model):
    # Candidate Details
    roll_number = models.CharField(max_length=20, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    cat1 = models.CharField(max_length=50, blank=True, null=True)
    cat2 = models.CharField(max_length=50, blank=True, null=True)
    cat3 = models.CharField(max_length=50, blank=True, null=True)
    
    # Exam Details
    exam_date = models.CharField(max_length=100)
    section_1_2_marks = models.CharField(max_length=100)
    section_1_2_marks_with_bonous = models.CharField(max_length=100)
    total_normalized_marks = models.CharField(max_length=100)
    computer_status = models.CharField(max_length=100)


    # All India Rank
    rank_by_section_1_2_marks = models.CharField(max_length=100)
    rank_by_section_1_2_marks_with_bonous = models.CharField(max_length=100)
    rank_by_total_normalized_marks = models.CharField(max_length=100)


   
    
    class Meta:
        managed = False  # Prevents Django from modifying SQLite
        db_table = 'ranked_output'  # Name of table in data.db



from django.db import models
from ckeditor.fields import RichTextField
class answer_key_generator(models.Model):
    button_name = models.CharField(max_length=200)
    url_word = models.CharField(max_length=200, default='digialm')
    # roll_number_element = models.CharField(max_length=200, default='/html/body/div/div[2]/table/tbody/tr[1]/td[2]')
    # exam_name_element = models.CharField(max_length=200, default='/html/body/div/div[2]/table/tbody/tr[6]/td[2]')
    right_exam_name = models.CharField(max_length=200, default='CHSL Exam 2024 Tier I')
    roll_number_name = models.CharField(max_length=200, default='Roll Number')
    exam_name_name = models.CharField(max_length=200, default='Subject')
    candidate_name_name = models.CharField(max_length=200, default='Candidate Name')
    venue_name_name = models.CharField(max_length=200, default='Test Center Name')
    exam_date_name = models.CharField(max_length=200, default='Test Date')
    exam_time_name = models.CharField(max_length=200, default='Test Time')
    # venue_name_element = models.CharField(max_length=200, default='/html/body/div/div[2]/table/tbody/tr[3]/td[2]')
    # exam_date_element = models.CharField(max_length=200, default='/html/body/div/div[2]/table/tbody/tr[4]/td[2]')
    # exam_time_element = models.CharField(max_length=200, default='/html/body/div/div[2]/table/tbody/tr[5]/td[2]')
    # candidate_name_element = models.CharField(max_length=200, default='/html/body/div/div[2]/table/tbody/tr[2]/td[2]')
    
    question_per_subject = models.JSONField(default=[25,25,25,25])
    per_mcq_marks = models.JSONField(default=[2.0,2.0,2.0,2.0])
    wrong_ans_marks = models.JSONField(default=[0.5,0.5,0.5,0.5])
    question_panel_class = models.CharField(max_length=200, default = '//div[contains(@class, "question-pnl")]')
    # bold_text_class = models.CharField(max_length=200, default = './/td[contains(@class, "bold")]')
    # answer_text_index = models.IntegerField(default = 9)
    right_answer_class = models.CharField(max_length=200, default = './/td[contains(@class, "rightAns")]')
    section_class = models.CharField(max_length=200, default = '//div[@class="section-lbl"]//span[@class="bold"]')
    normalization_starting_index = models.IntegerField(default = 0)
    subject_count_in_merit_list = models.JSONField(default=[1,1,1,1])
    # qualifying_marks = models.FloatField(default=20)
    qualifying_percentage = models.JSONField(default={
        'UR': 30,
        'OBC': 25,
        'EWS': 25,
        'SC': 20,
        'ST': 20
    })
    answer_key_order = models.IntegerField(default = 0)
    
class form_video(models.Model):
    answer_key_generator = models.ForeignKey(answer_key_generator, on_delete=models.CASCADE)
    form_video_url = models.CharField(max_length=200)
    form_video_order = models.IntegerField(default = 0)
class exam_details(models.Model):
    answer_key_generator = models.ForeignKey(answer_key_generator, on_delete=models.CASCADE)
    
    exam_description = RichTextField(blank=True, null=True)
    exam_description_order = models.IntegerField(default = 0)
class result_video(models.Model):
    answer_key_generator = models.ForeignKey(answer_key_generator, on_delete=models.CASCADE)
    result_video_url = models.CharField(max_length=200)
    result_video_order = models.IntegerField(default = 0)

class original_candidates_data(models.Model):

    answer_key_generator = models.ForeignKey(answer_key_generator, on_delete=models.CASCADE)
    answer_key_link = models.CharField(max_length=200, unique=True)
    category = models.CharField(max_length=50)
    roll_number = models.CharField(max_length=50, primary_key=True)
    candidate_name = models.CharField(max_length=200)
    venue_name = models.CharField(max_length=200)
    exam_date = models.CharField(max_length=200)
    exam_time = models.CharField(max_length=200)
    total_marks = models.FloatField()
    total_marks_for_merit_list = models.FloatField(default=0)
    section_data = models.JSONField(default=dict)
    wrong_questions = models.TextField(default='' , null=True, blank=True)

    def __str__(self):
        return self.roll_number
    
    class Meta:
        ordering = ['answer_key_generator', 'roll_number']

class raw_marks_candidates_data(models.Model):
    answer_key_generator = models.ForeignKey(answer_key_generator, on_delete=models.CASCADE)
    answer_key_link = models.CharField(max_length=200, unique=True)
    category = models.CharField(max_length=50)
    roll_number = models.CharField(max_length=50, primary_key=True)
    candidate_name = models.CharField(max_length=200)
    venue_name = models.CharField(max_length=200)
    exam_date = models.CharField(max_length=200)
    exam_time = models.CharField(max_length=200)
    total_marks = models.FloatField()
    total_marks_for_merit_list = models.FloatField(default=0)
    section_data = models.JSONField(default=dict)
    overall_rank = models.IntegerField(default=0)
    overall_average = models.FloatField(default=0)
    category_rank = models.IntegerField()
    shift = models.CharField(max_length=200)
    shift_average = models.FloatField()
    shift_rank = models.IntegerField()
    category_average = models.FloatField()
    marks_in_qualifying_subjects = models.FloatField(default=0)
    qualifies = models.BooleanField(default=False)
    wrong_questions = models.TextField(default='' , null=True, blank=True)

class normalized_marks_candidates_data(models.Model):
    answer_key_generator = models.ForeignKey(answer_key_generator, on_delete=models.CASCADE)
    answer_key_link = models.CharField(max_length=200, unique=True)
    category = models.CharField(max_length=50)
    roll_number = models.CharField(max_length=50, primary_key=True)
    candidate_name = models.CharField(max_length=200)
    venue_name = models.CharField(max_length=200)
    exam_date = models.CharField(max_length=200)
    exam_time = models.CharField(max_length=200)
    total_marks = models.FloatField()
    total_marks_for_merit_list = models.FloatField(default=0)
    section_data = models.JSONField(default=dict)
    overall_rank = models.IntegerField(default=0)
    overall_average = models.FloatField(default=0)
    category_rank = models.IntegerField()
    shift = models.CharField(max_length=200)
    shift_average = models.FloatField()
    shift_rank = models.IntegerField()
    category_average = models.FloatField()
    shift_mean = models.FloatField(default=0, null=True, blank=True)
    shift_std = models.FloatField(default=0, null=True, blank=True)
    shift_median = models.FloatField(default=0, null=True, blank=True)
    shift_M_ti = models.FloatField(default=0, null=True, blank=True)
    shift_M_iq = models.FloatField(default=0, null=True, blank=True)
    normalized_marks = models.FloatField(default=0, null=True, blank=True)
    normalized_rank = models.FloatField(default=0, null=True, blank=True)
    normalized_category_rank = models.FloatField(default=0, null=True, blank=True)
    wrong_questions = models.TextField(default='' , null=True, blank=True)



class ssc_cgl_2024_answerkey(models.Model):
    link = models.CharField(max_length=300)
   
    def __str__(self):
        return self.link









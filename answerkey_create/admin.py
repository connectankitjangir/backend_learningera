from django.contrib import admin
from .models import answer_key_generator,form_video,exam_details,result_video,original_candidates_data,raw_marks_candidates_data,normalized_marks_candidates_data
# Register your models here.
class answer_key_generatorAdmin(admin.ModelAdmin):
    list_display = ('button_name', 'right_exam_name')
admin.site.register(answer_key_generator, answer_key_generatorAdmin)
# class answer_key_generatorAdmin(admin.ModelAdmin):
#     list_display = ('button_name','roll_number_element','exam_name_element','right_exam_name','candidate_name_element','venue_name_element','exam_date_element','exam_time_element','question_per_subject','per_mcq_marks','wrong_ans_marks','question_panel_class','bold_text_class','answer_text_index','right_answer_class','section_class','normalization_starting_index','subject_count_in_merit_list','answer_key_order')
# admin.site.register(answer_key_generator, answer_key_generatorAdmin)

class form_videoAdmin(admin.ModelAdmin):
    list_display = ('answer_key_generator','form_video_url','form_video_order')

admin.site.register(form_video, form_videoAdmin)

class exam_detailsAdmin(admin.ModelAdmin):
    list_display = ('answer_key_generator','exam_description','exam_description_order')
admin.site.register(exam_details, exam_detailsAdmin)

class result_videoAdmin(admin.ModelAdmin):
    list_display = ('answer_key_generator','result_video_url','result_video_order')
admin.site.register(result_video, result_videoAdmin)

# class CandidateAdmin(admin.ModelAdmin):
#     list_display = ('exam_day', 'exam_shift', 'gender', 'category', 'english_attempts', 'maths_attempts', 'reasoning_attempts', 'gk_attempts')
#     list_filter = ('gender', 'category', 'exam_shift')
#     search_fields = ('exam_day', 'exam_shift')

# admin.site.register(Candidate, CandidateAdmin)




class original_candidates_dataAdmin(admin.ModelAdmin):
    list_display = ('answer_key_generator','answer_key_link','category','roll_number','candidate_name','venue_name','exam_date','exam_time','total_marks','section_data')
    list_filter = ('answer_key_generator__right_exam_name',)
    search_fields = ('roll_number', 'candidate_name')
admin.site.register(original_candidates_data, original_candidates_dataAdmin)

class raw_marks_candidates_dataAdmin(admin.ModelAdmin):
    list_display = ('answer_key_generator','answer_key_link','category','roll_number','candidate_name','venue_name','exam_date','exam_time','total_marks','section_data','overall_rank','overall_average','category_rank', 'shift','shift_average','shift_rank','category_average')
    list_filter = ('answer_key_generator__right_exam_name', 'shift')
    search_fields = ('roll_number', 'candidate_name')
admin.site.register(raw_marks_candidates_data, raw_marks_candidates_dataAdmin)

class normalized_marks_candidates_dataAdmin(admin.ModelAdmin):
    list_display = ('answer_key_generator','answer_key_link','category','roll_number','candidate_name','venue_name','exam_date','exam_time','total_marks','section_data','overall_rank','overall_average','category_rank', 'shift','shift_average','shift_rank','category_average','shift_mean','shift_std','shift_M_ti','shift_M_iq','normalized_marks','shift_median','normalized_rank','normalized_category_rank')
    list_filter = ('answer_key_generator__right_exam_name', 'shift')
    search_fields = ('roll_number', 'candidate_name')
admin.site.register(normalized_marks_candidates_data, normalized_marks_candidates_dataAdmin)

# from django.contrib import admin
# from django.apps import apps
# from .models import *

# # Get all models from the 'testseries' app
# app_models = apps.get_app_config('answerkey_create').get_models()

# for model in app_models:
#     try:
#         admin.site.register(model)
#     except admin.sites.AlreadyRegistered:
#         pass  # Skip if the model is already registered




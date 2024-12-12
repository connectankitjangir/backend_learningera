# from django.http import HttpResponse
from django.shortcuts import render
from answerkey_create.models import answer_key_generator
from django.core.cache import cache
from content_updater.models import news_bar,our_videos
from examreviws.models import exam_review
# import json

# import requests
# from lxml import etree
# import sqlite3
# import pandas as pd
# import os

# from utils import (
#     fetch_candidates_df,
#     fetch_original_data_df,
#     is_roll_number_exists,
#     is_roll_number_exists_in_normalized_table,
#     calculate_normalized_marks,
#     calculate_rank,
#     calculate_shift_averages_and_ranks,
#     calculate_averages,
#     initialize_db,
#     update_db_with_raw_marks,
#     fetch_normalized_df,
#     calculate_normalized_rank,
#     update_db_with_normalized_marks,
# )



# def home(request):
#     # Try to get the answer key data from the cache
#     answer_key_generatorData = cache.get('answer_key_generatorData')
#     news_barData = cache.get('news_barData')
#     exam_reviewData = cache.get('exam_reviewData')
#     # why_choose_usData = cache.get('why_choose_usData')
#     our_videosData = cache.get('our_videosData')
    
    
#     print('starting point')

#     if not answer_key_generatorData:
#         # If cache is empty, query the database
#         answer_key_generatorData = answer_key_generator.objects.all().order_by('-answer_key_order')
#         news_barData = news_bar.objects.all().order_by('-news_bar_order')
#         exam_reviewData = exam_review.objects.all().order_by('-exam_review_order')
#         # why_choose_usData = why_choose_us.objects.all().order_by('-why_choose_us_order')
#         our_videosData = our_videos.objects.all().order_by('-our_videos_order')
#         # Store the result in cache for 15 minutes (900 seconds)
#         cache.set('answer_key_generatorData', answer_key_generatorData, 900)
#         cache.set('news_barData', news_barData, 900)
#         cache.set('exam_reviewData', exam_reviewData, 900)
#         # cache.set('why_choose_usData', why_choose_usData, 900)
#         cache.set('our_videosData', our_videosData, 900)
#         print('after cache set')

#     # Define other data to be included in the context if needed in the future
#     data = {
#         'answer_key_generatorData': answer_key_generatorData,
#         'news_barData': news_barData,
#         'exam_reviewData': exam_reviewData,
#         # 'why_choose_usData': why_choose_usData,
#         'our_videosData': our_videosData,
#     }

#     # Render the template with the cached data
#     return render(request, 'index.html', data)


# def home(request):
#     # newsData = news.objects.all().order_by('-newsTitle')
#     # featuresData = features.objects.all().order_by('-featureTitle')
#     answer_key_generatorData = answer_key_generator.objects.all().order_by('-answer_key_order')
#     # news_barData = news_bar.objects.all().order_by('-news_bar_order')
#     # why_choose_usData = why_choose_us.objects.all().order_by('-why_choose_us_order')
#     # our_videosData = our_videos.objects.all().order_by('-our_videos_order')
#     data = {
#         # 'featuresData': featuresData,
#         # 'newsData': newsData,
#         'answer_key_generatorData': answer_key_generatorData,
#         # 'news_barData': news_barData,
#         # 'why_choose_usData': why_choose_usData,
#         # 'our_videosData': our_videosData,
#         # 'button_name': examcreatorData.first().button_name if examcreatorData.exists() else None,
#         # 'button_slug': examcreatorData.first().button_name.replace(' ', '-').lower() if examcreatorData.exists() else None
#     }
#     # print(data)
#     return render(request, 'index.html', data)

# def aboutus(request):
#     # about_usData = cache.get('about_usData')
#     # if not about_usData:
#     #     # about_usData = about_us.objects.all().order_by('-about_us_order')
#     #     cache.set('about_usData', about_usData, 900)
#     # # about_usData = about_us.objects.all().order_by('-about_us_order')
#     # # data = {
#     # #     'about_usData': about_usData,
#     # # }
#     return render(request, 'aboutus.html')





















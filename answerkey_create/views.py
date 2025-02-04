from django.http import HttpResponse
from django.shortcuts import render
from answerkey_create.models import answer_key_generator,form_video,exam_details,result_video,original_candidates_data, raw_marks_candidates_data,normalized_marks_candidates_data,ssc_cgl_2024_answerkey
from rest_framework import status
import json
import requests
from lxml import etree
import sqlite3
import pandas as pd
import os
import re
import math

from rest_framework.response import Response
from rest_framework import generics
from .serializers import AnswerKeySerializer, SSC_CGL_2024_AnswerKeySerializer

from utils import (
    fetch_candidates_df,
    fetch_original_data_df,
    is_roll_number_exists,
    is_roll_number_exists_in_normalized_table,
    calculate_normalized_marks,
    calculate_rank,
    calculate_shift_averages_and_ranks,
    calculate_averages,
    initialize_db,
    update_db_with_raw_marks,
    fetch_normalized_df,
    calculate_normalized_rank,
    update_db_with_normalized_marks,
)

def is_roll_number_exists_in_normalized_table(database_path, roll_number):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM normalized WHERE roll_number = ?', (roll_number,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

class SSC_CGL_2024_AnswerKeyAPIView(generics.ListAPIView):
    queryset = ssc_cgl_2024_answerkey.objects.all()
    serializer_class = SSC_CGL_2024_AnswerKeySerializer

    def post(self, request):
        link = request.data.get("link")
        print("link",link)

        ssc_cgl_2024_answerkey.objects.create(link=link)
        return Response({"message": "Answer key submitted successfully"})

class AnswerKeyGeneratorAPIView(generics.ListAPIView):
    queryset = answer_key_generator.objects.all()


    serializer_class = AnswerKeySerializer

    def get(self, request, *args, **kwargs):
        # Try to get cached data
        cache_key = 'answer_key_generator_list'
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            return Response(cached_data)
            
        # If cache miss, get data from database
        response = self.list(request, *args, **kwargs)
        
        # Cache the response data for 15 minutes
        cache.set(cache_key, response.data, timeout=900)
        
        return response


from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.core.cache import cache
from django.http import JsonResponse
import requests
from lxml import etree
import re
import pandas as pd
from answerkey_create.models import (
    answer_key_generator,
    form_video,
    exam_details,
    original_candidates_data,
    raw_marks_candidates_data,
)
from utils import (
    calculate_rank,
    calculate_shift_averages_and_ranks,
    calculate_averages,
)

class FormAPIView(APIView):
    # def get(self, request):
    #     url_slug = request.GET.get('url_slug')
    #     title = url_slug.replace('-', ' ').title() + ' Marks, And Rank Calculator By Learning Era'
    #     parts = re.split(r'(\d{4}.*)', title, maxsplit=1)
    #     first_part = ' '.join(word.upper() for word in parts[0].split())
    #     title = first_part + ' ' + parts[1]
        
    #     answer_key_generator_data = answer_key_generator.objects.filter(
    #         button_name__iexact=url_slug.replace('-', ' ')
    #     ).first()
        
    #     form_video_cache_key = f'form_video_data_{url_slug}'
    #     exam_details_cache_key = f'exam_details_data_{url_slug}'
        
    #     form_video_data = cache.get(form_video_cache_key)
    #     if not form_video_data:
    #         form_video_data = form_video.objects.filter(
    #             answer_key_generator=answer_key_generator_data
    #         ).order_by('-form_video_order')
    #         cache.set(form_video_cache_key, form_video_data, 900)
        
    #     exam_details_data = cache.get(exam_details_cache_key)
    #     if not exam_details_data:
    #         exam_details_data = exam_details.objects.filter(
    #             answer_key_generator=answer_key_generator_data
    #         ).order_by('-exam_description_order')
    #         cache.set(exam_details_cache_key, exam_details_data, 900)
        
    #     content = {}
    #     data = {
    #         'content': content,
    #         'form_video_data': form_video_data,
    #         'exam_details_data': exam_details_data,
    #         'title': title
    #     }
    #     return Response(data)

    def post(self, request):
        #print all data received via post request
        print("request",request.data)

        url_slug = request.data.get('url_slug')
        wrong_questions = request.data.get('wrongQuestions')
        print("wrong_questions",wrong_questions)
        print("url_slug",url_slug)
        title = url_slug.replace('-', ' ').title() + ' Marks, And Rank Calculator By Learning Era'
        parts = re.split(r'(\d{4}.*)', title, maxsplit=1)
        first_part = ' '.join(word.upper() for word in parts[0].split())
        title = first_part + ' ' + parts[1]
        print("title",title)
        answer_key_generator_data = answer_key_generator.objects.filter(
            button_name__iexact=url_slug.replace('-', ' ')
        ).first()
        print("answer_key_generator_data",answer_key_generator_data)
        # print all fields of answer_key_generator_data
        print("answer_key_generator_data fields and values:", {field.name: getattr(answer_key_generator_data, field.name) for field in answer_key_generator_data._meta.fields})

        form_video_cache_key = f'form_video_data_{url_slug}'
        exam_details_cache_key = f'exam_details_data_{url_slug}'

        form_video_data = cache.get(form_video_cache_key)
        if not form_video_data:
            form_video_data = form_video.objects.filter(
                answer_key_generator=answer_key_generator_data
            ).order_by('-form_video_order')
            cache.set(form_video_cache_key, form_video_data, 900)

        exam_details_data = cache.get(exam_details_cache_key)
        if not exam_details_data:
            exam_details_data = exam_details.objects.filter(
                answer_key_generator=answer_key_generator_data
            ).order_by('-exam_description_order')
            cache.set(exam_details_cache_key, exam_details_data, 900)

        content = {}
        outside_route = True

        answer_key_link = request.data.get('answerKeyLink')
        category = request.data.get('category')
        print("category",category)
        print("answer_key_link",answer_key_link)

        if not (answer_key_generator_data.url_word in answer_key_link):
            content['Error'] = 'Invalid answer key link'
            print("content",content)
            return JsonResponse({'content': content, 'title': title})

        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            print("headers",headers)
            response = requests.get(answer_key_link, headers=headers)
            print("response",response)
            response.raise_for_status()
            print("response",response)

            parser = etree.HTMLParser()
            tree = etree.fromstring(response.content, parser)
            tbody = tree.xpath('//tbody')[0]
            roll_number_row = tbody.xpath(f'.//td[contains(., "{answer_key_generator_data.roll_number_name}")]')[0]
            roll_number_value_row = roll_number_row.getnext()
            roll_number = roll_number_value_row.text.strip() if roll_number_value_row is not None else 'Roll Number not found'
            print("roll_number",roll_number)
            exam_name_row = tbody.xpath(f'.//td[contains(., "{answer_key_generator_data.exam_name_name}")]')[0]
            exam_name_value_row = exam_name_row.getnext()
            exam_name = exam_name_value_row.text.strip() if exam_name_value_row is not None else 'Exam Name not found'
            right_exam_name = answer_key_generator_data.right_exam_name
            if right_exam_name.lower() not in exam_name.lower():
                content['Error'] = 'Please enter ' + right_exam_name + ' answer key link'
                return JsonResponse({'content': content, 'title': title})

            section_data = {}
            original_candidates_data_for_exam = original_candidates_data.objects.filter(answer_key_generator=answer_key_generator_data)
            subject_list_in_merit_list = answer_key_generator_data.subject_count_in_merit_list
            if original_candidates_data_for_exam is None or not original_candidates_data_for_exam.filter(roll_number=roll_number).exists():
                candidate_name_row = tbody.xpath(f'.//td[contains(., "{answer_key_generator_data.candidate_name_name}")]')[0]
                candidate_name_value_row = candidate_name_row.getnext()
                candidate_name = candidate_name_value_row.text.strip() if candidate_name_value_row is not None else 'Candidate Name not found'
                venue_name_row = tbody.xpath(f'.//td[contains(., "{answer_key_generator_data.venue_name_name}")]')[0]
                venue_name_value_row = venue_name_row.getnext()
                venue_name = venue_name_value_row.text.strip() if venue_name_value_row is not None else 'Venue Name not found'
                exam_date_row = tbody.xpath(f'.//td[contains(., "{answer_key_generator_data.exam_date_name}")]')[0]
                exam_date_value_row = exam_date_row.getnext()
                exam_date = exam_date_value_row.text.strip() if exam_date_value_row is not None else 'Exam Date not found'
                exam_date = exam_date.replace('/', '-') if exam_date else 'Exam Date not found'
                exam_time_row = tbody.xpath(f'.//td[contains(., "{answer_key_generator_data.exam_time_name}")]')[0]
                exam_time_value_row = exam_time_row.getnext()
                exam_time = exam_time_value_row.text.strip() if exam_time_value_row is not None else 'Exam Time not found'
                questions_per_subject = answer_key_generator_data.question_per_subject
                per_mcq_marks = answer_key_generator_data.per_mcq_marks
                wrong_ans_marks = answer_key_generator_data.wrong_ans_marks
                sections_element = tree.xpath(answer_key_generator_data.section_class)
                question_panels = tree.xpath(answer_key_generator_data.question_panel_class)
                total_marks = 0
                total_not_attempted = 0
                total_right = 0
                total_wrong = 0
                total_marks_for_merit_list = 0
                total_not_attempted_for_merit_list = 0
                total_right_for_merit_list = 0
                total_wrong_for_merit_list = 0
                start_question_panel = 0
                for index, subject in enumerate(questions_per_subject):
                    section_right = 0
                    section_not_attempted = 0
                    section_name = sections_element[index].text.strip()
                    for question in range(start_question_panel, subject+start_question_panel):
                        right = 0
                        not_attempted = 0
                        question_panel = question_panels[question]
                        choosen_option = question_panel.xpath('.//td[contains(text(), "Chosen Option")]')
                        answer_text_data = choosen_option[0].getnext()
                        answer_text = answer_text_data.text.strip()
                        if '-' in answer_text:
                            not_attempted += 1
                        else:
                            try:
                                correct_answer = question_panel.xpath(f'{answer_key_generator_data.right_answer_class}/text()')[0][0]
                                if correct_answer == answer_text:
                                    right += 1
                            except Exception:
                                pass
                        section_not_attempted += not_attempted
                        section_right += right
                    answer_text = ""
                    correct_answer = ""
                    start_question_panel += subject
                    section_total = questions_per_subject[index]
                    section_wrong = section_total - section_right - section_not_attempted
                    section_marks = section_right * per_mcq_marks[index] - section_wrong * wrong_ans_marks[index]
                    total_marks += section_marks
                    total_wrong += section_wrong
                    total_not_attempted += section_not_attempted
                    total_right += section_right
                    if subject_list_in_merit_list[index] > 0:
                        total_marks_for_merit_list += section_marks
                        total_not_attempted_for_merit_list += section_not_attempted
                        total_right_for_merit_list += section_right
                        total_wrong_for_merit_list += section_wrong
                    if index == 0:  
                        section_data[index] = [section_name, section_not_attempted, section_right,  section_wrong, section_marks]
                    else:
                        section_data.update({index: [section_name, section_not_attempted, section_right, section_wrong, section_marks]})
                section_data['Total'] = ['Total', total_not_attempted, total_right, total_wrong, total_marks]
                section_data['Total Merit List'] = ['Total Merit List', total_not_attempted_for_merit_list, total_right_for_merit_list, total_wrong_for_merit_list, total_marks_for_merit_list]
                total_questions = sum(questions_per_subject)
                total_questions_for_merit_list = total_right_for_merit_list + total_not_attempted_for_merit_list + total_wrong_for_merit_list
                
                original_candidate = original_candidates_data(
                    answer_key_generator=answer_key_generator_data,
                    answer_key_link=answer_key_link,
                    category=category,
                    roll_number=roll_number,
                    candidate_name=candidate_name,
                    venue_name=venue_name,
                    exam_date=exam_date,
                    exam_time=exam_time,
                    total_marks=total_marks,
                    total_marks_for_merit_list=total_marks_for_merit_list,
                    section_data=section_data,
                    wrong_questions=wrong_questions
                )
                original_candidate.save()
                print('category after save',category)

            
                maximum_marks_in_qualifying_subjects = 0
                for index, maximum_questions_in_current_subject in enumerate(questions_per_subject):
                    if subject_list_in_merit_list[index] < 1:
                        maximum_marks_in_qualifying_subjects += maximum_questions_in_current_subject * per_mcq_marks[index]

                df = pd.DataFrame(list(original_candidates_data.objects.filter(answer_key_generator=answer_key_generator_data).values()))
                print('category after df',category)
                df['marks_in_qualifying_subjects'] = df['total_marks'] - df['total_marks_for_merit_list']
                print('category after marks_in_qualifying_subjects',category)
                qualifying_marks_dict = {}
                for category_name, percentage in answer_key_generator_data.qualifying_percentage.items():
                    qualifying_marks = maximum_marks_in_qualifying_subjects * percentage / 100
                    qualifying_marks_dict[category_name] = qualifying_marks
                print('category after qualifying_marks_dict',category)
                df['qualifies'] = df.apply(lambda x: x['marks_in_qualifying_subjects'] >= qualifying_marks_dict.get(x['category'], 0), axis=1)
                print('category after qualifies',category)

                if total_marks - total_marks_for_merit_list >= qualifying_marks_dict.get(category, 0):
                    overall_rank, category_rank = calculate_rank(df, roll_number, category)
                    
                    shift_averages, shift_ranks = calculate_shift_averages_and_ranks(df)
                    
                    shift_key = f"{exam_date} {exam_time}"
                    
                    average_marks_for_shift = shift_averages.get(shift_key, 'No data for this shift')
                    
                    shift_rank = shift_ranks.get(roll_number, 'No data for this shift')
                    
                    overall_average, category_averages, total_candidates = calculate_averages(df)
                    
                    df['overall_average'] = overall_average
                    print("df before delete",df)

                    raw_marks_candidates_data.objects.filter(answer_key_generator=answer_key_generator_data).delete()
                    for index, row in df.iterrows():
                        raw_marks_candidates_data.objects.create(
                        answer_key_generator=answer_key_generator_data,
                        answer_key_link=row['answer_key_link'],
                        category=row['category'],
                        roll_number=row['roll_number'],
                        candidate_name=row['candidate_name'],
                        venue_name=row['venue_name'],
                        exam_date=row['exam_date'],
                        exam_time=row['exam_time'],
                        total_marks=row['total_marks'],
                        total_marks_for_merit_list = row['total_marks_for_merit_list'],
                        section_data=row['section_data'],
                        overall_rank=row['overall_rank'],
                        overall_average=row['overall_average'],
                        category_rank=row['category_rank'],
                        shift=row['shift'],
                        shift_average=row['shift_average'],
                        shift_rank=row['shift_rank'],
                        category_average=row['category_average'],
                        marks_in_qualifying_subjects=row['marks_in_qualifying_subjects'],
                        qualifies=row['qualifies'],
                        wrong_questions=row['wrong_questions']
                        )
                else:
                    overall_rank = 'Not Eligible'
                    overall_average = 'Not Eligible'
                    total_candidates = 'Not Eligible'
                    category_rank = 'Not Eligible'
                    category_average = 'Not Eligible'
                    shift_rank = 'Not Eligible'
                    average_marks_for_shift = 'Not Eligible'
                print ('category before try',category)
                try:
                    category_average = category_averages.get(category)
                except:
                    overall_rank = 'Not Eligible'
                    category_average = 'Not Eligible'
            
                content = {
                    'Total Marks': total_marks,
                    'Total Merit List Marks': total_marks_for_merit_list,
                    'Overall Rank': overall_rank*7,
                    'Overall Average': overall_average,
                    'Category Rank': category_rank*7,
                    'Category Average': category_average,
                    'Shift Rank': shift_rank*7,
                    'Average Marks for Shift': average_marks_for_shift
                }
                candidate_data = {
                    'Candidate Name': candidate_name,
                    'Roll Number': roll_number,
                    'Category': category,
                    'Venue Name': venue_name,
                    'Exam Date': exam_date,
                    'Exam Time': exam_time
                }
                # request.session['roll_number'] = roll_number
                # request.session['category'] = category
                # request.session['url_slug'] = url_slug
                data = {
                    'section_data': section_data,
                    'outside_route': outside_route,
                    'content': content,
                    'candidate_data': candidate_data,
                    # 'form_video_data': form_video_data,
                    # 'exam_details_data': exam_details_data,
                    # 'url_slug': url_slug,
                    # 'title': title
                }
                print("data",data)
                return JsonResponse(data)
                
            else:
                try:
                    candidate_row = raw_marks_candidates_data.objects.get(answer_key_generator=answer_key_generator_data, roll_number=roll_number)
                    print("candidate_row",candidate_row)
                    overall_average = candidate_row.overall_average
                    category = candidate_row.category
                    candidate_name = candidate_row.candidate_name
                    venue_name = candidate_row.venue_name
                    exam_date = candidate_row.exam_date
                    exam_time = candidate_row.exam_time
                    total_marks = candidate_row.total_marks
                    total_marks_for_merit_list = candidate_row.total_marks_for_merit_list
                    overall_rank = candidate_row.overall_rank
                    category_rank = candidate_row.category_rank
                    average_marks_for_shift = candidate_row.shift_average
                    shift_rank = candidate_row.shift_rank
                    category_average = candidate_row.category_average
                    section_data = candidate_row.section_data
                except:
                    original_candidates_data_for_exam = original_candidates_data.objects.filter(answer_key_generator=answer_key_generator_data, roll_number=roll_number).first()
                    candidate_name = original_candidates_data_for_exam.candidate_name
                    total_marks = original_candidates_data_for_exam.total_marks
                    total_marks_for_merit_list = original_candidates_data_for_exam.total_marks_for_merit_list
                    venue_name = original_candidates_data_for_exam.venue_name
                    exam_date = original_candidates_data_for_exam.exam_date
                    exam_time = original_candidates_data_for_exam.exam_time
                    category = original_candidates_data_for_exam.category
                    overall_average = 'Not Eligible'
                    category_average = 'Not Eligible'
                    overall_rank = 'Not Eligible'
                    category_rank = 'Not Eligible'
                    average_marks_for_shift = 'Not Eligible'
                    shift_rank = 'Not Eligible'
                    section_data = original_candidates_data_for_exam.section_data
                
                content = {
                    'Total Marks': total_marks,
                    'Total Merit List Marks': total_marks_for_merit_list,
                    'Overall Rank': overall_rank*7,
                    'Overall Average': overall_average,
                    'Category Rank': category_rank*7,
                    'Category Average': category_average,
                    'Shift Rank': shift_rank*7,
                    'Average Marks for Shift': average_marks_for_shift
                }
                candidate_data = {
                    'Candidate Name': candidate_name,
                    'Roll Number': roll_number,
                    'Category': category,
                    'Venue Name': venue_name,
                    'Exam Date': exam_date,
                    'Exam Time': exam_time
                }
                request.session['roll_number'] = roll_number
                request.session['category'] = category
                data = {
                    'section_data': section_data,
                    'outside_route': outside_route,
                    'content': content,
                    'candidate_data': candidate_data,
                    # 'form_video_data': form_video_data,
                    # 'exam_details_data': exam_details_data,
                    # 'url_slug': url_slug,
                    # 'title': title
                }
                print("data",data)
                return JsonResponse(data)

        except requests.RequestException as e:
            content['Error'] = f"An error occurred while fetching the answer key link: {e}"
        except Exception as e:
            content['Error'] = f"An error occurred: {e}"

        data = {
            'content': content,
            'form_video_data': form_video_data,
            'exam_details_data': exam_details_data,
            'outside_route': outside_route,
            'title': title
        }
        return JsonResponse(data)
class ResultAPIView(APIView):
    def post(self, request):
        try:
            #get url_slug, roll_number, category from post request
            url_slug = request.data.get('url_slug')
            roll_number = request.data.get('rollNumber')
            category = request.data.get('category')
            print("url_slug",url_slug)
            print("roll_number",roll_number)
            print("category",category)
            answer_key_generator_data = answer_key_generator.objects.filter(button_name__iexact=url_slug.replace('-', ' ')).first()
            title = url_slug.replace('-', ' ').title() + ' Normalized Marks, And Rank Calculator By Learning Era'
            parts = re.split(r'(\d{4}.*)', title, maxsplit=1)
            first_part = ' '.join(word.upper() for word in parts[0].split())
            title = first_part + ' ' + parts[1]
            print("title",title)
            
            result_video_cache_key = f'result_video_data_{url_slug}'
            result_video_data = cache.get(result_video_cache_key)
            if not result_video_data:
                result_video_data = result_video.objects.filter(answer_key_generator=answer_key_generator_data).order_by('-result_video_order')
                cache.set(result_video_cache_key, result_video_data, 900)

            content = {}
            df = pd.DataFrame(list(raw_marks_candidates_data.objects.filter(answer_key_generator=answer_key_generator_data).values()))
            normalized_marks_candidates_data_for_exam = normalized_marks_candidates_data.objects.filter(answer_key_generator=answer_key_generator_data)
            df_normalized = pd.DataFrame(list(normalized_marks_candidates_data_for_exam.values()))
            
            print("after data frame creation")
            
            # roll_number = request.session.get('roll_number')
            # category = request.session.get('category')
            print("roll_number",roll_number)
            print("category",category)
            print(df.empty)
            print(df_normalized.empty)
            print(normalized_marks_candidates_data_for_exam)
            
            if df_normalized.empty or not normalized_marks_candidates_data_for_exam.filter(roll_number=roll_number).exists():
                print("inside if block normalization check")
                try:
                    normalized_marks_candidates_data.objects.filter(answer_key_generator=answer_key_generator_data).delete()
                    print("after delete normalized_marks_candidates_data")
                except Exception as e:
                    print("Error deleting normalized_marks_candidates_data:", e)

                if not df.empty and roll_number and category:
                    shift_groups = df.groupby('shift').size()
                    print("shift_groups",shift_groups)

                    if (shift_groups > answer_key_generator_data.normalization_starting_index).all():
                        df = calculate_normalized_marks(df)
                        overall_normalized_rank, normalized_category_rank = calculate_normalized_rank(df, roll_number, category)
                        print("overall_normalized_rank",overall_normalized_rank)
                        print("normalized_category_rank",normalized_category_rank)
                        
                        # if pd.isnull(overall_normalized_rank):
                        #     print("overall_normalized_rank is nan")
                        #     content['Candidate_Normalized_Rank'] = None
                        # else:
                        #     try:
                        #         content['Candidate_Normalized_Rank'] = int(float(overall_normalized_rank))*7
                        #     except (ValueError, TypeError):
                        #         print("Error converting overall_normalized_rank to integer")
                        #         content['Candidate_Normalized_Rank'] = None
                                
                        # if pd.isnull(normalized_category_rank):
                        #     print("normalized_category_rank is nan")
                        #     content['Candidate_Normalized_Rank_with_category'] = None
                        # else:
                        #     try:
                        #         content['Candidate_Normalized_Rank_with_category'] = int(float(normalized_category_rank))*7
                        #     except (ValueError, TypeError):
                        #         print("Error converting normalized_category_rank to integer")
                        #         content['Candidate_Normalized_Rank_with_category'] = None
                        
                        print('before candidate_row')
                        candidate_row = df[df['roll_number'] == roll_number]
                        print(candidate_row)
                        
                        for index, row in df.iterrows():
                            # Replace nan values with None before creating object
                            row_dict = row.where(pd.notna(row), None)
                            normalized_marks_candidates_data.objects.create(
                                answer_key_generator=answer_key_generator_data,
                                answer_key_link=row_dict['answer_key_link'],
                                category=row_dict['category'], 
                                roll_number=row_dict['roll_number'],
                                candidate_name=row_dict['candidate_name'],
                                venue_name=row_dict['venue_name'],
                                exam_date=row_dict['exam_date'],
                                exam_time=row_dict['exam_time'],
                                total_marks=row_dict['total_marks'],
                                total_marks_for_merit_list=row_dict['total_marks_for_merit_list'],
                                section_data=row_dict['section_data'],
                                overall_rank=row_dict['overall_rank'],
                                overall_average=row_dict['overall_average'],
                                category_rank=row_dict['category_rank'],
                                shift=row_dict['shift'],
                                shift_average=row_dict['shift_average'],
                                shift_rank=row_dict['shift_rank'],
                                category_average=row_dict['category_average'],
                                shift_mean=row_dict['shift_mean'],
                                shift_std=row_dict['shift_std'],
                                shift_median=row_dict['shift_median'],
                                shift_M_ti=row_dict['shift_M_ti'],
                                shift_M_iq=row_dict['shift_M_iq'],
                                normalized_marks=row_dict['normalized_marks'],
                                normalized_rank=row_dict['normalized_rank'],
                                normalized_category_rank=row_dict['normalized_category_rank'],
                                wrong_questions=row_dict['wrong_questions']
                            )
                            
                        print('after save data to normalized_marks_candidates_data')
                        candidate_normalized_marks = candidate_row['normalized_marks'].values[0]
                        content['Candidate_Normalized_Marks'] = float(candidate_normalized_marks)
                        candidate_normalized_rank = candidate_row['normalized_rank'].values[0]
                        content['Candidate_Normalized_Rank'] = float(candidate_normalized_rank) * 7
                        candidate_normalized_category_rank = candidate_row['normalized_category_rank'].values[0]
                        content['Candidate_Normalized_Rank_with_category'] = float(candidate_normalized_category_rank) * 7
                        candidate_shift_median = candidate_row['shift_median'].values[0]
                        content['Candidate_shift_median'] = float(candidate_shift_median)
                        
                    else:
                        content['Error'] = 'Not enough data for normalization'
            else:
                df = pd.DataFrame(list(normalized_marks_candidates_data.objects.filter(answer_key_generator=answer_key_generator_data).values()))
                candidate_row = df[df['roll_number'] == roll_number]
                candidate_normalized_marks = candidate_row['normalized_marks'].values[0]
                content['Candidate_Normalized_Marks'] = candidate_normalized_marks
                candidate_shift_median = candidate_row['shift_median'].values[0]
                content['Candidate_shift_median'] = candidate_shift_median
                candidate_normalized_rank = (candidate_row['normalized_rank'].values[0])
                print("before multiply by 7")
                print(candidate_normalized_rank)
                if candidate_normalized_rank == 'nan':
                    content['Candidate_Normalized_Rank'] = None
                else:
                    content['Candidate_Normalized_Rank'] = int(float(candidate_normalized_rank)) * 7
                    
                print("after multiply by 7")
                print(content['Candidate_Normalized_Rank'])
                candidate_normalized_rank_with_category = (candidate_row['normalized_category_rank'].values[0])
                print("before multiply by 7")
                print(candidate_normalized_rank_with_category)
                if candidate_normalized_rank_with_category == 'nan':
                    content['Candidate_Normalized_Rank_with_category'] = None
                else:
                    content['Candidate_Normalized_Rank_with_category'] = int(float(candidate_normalized_rank_with_category))*7

            print("content",content)
            # Replace any NaN values with None before returning response
            for key, value in content.items():
                if isinstance(value, float) and math.isnan(value):
                    content[key] = None
            
            data = {
                'content': content,
                # 'result_video_data': list(result_video_data.values()),
                # 'url_slug': url_slug,
                # 'title': title
            }

            return Response(data)
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

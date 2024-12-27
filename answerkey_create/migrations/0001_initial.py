# Generated by Django 5.1.4 on 2024-12-26 09:52

import ckeditor.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='answer_key_generator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('button_name', models.CharField(max_length=200)),
                ('url_word', models.CharField(default='digialm', max_length=200)),
                ('right_exam_name', models.CharField(default='CHSL Exam 2024 Tier I', max_length=200)),
                ('roll_number_name', models.CharField(default='Roll Number', max_length=200)),
                ('exam_name_name', models.CharField(default='Subject', max_length=200)),
                ('candidate_name_name', models.CharField(default='Candidate Name', max_length=200)),
                ('venue_name_name', models.CharField(default='Test Center Name', max_length=200)),
                ('exam_date_name', models.CharField(default='Test Date', max_length=200)),
                ('exam_time_name', models.CharField(default='Test Time', max_length=200)),
                ('question_per_subject', models.JSONField(default=[25, 25, 25, 25])),
                ('per_mcq_marks', models.JSONField(default=[2.0, 2.0, 2.0, 2.0])),
                ('wrong_ans_marks', models.JSONField(default=[0.5, 0.5, 0.5, 0.5])),
                ('question_panel_class', models.CharField(default='//div[contains(@class, "question-pnl")]', max_length=200)),
                ('right_answer_class', models.CharField(default='.//td[contains(@class, "rightAns")]', max_length=200)),
                ('section_class', models.CharField(default='//div[@class="section-lbl"]//span[@class="bold"]', max_length=200)),
                ('normalization_starting_index', models.IntegerField(default=0)),
                ('subject_count_in_merit_list', models.JSONField(default=[1, 1, 1, 1])),
                ('qualifying_percentage', models.JSONField(default={'EWS': 25, 'OBC': 25, 'SC': 20, 'ST': 20, 'UR': 30})),
                ('answer_key_order', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='exam_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('exam_description_order', models.IntegerField(default=0)),
                ('answer_key_generator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='answerkey_create.answer_key_generator')),
            ],
        ),
        migrations.CreateModel(
            name='form_video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_video_url', models.CharField(max_length=200)),
                ('form_video_order', models.IntegerField(default=0)),
                ('answer_key_generator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='answerkey_create.answer_key_generator')),
            ],
        ),
        migrations.CreateModel(
            name='normalized_marks_candidates_data',
            fields=[
                ('answer_key_link', models.CharField(max_length=200, unique=True)),
                ('category', models.CharField(max_length=50)),
                ('roll_number', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('candidate_name', models.CharField(max_length=200)),
                ('venue_name', models.CharField(max_length=200)),
                ('exam_date', models.CharField(max_length=200)),
                ('exam_time', models.CharField(max_length=200)),
                ('total_marks', models.FloatField()),
                ('total_marks_for_merit_list', models.FloatField(default=0)),
                ('section_data', models.JSONField(default=dict)),
                ('overall_rank', models.IntegerField(default=0)),
                ('overall_average', models.FloatField(default=0)),
                ('category_rank', models.IntegerField()),
                ('shift', models.CharField(max_length=200)),
                ('shift_average', models.FloatField()),
                ('shift_rank', models.IntegerField()),
                ('category_average', models.FloatField()),
                ('shift_mean', models.FloatField(blank=True, default=0, null=True)),
                ('shift_std', models.FloatField(blank=True, default=0, null=True)),
                ('shift_median', models.FloatField(blank=True, default=0, null=True)),
                ('shift_M_ti', models.FloatField(blank=True, default=0, null=True)),
                ('shift_M_iq', models.FloatField(blank=True, default=0, null=True)),
                ('normalized_marks', models.FloatField(blank=True, default=0, null=True)),
                ('normalized_rank', models.FloatField(blank=True, default=0, null=True)),
                ('normalized_category_rank', models.FloatField(blank=True, default=0, null=True)),
                ('wrong_questions', models.TextField(blank=True, default='', null=True)),
                ('answer_key_generator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='answerkey_create.answer_key_generator')),
            ],
        ),
        migrations.CreateModel(
            name='original_candidates_data',
            fields=[
                ('answer_key_link', models.CharField(max_length=200, unique=True)),
                ('category', models.CharField(max_length=50)),
                ('roll_number', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('candidate_name', models.CharField(max_length=200)),
                ('venue_name', models.CharField(max_length=200)),
                ('exam_date', models.CharField(max_length=200)),
                ('exam_time', models.CharField(max_length=200)),
                ('total_marks', models.FloatField()),
                ('total_marks_for_merit_list', models.FloatField(default=0)),
                ('section_data', models.JSONField(default=dict)),
                ('wrong_questions', models.TextField(blank=True, default='', null=True)),
                ('answer_key_generator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='answerkey_create.answer_key_generator')),
            ],
            options={
                'ordering': ['answer_key_generator', 'roll_number'],
            },
        ),
        migrations.CreateModel(
            name='raw_marks_candidates_data',
            fields=[
                ('answer_key_link', models.CharField(max_length=200, unique=True)),
                ('category', models.CharField(max_length=50)),
                ('roll_number', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('candidate_name', models.CharField(max_length=200)),
                ('venue_name', models.CharField(max_length=200)),
                ('exam_date', models.CharField(max_length=200)),
                ('exam_time', models.CharField(max_length=200)),
                ('total_marks', models.FloatField()),
                ('total_marks_for_merit_list', models.FloatField(default=0)),
                ('section_data', models.JSONField(default=dict)),
                ('overall_rank', models.IntegerField(default=0)),
                ('overall_average', models.FloatField(default=0)),
                ('category_rank', models.IntegerField()),
                ('shift', models.CharField(max_length=200)),
                ('shift_average', models.FloatField()),
                ('shift_rank', models.IntegerField()),
                ('category_average', models.FloatField()),
                ('marks_in_qualifying_subjects', models.FloatField(default=0)),
                ('qualifies', models.BooleanField(default=False)),
                ('wrong_questions', models.TextField(blank=True, default='', null=True)),
                ('answer_key_generator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='answerkey_create.answer_key_generator')),
            ],
        ),
        migrations.CreateModel(
            name='result_video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result_video_url', models.CharField(max_length=200)),
                ('result_video_order', models.IntegerField(default=0)),
                ('answer_key_generator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='answerkey_create.answer_key_generator')),
            ],
        ),
    ]

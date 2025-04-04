# Generated by Django 5.1.3 on 2025-02-03 07:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='exam_review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('button_name', models.CharField(max_length=200)),
                ('exam_review_order', models.IntegerField(default=0)),
                ('exam_days', models.JSONField(default=['09-09-2024', '10-09-2024', '11-09-2024'])),
                ('exam_shifts', models.IntegerField(default=1)),
                ('gender', models.BooleanField(default=False)),
                ('category', models.BooleanField(default=False)),
                ('english_attempts', models.BooleanField(default=False)),
                ('maths_attempts', models.BooleanField(default=False)),
                ('reasoning_attempts', models.BooleanField(default=False)),
                ('gk_attempts', models.BooleanField(default=False)),
                ('computer_attempts', models.BooleanField(default=False)),
                ('exam_review', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='exam_review_store_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_day', models.CharField(blank=True, max_length=200, null=True)),
                ('exam_shift', models.IntegerField(blank=True, default=0, null=True)),
                ('gender', models.CharField(blank=True, max_length=50, null=True)),
                ('category', models.CharField(blank=True, max_length=50, null=True)),
                ('english_attempts', models.CharField(blank=True, max_length=50, null=True)),
                ('maths_attempts', models.CharField(blank=True, max_length=50, null=True)),
                ('reasoning_attempts', models.CharField(blank=True, max_length=50, null=True)),
                ('gk_attempts', models.CharField(blank=True, max_length=50, null=True)),
                ('computer_attempts', models.CharField(blank=True, max_length=50, null=True)),
                ('exam_review_data', models.TextField(blank=True, default='', null=True)),
                ('exam_review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam_reviews.exam_review')),
            ],
        ),
    ]

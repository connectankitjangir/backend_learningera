# Generated by Django 5.1.3 on 2025-02-03 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SSCResult',
            fields=[
                ('roll_number', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('fathername', models.CharField(max_length=100)),
                ('mothername', models.CharField(max_length=100)),
                ('dob', models.DateField()),
                ('cat1', models.CharField(blank=True, max_length=50, null=True)),
                ('cat2', models.CharField(blank=True, max_length=50, null=True)),
                ('cat3', models.CharField(blank=True, max_length=50, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('candidate_name', models.CharField(max_length=100)),
                ('venue_name', models.CharField(max_length=200)),
                ('exam_date', models.DateField()),
                ('maths_marks', models.FloatField()),
                ('reasoning_marks', models.FloatField()),
                ('english_marks', models.FloatField()),
                ('gk_marks', models.FloatField()),
                ('computer_marks', models.FloatField()),
                ('normalized_marks_s1', models.FloatField()),
                ('normalized_marks_s2', models.FloatField()),
                ('total_normalized_marks', models.FloatField()),
            ],
            options={
                'db_table': 'ranked_output',
                'managed': False,
            },
        ),
    ]

# Generated by Django 5.0.6 on 2024-07-06 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fileupload', '0003_data_sorted_exam_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='data_sorted',
            name='subject_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
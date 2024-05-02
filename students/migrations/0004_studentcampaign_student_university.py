# Generated by Django 5.0.4 on 2024-05-01 15:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_studentcampaign'),
        ('university', '0003_university_is_approve'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentcampaign',
            name='student_university',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='campaign_student_university', to='university.university'),
            preserve_default=False,
        ),
    ]

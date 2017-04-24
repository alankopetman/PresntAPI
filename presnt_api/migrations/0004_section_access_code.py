# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-24 02:39
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('presnt_api', '0003_section_class_time_end'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='access_code',
            field=models.CharField(blank=True, default=uuid.uuid4, max_length=10, unique=True),
        ),
    ]
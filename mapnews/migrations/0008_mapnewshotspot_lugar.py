# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-10-05 14:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapnews', '0007_auto_20191004_2006'),
    ]

    operations = [
        migrations.AddField(
            model_name='mapnewshotspot',
            name='lugar',
            field=models.CharField(default='tags', max_length=256),
        ),
    ]
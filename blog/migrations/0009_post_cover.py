# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-12 10:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20160512_0649'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='cover',
            field=models.ImageField(blank=True, upload_to='uploads/%Y/%m/%d/'),
        ),
    ]

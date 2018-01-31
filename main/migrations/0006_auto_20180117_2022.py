# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-01-17 15:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20180117_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Category'),
        ),
        migrations.AlterField(
            model_name='category',
            name='photo',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to=''),
        ),
    ]
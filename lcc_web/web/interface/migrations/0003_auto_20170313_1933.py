# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-13 18:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0002_auto_20170313_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='starsfilter',
            name='finish_date',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
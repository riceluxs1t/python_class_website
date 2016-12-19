# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-19 01:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('homework_name', models.CharField(max_length=30)),
                ('deadline', models.DateField()),
                ('modules', models.CharField(max_length=1000)),
            ],
        ),
    ]

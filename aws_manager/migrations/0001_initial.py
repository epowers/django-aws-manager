# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-22 01:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AWSServer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('aws_access_key', models.CharField(max_length=20)),
                ('aws_secret_key', models.CharField(max_length=40)),
                ('aws_region', models.CharField(default='us-east-1', max_length=20)),
                ('user_name', models.CharField(default='Administrator', max_length=20)),
            ],
        ),
    ]
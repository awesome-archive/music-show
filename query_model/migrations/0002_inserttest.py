# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 15:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('query_model', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inserttest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, null=True)),
                ('uid', models.TextField(blank=True, null=True)),
            ],
        ),
    ]

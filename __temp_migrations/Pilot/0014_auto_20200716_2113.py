# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2020-07-16 19:13
from __future__ import unicode_literals

from django.db import migrations
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('Pilot', '0013_auto_20200716_1904'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='urn_draws_1',
            field=otree.db.models.StringField(max_length=10000, null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='urn_draws_2',
            field=otree.db.models.StringField(max_length=10000, null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='urn_draws_3',
            field=otree.db.models.StringField(max_length=10000, null=True),
        ),
    ]

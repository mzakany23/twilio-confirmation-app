# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game_confirmation', '0002_auto_20150515_0023'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='field_location_url',
            field=models.CharField(max_length=40, null=True, blank=True),
        ),
    ]

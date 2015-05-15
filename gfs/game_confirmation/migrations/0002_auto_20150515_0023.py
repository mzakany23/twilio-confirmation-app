# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game_confirmation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameconfirmation',
            name='players',
            field=models.ManyToManyField(to='game_confirmation.Player', blank=True),
        ),
    ]

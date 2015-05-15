# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConfirmMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recipient', models.CharField(max_length=40)),
                ('body', models.CharField(max_length=40)),
                ('confirmed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('opponent', models.CharField(max_length=40)),
                ('field_address', models.CharField(max_length=40)),
                ('city', models.CharField(max_length=40)),
                ('zip_code', models.IntegerField(default=0)),
                ('attendee_total', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='GameConfirmation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('invitations_sent', models.IntegerField(default=0)),
                ('date_sent_id', models.DateField(auto_now_add=True, null=True)),
                ('game', models.ForeignKey(blank=True, to='game_confirmation.Game', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('phone_number', models.CharField(max_length=40)),
            ],
        ),
        migrations.AddField(
            model_name='gameconfirmation',
            name='players',
            field=models.ManyToManyField(to='game_confirmation.Player', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='confirmmessage',
            name='game_confirm',
            field=models.ForeignKey(blank=True, to='game_confirmation.GameConfirmation', null=True),
        ),
        migrations.AddField(
            model_name='confirmmessage',
            name='player',
            field=models.ForeignKey(blank=True, to='game_confirmation.Player', null=True),
        ),
    ]

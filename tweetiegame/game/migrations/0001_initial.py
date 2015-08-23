# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('player1score', models.IntegerField(default=0)),
                ('player2score', models.IntegerField(default=0)),
                ('completed', models.BooleanField(default=False)),
                ('round', models.IntegerField(default=0)),
                ('giveword', models.CharField(max_length=100, default=None)),
                ('guessword', models.CharField(max_length=100, default=None)),
                ('form_player', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='form_player')),
                ('give_player', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='give_player')),
                ('player1', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='player1')),
                ('player2', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='player2')),
            ],
        ),
    ]

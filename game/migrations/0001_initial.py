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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('player1score', models.IntegerField(default=0)),
                ('player2score', models.IntegerField(default=0)),
                ('completed', models.BooleanField(default=False)),
                ('round', models.IntegerField(default=1)),
                ('giveword', models.CharField(max_length=100, default='')),
                ('guessword', models.CharField(max_length=100, default='')),
                ('form_player', models.ForeignKey(related_name='form_player', to=settings.AUTH_USER_MODEL)),
                ('give_player', models.ForeignKey(related_name='give_player', to=settings.AUTH_USER_MODEL)),
                ('player1', models.ForeignKey(related_name='player1', to=settings.AUTH_USER_MODEL)),
                ('player2', models.ForeignKey(related_name='player2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

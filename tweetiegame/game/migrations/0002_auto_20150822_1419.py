# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='giveword',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='game',
            name='guessword',
            field=models.CharField(default='', max_length=100),
        ),
    ]

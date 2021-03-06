from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Game(models.Model):
    """model to keep track of players and their score"""
    player1 = models.ForeignKey(User, related_name='player1')
    player2 = models.ForeignKey(User, related_name='player2')
    player1score = models.IntegerField(default=0)
    player2score = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    give_player = models.ForeignKey(User, related_name='give_player')
    form_player = models.ForeignKey(User, related_name='form_player')
    round = models.IntegerField(default=1)
    giveword = models.CharField(max_length=100, default='')
    guessword = models.CharField(max_length=100, default='')



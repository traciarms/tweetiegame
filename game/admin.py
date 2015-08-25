from django.contrib import admin

# Register your models here.
from game.models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('player1', 'player2', 'player1score', 'player2score', 'completed')

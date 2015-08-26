from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
import json
from django.views.generic import TemplateView
import requests
from game.forms import WordForm
from tweetiegame.settings import TWITTER_TOKEN

from game.models import Game


# class SearchTwitterView(TemplateView):
    # template_name = "index.html"

def get_twitter_dict(word1, word2):
    # def get_context_data(self, **kwargs):
    #     context = super(SearchTwitterView, self).get_context_data(**kwargs)

    response = requests.get(
        'https://api.twitter.com/1.1/search/tweets.json?q={}'.
            format(word1, word2),
        headers={'Authorization': 'Bearer {}'.format(TWITTER_TOKEN)})

    tweets = response.json()
    num = len(tweets['statuses'])
    tweet_list = tweets['statuses'][:3]
    ret_tweet_list = []

    for each in range(len(tweet_list)):
        ret_tweet_list.append(tweet_list[each]['text'])

    return_dict = {'count': num, 'tweets': ret_tweet_list}
    return return_dict

def playgame(request):

    winner = ''
    try:
        game = Game.objects.get(completed=False)
    except:
        game = Game.objects.create(player1=User.objects.get(username='player1'),
                                   player2=User.objects.get(username='player2'),
                                   give_player=User.objects.get(username='player1'),
                                   form_player=User.objects.get(username='player1'))
    if request.method == 'GET':
        form = WordForm()
        context = {'game': game, 'form': form}
        return render(request, 'index.html', context)

    if request.method == 'POST':
        form = WordForm(request.POST)
        if request.user == game.give_player:
            if form.is_valid():
                giveword = form.cleaned_data['word']
                game.giveword = giveword
                if game.form_player == User.objects.get(username='player1'):
                    game.form_player = User.objects.get(username='player2')
                else:
                    game.form_player = User.objects.get(username='player1')
        if request.user != game.give_player:
            if form.is_valid():
                guessword = form.cleaned_data['word']
                game.guessword = guessword
        if len(game.guessword) > 0 and len(game.giveword) > 0:
            twitter_dict = get_twitter_dict(game.giveword, game.guessword)
            game.giveword = ''
            game.guessword = ''
            game.round += 1
            if game.give_player == User.objects.get(username='player1'):
                game.player2score += twitter_dict['count']
                game.give_player = User.objects.get(username='player2')
                game.form_player = User.objects.get(username='player2')
            else:
                game.player1score += twitter_dict['count']
                game.give_player = User.objects.get(username='player1')
                game.form_player = User.objects.get(username='player1')
            form = WordForm()
            if game.round >= 6:
                game.completed = True
                if game.player1score > game.player2score:
                    winner = 'Player 1'
                else:
                    winner = 'Player 2'
            game.save()
            context = {'game': game, 'form': form, 'form_player':
                    game.form_player, 'twitter_dict': twitter_dict, 'winner': winner}
            return render(request, 'index.html', context)
        context = {'game': game, 'form': form,}
        game.save()
        return render(request, 'index.html', context)
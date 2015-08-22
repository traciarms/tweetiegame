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
#     template_name = "index.html"

def get_twitter_dict(word1, word2):
    # context = super(SearchTwitterView, self).get_context_data(**kwargs)

    response = requests.get(
        'https://api.twitter.com/1.1/search/tweets.json?q={} {}'.
            format(word1, word2),
        headers={'Authorization': 'Bearer {}'.format(TWITTER_TOKEN)})

    tweets = response.json()

    tweet_list = tweets['statuses'][:3]

    ret_tweet_list = []
    ret_tweet_list.append(tweet_list[0]['text'])
    ret_tweet_list.append(tweet_list[1]['text'])
    ret_tweet_list.append(tweet_list[2]['text'])

    return_dict = {'count': len(tweets), 'tweets': ret_tweet_list}
    return return_dict

def playgame(request):
    form = WordForm(request.POST)
    try:
        game = Game.objects.get(completed=False)
    except:
        game = Game.objects.create(player1=User.objects.get(username='player1'),
                                   player2=User.objects.get(username='player2'),
                                   give_player=User.objects.get(username='player1'),
                                   form_player=User.objects.get(username='player1'))
    if request.method == 'GET':
        context = {'game': game, 'form': form}
        return render(request, 'index.html', context)
    if request.method == 'POST':
        if request.user == game.give_player:
            if form.is_valid():
                giveword = form.cleaned_data['word']
                game.giveword = giveword
                game.save()
                if game.form_player == User.objects.get(username='player1'):
                    game.form_player = User.objects.get(username='player2')
                else:
                    game.form_player = User.objects.get(username='player1')
        if request.user != game.give_player:
            if form.is_valid():
                guessword = form.cleaned_data['word']
                game.guessword = guessword
                game.save()
        if len(game.guessword) > 0 and len(game.giveword) > 0:
            twitter_dict = get_twitter_dict(game.giveword, game.guessword)
            game.giveword = ''
            game.guessword = ''
            game.round += 1
            game.save()
            if game.give_player == User.objects.get(username='player1'):
                game.player2score += twitter_dict['count']
                game.give_player = User.objects.get(username='player2')
                game.form_player = User.objects.get(username='player2')
                game.save()
            else:
                game.player1score += twitter_dict['count']
                game.give_player == User.objects.get(username='player1')
                game.form_player = User.objects.get(username='player1')
                game.save()
                context = {'game': game, 'form': form, 'form_player' : game.form_player, 'twitter_dict': twitter_dict}
                return render(request, 'index.html', context)
        context = {'game': game, 'form': form,}
        return render(request, 'index.html', context)
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
import json
from django.views.generic import TemplateView
import requests
from tweetiegame.settings import TWITTER_TOKEN
from game.forms import GiveForm, GuessForm
from game.models import Game


class SearchTwitterView(TemplateView):
    template_name = "index.html"

    # def get_tweet_dict(word1, word2):
    def get_context_data(self, **kwargs):
        context = super(SearchTwitterView, self).get_context_data(**kwargs)

        response = requests.get(
            'https://api.twitter.com/1.1/search/tweets.json?q={} {}'.
                format('red', 'dress'),
            headers={'Authorization': 'Bearer {}'.format(TWITTER_TOKEN)})

        tweets = response.json()
        num = len(tweets)
        tweet_list = tweets['statuses']

        return_dict = {'count': len(tweets), 'tweets': tweet_list}
        return context

        # {count: value, tweets: listof3}


def playgame(request):
    giveform = GiveForm(request.POST)
    guessform = GuessForm(request.POST)
    try:
        game = Game.objects.get(completed=False)
    except:
        game = Game.objects.create(player1=User.objects.get(username='player1'),
                                   player2=User.objects.get(username='player2'),
                                   give_player=User.objects.get(username='player1'))
    context = {'game': game, 'giveform': giveform, 'guessform': guessform}
    if request.method == 'GET':
        return render(request, 'index.html', context)
    if request.method == 'POST':
        giveword = giveform.cleaned_data['giveword']
        guessword = guessform.cleaned_data['guessword']
        context = {'game': game, 'giveform': giveform, 'guessform': guessform, 'giveword': giveword, 'guessword': guessword}
        return render(request, 'index.html', context)
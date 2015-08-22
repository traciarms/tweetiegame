from django.contrib.auth.models import User
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

    for each in range(len(tweet_list)):
        ret_tweet_list.append(tweet_list[each]['text'])

    return_dict = {'count': len(tweets), 'tweets': ret_tweet_list}
    return return_dict

def playgame(request):
    give_form = GiveForm(request.POST)
    guess_form = GuessForm(request.POST)
    try:
        game = Game.objects.get(completed=False)
    except:
        game = Game.objects.create(player1=User.objects.get(username='player1'),
                                   player2=User.objects.get(username='player2'),
                                   give_player=User.objects.get(username='player1'))
    if request.method == 'GET':
        context = {'game': game, 'giveform': give_form, 'guessform': guess_form}
        return render(request, 'index.html', context)
    if request.method == 'POST':
        if give_form.is_valid():
            giveword = give_form.cleaned_data['giveword']
        if guess_form.is_valid():
            guessword = guess_form.cleaned_data['guessword']
        context = {'game': game, 'giveform': give_form,
                   'guessform': guess_form, 'giveword': giveword,
                   'guessword': guessword}
        return render(request, 'index.html', context)
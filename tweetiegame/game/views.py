from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
import json
from django.views.generic import TemplateView
from game.client import Client
import requests
from game.forms import GiveForm, GuessForm
from game.models import Game


class SearchTwitterView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(SearchTwitterView, self).get_context_data(**kwargs)

        # The consumer secret is an example and will not work for real requests
        # To register an app visit https://dev.twitter.com/apps/new
        CONSUMER_KEY = 'N5pdrHbC2BU4vkzmzzgAkXQ9T'
        CONSUMER_SECRET = 'tdBSEKC4fnePzds99rLHx63ErvuTOqpQ3gStQI7ApN2AuJQnir'

        client = Client(CONSUMER_KEY, CONSUMER_SECRET)

        # Pretty print of tweet payload
        # tweet = client.request('https://api.twitter.com/1.1/statuses/show.json?id=316683059296624640')
        context['tweet'] = client.request(
            'https://api.twitter.com/1.1/search/tweets.json?q=%40twitterapi')
        # print(json.dumps(tweet, sort_keys=True, indent=4, separators=(',', ':')))

        # Show rate limit status for this application
        # status = client.rate_limit_status()
        # print(status['resources']['search'])
        return context


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
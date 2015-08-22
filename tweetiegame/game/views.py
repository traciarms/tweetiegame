from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
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
    ret_tweet_list.append(tweet_list[0]['text'])
    ret_tweet_list.append(tweet_list[1]['text'])
    ret_tweet_list.append(tweet_list[2]['text'])

    return_dict = {'count': len(tweets), 'tweets': ret_tweet_list}
    return return_dict

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

# Create your views here.
import json
from django.views.generic import TemplateView
import requests
from tweetiegame.settings import TWITTER_TOKEN


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


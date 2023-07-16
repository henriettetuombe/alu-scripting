#!/usr/bin/python3
"""parses the title of all hot articles"""
import json
import requests


def count_words(subreddit, word_list, after='', hot_list=None):
    if hot_list is None:
        hot_list = [0] * len(word_list)

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    request = requests.get(url, params={'after': after},
                           allow_redirects=False,
                           headers={'User-Agent': 'My User Agent 1.0'})

    if request.status_code == 200:
        data = request.json()

        for topic in data['data']['children']:
            title_words = topic['data']['title'].split()
            for word in title_words:
                for i, keyword in enumerate(word_list):
                    if keyword.lower() == word.lower():
                        hot_list[i] += 1

        after = data['data']['after']
        if after is None:
            word_counts = {}
            for i, word in enumerate(word_list):
                if word not in word_counts:
                    word_counts[word] = hot_list[i]
                else:
                    word_counts[word] += hot_list[i]

            sorted_counts = sorted(
                word_counts.items(),
                key=lambda x: (-x[1], x[0].lower())
            )

            for word, count in sorted_counts:
                if count > 0:
                    print("{}: {}".format(word.lower(), count))
        else:
            count_words(subreddit, word_list, after, hot_list)

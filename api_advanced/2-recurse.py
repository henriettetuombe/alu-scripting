#!/usr/bin/python3
""""Recurse"""
import requests


def recurse(subreddit, hot_list=[], after=""):
    """"
    Reddit sends an after property in the response.
    Keep retrieving comments until after is null.
    """
    url = "https://www.reddit.com/r/{}/hot.json" \
        .format(subreddit)
    header = {'User-Agent': 'Mozilla/5.0'}
    param = {'after': after}
    response = requests.get(url, headers=header, params=param)

    if response.status_code != 200:
        return None
    else:
        json_res = response.json()
        # print(json_res.get('data').get('after'))
        after = json_res.get('data').get('after')
        has_next = \
            json_res.get('data').get('after') is not None
        # print(has_next)
        hot_articles = json_res.get('data').get('children')
        [hot_list.append(article.get('data').get('title'))
         for article in hot_articles]
        # print(len(hot_list))
        # print(hot_list)
        return recurse(subreddit, hot_list, after=after) \
            if has_next else hot_list

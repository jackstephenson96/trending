# -*- coding: utf-8 -*-

import requests
from ask_sdk_model import IntentRequest
from typing import Union, Dict, List
import feedparser
import json
import pycountry_convert as pc

# put this in Data.py eventually
google_trends_rss_url = 'https://trends.google.com/trends/trendingsearches/daily/rss?geo='



def gettrends(url=google_trends_rss_url, geo='US', num=1):

    url = url + geo
    feed = feedparser.parse(url)
    alltrends = feed['entries']
    trends = []
    if alltrends:
        for i in range(num):
            trend = {'num': i, 'trend':alltrends[i]['title'], 'newstitle':alltrends[i]['ht_news_item_title']}
            trends.append(trend)
    else:
        trends.append({'num':0, 'trend':'oops, this skill is out of date', 'newstitle':None})
    return trends

def get_country_code(country):
    code = pc.country_name_to_country_alpha2(country)
    return code


# def get_weather(city_data, api_info):
#     """Return weather information for a city by calling API."""
#     # type: (Dict, Dict) -> str, str, str
#     url = build_url(city_data, api_info)

#     response = http_get(url)
#     channel = response["query"]["results"]["channel"]

#     local_time = channel["lastBuildDate"][17:25]
#     current_temp = channel["item"]["condition"]["temp"]
#     current_condition = channel["item"]["condition"]["text"]

#     return local_time, current_temp, current_condition


def get_resolved_value(request, slot_name):
    """Resolve the slot name from the request."""
    # type: (IntentRequest, str) -> Union[str, None]
    try:
        return request.intent.slots[slot_name].value
    except (AttributeError, ValueError, KeyError, IndexError):
        return None

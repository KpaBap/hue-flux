import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta


def get_sun(location):
    apikey = "abc123"
    if apikey == "abc123":
      print ("Please set a valid wunderground API key in sun.py")
      return

    location = urllib.parse.quote(location)
    url = "http://api.wunderground.com/api/{}/astronomy/q/{}.json"
    url = url.format(apikey, location)

    response = urllib.request.urlopen(url).read().decode("utf-8", "replace")
    data = json.loads(response)['moon_phase']
    time = "{}:{}".format(data['current_time']['hour'], data['current_time']['minute'])

    sunrise = "{}:{}".format(data['sunrise']['hour'], data['sunrise']['minute'])
    sunset = "{}:{}".format(data['sunset']['hour'], data['sunset']['minute'])

    return sunrise, sunset

#   Copyright 2015 Iavor Todorov
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import json
import urllib.request
import urllib.parse


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

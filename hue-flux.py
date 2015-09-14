#   Copyright 2014 Iavor Todorov
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
#  

import ssdp
import urllib.request
import xml.dom.minidom
import phue
import time
import math
import sun


def discover_and_connect_bridge():
    ssdp_responses = ssdp.discover("device")
    registered = False
    help_printed = False

    for response in ssdp_responses:

        hub_ip = verify_hue_upnp(response.location)

        if hub_ip:
            print("Found hub at: %s" % hub_ip)

    while not(registered):
        try:
            bridge = phue.Bridge(hub_ip)
            registered = True
            print("Conected to hub at: %s" % hub_ip)
            return bridge
        except phue.PhueRegistrationException:
            registered = False
            time.sleep(1)
            if not help_printed:
                print(
                    "Please press the button on the Hue bridge to connect this app.")
                help_printed = True


def verify_hue_upnp(url):

    upnpxml = urllib.request.urlopen(url).read().decode()
    dom = xml.dom.minidom.parseString(upnpxml)

    baseurl = dom.getElementsByTagName("URLBase")[0].childNodes[0].data
    hub_ip = urllib.request.urlparse(baseurl).netloc.split(":")[0]

    hub_config = urllib.request.urlopen(
        baseurl + "api/%20/config").read().decode()

    if hub_config.find("hue") != -1:
        return hub_ip
    else:
        return False


def find_lights_by_name(bridge, searchtext):
    lights = bridge.get_light_objects()
    computer_lights = []

    # Find lights and initialize them
    for light in lights:
        if light.name.find(searchtext) != -1:
            computer_lights.append(light)
            light.transitiontime = 0
            light.sat = 255
            light.brightness = 255

    return computer_lights


def turn_lights_on(lights):
    for light in lights:
        if not light.on:
            light.on = True
            light.brightness = 254


def turn_lights_off(lights):
    for light in lights:
        if light.on:
            light.on = False


def set_lights_colortemp_k(lights, temp):
    for light in lights:
        light.colortemp_k = temp


def set_lights_xy(lights, x, y):
    for light in lights:
        light.xy = [x, y]

#        print("Setting light to: %s, %s" % (x, y))


def frange(start, stop, step):

    i = start

    if start > stop:
        while i > stop:
            yield i
            i += step
    else:
        while i < stop:
            yield i
            i += step


def fade_colortemp_k(lights, temp_from, temp_to, fadetime):

    delay = (0.2)

    # If the color temp steps work out to less than 1, increase the delay
    # instead
    if abs(temp_from - temp_to) < fadetime:
        delay = fadetime / abs(temp_from - temp_to)

    if temp_from > temp_to:
        temp_to -= 1
        step = -(round((temp_from - temp_to) / (fadetime / delay), 2))
    else:
        temp_to += 1
        step = (round((temp_to - temp_from) / (fadetime / delay), 2))

    print("Fading lights with %s sec delay and %s color step" % (delay, step))

    for temp in frange(temp_from, temp_to, step):
        x, y = RGB_to_xy(*colortemp_k_to_RGB(temp))
        set_lights_xy(lights, x, y)

        print("Setting lights to temp: %s" % temp)
        time.sleep(delay)

# Taken from:
# http://www.developers.meethue.com/documentation/color-conversions-rgb-xy


def RGB_to_xy(red, green, blue):

    red = red / 255
    blue = blue / 255
    green = green / 255

    # Gamma correction
    red = pow((red + 0.055) / (1.0 + 0.055),
              2.4) if (red > 0.04045) else (red / 12.92)
    green = pow((green + 0.055) / (1.0 + 0.055),
                2.4) if (green > 0.04045) else (green / 12.92)
    blue = pow((blue + 0.055) / (1.0 + 0.055),
               2.4) if (blue > 0.04045) else (blue / 12.92)

    x = red * 0.664511 + green * 0.154324 + blue * 0.162028
    y = red * 0.313881 + green * 0.668433 + blue * 0.047685
    z = red * 0.000088 + green * 0.072310 + blue * 0.986039

    try:
        cx = x / (x + y + z)
        cy = y / (x + y + z)
    except:
        cx, cy = 0, 0

    if cx > 0.675:
        cx = 0.675
    if cx < 0.167:
        cx = 0.167

    if cy > 0.518:
        cy = 0.518
    if cy < 0.04:
        cy = 0.04

    return round(cx, 3), round(cy, 3)


def colortemp_k_to_RGB(temp):
    temp = temp / 100

    if temp <= 66:
        red = 255
    else:
        red = temp - 60
        red = 329.698727446 * (red ** -0.1332047592)
        red = 0 if red < 0 else red
        red = 255 if red > 255 else red

    if temp <= 66:
        green = temp
        green = 99.4708025861 * math.log(green) - 161.1195681661
        green = 0 if green < 0 else green
        green = 255 if green > 255 else green
    else:
        green = temp - 60
        green = 288.1221695283 * (green ** -0.0755148492)
        green = 0 if green < 0 else green
        green = 255 if green > 255 else green

    if temp >= 66:
        blue = 255
    else:
        if temp <= 19:
            blue = 0
        else:
            blue = temp - 10
            blue = 138.5177312231 * math.log(blue) - 305.0447927307
            blue = 0 if blue < 0 else blue
            blue = 255 if blue > 255 else blue

    return red, green, blue


def get_secs_to_hour(hour):
    today = time.strftime("%x", time.localtime())
    return time.mktime(time.strptime(today + hour, "%x%H:%M")) - time.time()


# MAIN PROGRAM #
# Change settings as desired

location = "95050"  # Zip code or some other location string
bedtime = "21:30"
day_colortemp = 4000
sunset_colortemp = 3000
bedtime_colortemp = 1900

# String to use to search for lights to work with.
# For example, if your computer room lights are named "Computer 1",
# "Computer 2", etc
searchtext = "Computer"

# Don't touch things below here

print("Discovering Hue bridges...")
try:
    bridge = phue.Bridge()
    registered = True
    print("Found previously connected bridge")
except:
    bridge = discover_and_connect_bridge()


lights = find_lights_by_name(bridge, searchtext)
turn_lights_on(lights)

sunset_time = sun.get_sun(location)[1]  # Sunset time in 24hr format
fadetime = get_secs_to_hour(sunset_time)

print("Local sunset is at: %s, in %s seconds" % (sunset_time, fadetime))
fade_colortemp_k(lights, day_colortemp, sunset_colortemp, fadetime)

fadetime = get_secs_to_hour(bedtime)
print("The sun has set. Bedtime is at: %s, in %s seconds" %
      (bedtime, fadetime))
fade_colortemp_k(lights, sunset_colortemp, bedtime_colortemp, fadetime)

print("Sweet dreams!")

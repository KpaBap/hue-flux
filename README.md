# hue-flux
Recreation of f.lux for Phillips Hue lights in Python by KpaBap

This script aims to closely replicate the functionality of f.lux for Phillips Hue
It is meant to be ran from a cronjob once a day, or manually whenever you want the lights to turn on and begin fading

Requirements: 
- Phillips Hue bridge on local network
- Python 3
- Phue library (https://github.com/studioimaginaire/phue) - run "pip3 install phue"

- Get a Wunderground API key and save it on a single line in a text file called wunder.api - this allows automatic lookup of your location's time of sunset
- You can also manually set "sunset_time" instead in 24hr format - e.g. "21:00"

- Set the prefered color temperatures and bed times in hue-flux.py variables



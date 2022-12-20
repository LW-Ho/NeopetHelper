# Update

Support Asyncio, Docker Container, Gmail notify, use selenium avoid stackpath CDN.

Please check dockerfile environment variables

Warning:
This docker image support Intel (linux/amd64), because selenium can not running on Apple Silicon(ARM64).
So, if u only Apple Silicon need run other container to replace selenium use webdriver remote method.

# Neopet Helper
This is a collection of python scripts that can be used to automate common Neopet tasks for you. At this time I've only uploaded a couple scripts. I have other scripts to perform dailies, get highscores in games, stock shops, shop wizard search, buy stocks, etc.

I will upload all my scripts with time.

If there's a task you need done let me know and I'll try to get that for you sooner than later if I already have it.

## How to use
Basic python knowledge is needed but to get it running all you have to do is add your username and password to main.py and run it.

## Dailies.py (Update 2022/08/31)
Runs the most common and lucrative Neopet daily activities. Currently it includes: <br>
* Collecting bank interest
* Buying daily allotment of stocks
* Spinning Trudy's Surprise Wheeel
* Coltzans Shrine
* Fishing Hole
* Giant Omelette
* TDMGPOP
* Healing Springs
* Advent Calendar
* Pet Lab (Need to open this Map)
* Island Training School (Default: Level, Auto buy codestone)
* More to come :)

## Classes
### Login
This script is self-explanatory. It allows you to log into your Neopets account by providing your username, password and a Requests session.

### Bank
This script allows you to deposit and withdraw neopoints from the bank; aswell as collect interest from the bank. Note: it doesn't support security pins which could be something you could contribute to the project.

### ShopWizard
This script provides a core functionality of the Neopet website and it's to use the Shop Wizard. It can do things like search and find the cheapest price of an item for you. It can also buy an item for you if you wish.

This script provides a lot of potential to the end user to develop snipe bots and auto restocking bots.

## Warning
Use of these scripts may result in your Neopets account being banned (frozen)

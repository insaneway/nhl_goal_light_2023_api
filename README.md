# Overview
All credit goes to arim215 (https://github.com/arim215/nhl_goal_light) for original work. NHL changed their API in 2023 and this has been adapted to the new API.

Nhl goal light python3 for raspberry pi GPIO. Works with any team, just enter full team name when prompted. (e.g. Dallas Stars)

Before use, make sure you have:

python3, python3-pip, git

Run the following commands manually to install requirements

run:

```
$ sudo apt-get install git python3 python3-pip
$ git clone https://github.com/arim215/nhl_goal_light.git
$ pip3 install -r requirements.txt
```

You can prepare a "settings.txt" file to auto-config the nhl_goal_light.py code, or the code will ask for your input everytime.

To start application, use following commands:
```
$ sudo python3 nhl_goal_light.py
```
When prompted to select a team input the full team name, city plus name. (e.g. Dallas Stars)

If you want to set a default and bypass the data entry, put the team tricode in line 2 of settings.txt (e.g. DAL)

# Materials
For documentation on how to wire the GPIOs with the lights and the button, pleaser refer to the "docs" folder.

* Raspberry Pi (currently using raspberry pi A model, but any model will work)
* Red Rotating Beacon Warning Light from ebay
* 5V 2 Channel Relay Module from ebay
* Momentary OFF ON Push Round Button
* 12V to 5V 1A adapter (used a car usb adapter) would be good to have a dual usb adapter in case you need to plug something else like a usb speaker.
* 3.5mm audio extension cable

# Audio
Goal horns are tied to the team you select. All 32 teams are included. If you wish to change the goal horn for your team, rename them "goal_horn_XXX" with the team tricode and save them to the audio file. (e.g. "goal_horn_DAL" for Dallas Stars)

# Delay
You will be prompted to enter a delay that works with your stream. You may also edit "settings.txt" to create a default option. Make sure the delay is entered in Line 3.

# Credit
Thank you to arim215 for the original code. The NHL changed their API in 2023 and this program was adapted from arim215's original work. https://github.com/arim215/nhl_goal_light

# Known Issues
Goal horn does not play in after OT goals. Working on a solution.

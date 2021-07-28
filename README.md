# tempus-py

python script to get tempus jump network player and map stats

## setup

tempus.py requires the [requests](https://pypi.org/project/requests/) python library.

you can install it with `pip install requests`

## usage

Start the script with a python runtime. The terminal prompts will direct you in using the features.

Alternatively, you can also pass arguments at launch to immediately lookup players or maps:

`tempus.py -m MAPNAME` will search for maps containing the string 'mapname'

`tempus.py -p PLAYERNAME` will search for players whose name contains the string 'playername'
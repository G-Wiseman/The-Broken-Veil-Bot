"""
Various Commands and logic for the main function to call on so that it remains
uncluttered.
"""

import dice
import os
import discord
import json
import datetime

def get_key():
    """
    Reads the key to log into the Baator Bot, from  config.json,
    since this is going on Github.
    """
    j_handle = open(".env")
    config = json.load(j_handle)
    j_handle.close()
    return config["key"]

def rollstats():
    string = "Stats are\n-----------\n"
    for loop in range(0,6):
        dropped, three_six = dice.four_six_drop()
        stat = sum(three_six)
        string += ("**" + str(stat) + "** ")
        string += (str(three_six) + " {" + str(dropped) + "}\n")
    return string

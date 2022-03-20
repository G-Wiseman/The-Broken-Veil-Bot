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
    j_handle = open("config.json")
    config = json.load(j_handle)
    j_handle.close()
    return config["key"]

def commands(command):
    if command == "rollstats":
        return dice.rollstats()
    if command == "ping":
        return "<legham:939388158443941898>"

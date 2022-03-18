import dice
import os
import discord
import json

def get_key():
    j_handle = open("config.json")
    config = json.load(j_handle)
    j_handle.close()
    return config["key"]

def commands(command):
    if command == "rollstats":
        return dice.rollstats()
    if command == "ping":
        return "<legham:939388158443941898>"

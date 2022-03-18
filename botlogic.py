import dice
import os
import discord

def commands(command):
    if command == "rollstats":
        return dice.rollstats()
    if command == "ping":
        return "<:legham:939388158443941898>"

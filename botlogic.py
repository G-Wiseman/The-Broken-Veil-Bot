"""
Various Commands and logic for the main function to call on so that it remains
uncluttered.
"""

import dice
import os
import discord
import json
from datetime import datetime
import pickle
from Character import *


def get_key():
    """
    Reads the key to log into the Baator Bot, from .env,
    since this is going on Github. Wouldn't want to share the
    key that gives access to my bot.
    """
    j_handle = open(".env")
    config = json.load(j_handle)
    j_handle.close()
    return config["key"]

def rollstats() -> str:
    string = "Stats are\n-----------\n"
    for loop in range(0,6):
        dropped, three_six = dice.four_six_drop()
        stat = sum(three_six)
        string += ("**" + str(stat) + "** ")
        string += (str(three_six) + " {" + str(dropped) + "}\n")
    return string


def guild_filename(guild, file_flag ,extension):
    """
    Creates the name of a file for a guild's character stats file
    """
    guild_title = guild.name + str(guild.id)
    title = guild_title + file_flag + extension
    return title

def create_backup_title(guild, extension):
    """
    Creates a back-up file title, based on the
    guild and the time the back-up was created to
    avoid any possible overwriting of files
    """

    cur_time = datetime.now()
    time_title = cur_time.strftime("%d-%m-%Y %H.%M.%S")
    guild_title = guild.name + str(guild.id)
    title = time_title + guild_title + "BACKUP" + extension
    return title

def is_char_owner(author, character)->bool:
    """
    Determines if a user is the owner of a character.
    Returns True if the the user is the owner.
    False otherwise.
    """
    return author.id == character.owner_id

def set_get_type(type):
    setter = None
    getter = None
    official_type = None


    if type == "Character Specific":
        setter = Character.set_spec_count
        getter = Character.get_spec_count

    elif type == "Kills":
        official_type = "Kills"
        getter = Character.get_kills
        setter = Character.set_kills

    elif type == "Unconscious":
        official_type = "Times Unconscious"
        getter = Character.get_unconc
        setter = Character.set_unconc

    elif type in "Deaths":
        official_type = "Deaths"
        getter = Character.get_deaths
        setter = Character.set_deaths

    elif type == "Final Kill":
        official_type = "\"How do you want to this\""
        getter = Character.get_finals
        setter = Character.set_finals

    elif type == "Max Damage" :
        getter = Character.get_max_damage
        setter = Character.set_max_damage
        official_type = "Damage in a single turn"

    elif type == "Healing Dealt":
        official_type = "Healing dealt"
        getter = Character.get_healing
        setter = Character.set_healing

    elif type == "Nat 20":
        official_type = "Natural Twenties"
        getter = Character.get_crit_success
        setter = Character.set_crit_success

    elif type == "Nat 1":
        official_type = "Natural Ones"
        getter = Character.get_crit_fail
        setter = Character.set_crit_fail

    print(setter)
    return setter, getter, official_type


def handle_log(char_name, type_stat, new_value, guild):
    """
    Handles the logging stats logic. Returns values for the
    prior and new values of the stat_type that was changed
    """
    g_filename = guild_filename(guild, "STATS" ,".pkl")
    chars_dict = unpickle(g_filename)
    if (chars_dict == None) or (char_name.lower() not in chars_dict.keys()):
        return

    character = chars_dict[char_name.lower()]


    setter, getter, logged_type = set_get_type(type_stat)

    if logged_type == "Damage in a single turn":
        cur_value = getter(character)
        if cur_value < new_value:
            setter(character, new_value)

    else:
        cur_value = getter(character)
        new_value += cur_value
        setter(character, new_value)


    chars_dict[char_name] = character

    repickle(chars_dict, g_filename)
    return cur_value, new_value


### The Pickling and Unpickling
def unpickle(filename):
    """
    Loads from a pickle file, unless the file is empty,
    and then it returns None
    """
    try:
        with open(filename, "rb") as pkl_file:
            try:
                unpickled =  pickle.load(pkl_file)
                return unpickled
            except EOFError as e:
                print(e)
                return None
    except FileNotFoundError as e:
        print("File not found error happened when unpickling")
        return None

def repickle(obj, filename:str)->None:
    """
    Stores a Python object into a pkl file. Overwrites anything currently
    in the file.
    """
    with open(filename, "wb") as pkl_file:
            pickle.dump(obj, pkl_file, -1)

def char_class_refresh(guilds)-> None:
    for guild in guilds:
        filename = guild_filename(guild, "STATS",".pkl")
        chars_dict = unpickle(filename)
        if chars_dict != None:
            new_dict = {}
            for character in chars_dict.values():
                new_char = remake_char(character)
                single_dict = {new_char._name.lower(): new_char}
                new_dict.update(single_dict)
            repickle(new_dict, filename)

def get_leaderboard_list(guild, stat_type) -> list:

    guild_name = guild_filename(guild, "STATS",".pkl")
    chars_dict = unpickle(guild_name)

    setter, getter, official_type = set_get_type(stat_type)

    character_stat_list = []
    for character in chars_dict.values():
        stat_value = getter(character)
        new_tup = (stat_value, character)
        character_stat_list.append(new_tup)

    character_stat_list.sort(reverse=True)
    return character_stat_list

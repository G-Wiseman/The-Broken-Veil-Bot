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

def guild_filename(guild, extension):
    """
    Creates the name of a file for a guild's character stats file
    """
    guild_title = guild.name + str(guild.id)
    title = guild_title + "STATS" + extension
    return title

def set_get_type(type, character):
    alias_dict = create_alias_dict()
    setter = None
    getter = None
    official_type = None

    if type.lower() in alias_dict["kill_alias"]:
        official_type = "Kill"
        getter = character.get_kills
        setter = character.set_kills

    elif type.lower() in alias_dict["unconc_alias"]:
        official_type = "Time Unconscious"
        getter = character.get_uncon
        setter = character.set_unconc

    elif type.lower() in alias_dict["death_alias"]:
        official_type = "Death"
        getter = character.get_deaths
        setter = character.set_deaths

    elif type.lower() in alias_dict["final_alias"]:
        official_type = "\"How do you want to this\""
        getter = character.get_finals
        setter = character.set_finals

    elif type.lower() in alias_dict["max_damage_alias"]:
        getter = character.get_max_damage
        setter = character.set_max_damage
        official_type = "Damage in a single turn"

    elif type.lower() in alias_dict["healing_alias"]:
        official_type = "Healing dealt"
        getter = character.get_healing
        setter = character.set_healing

    elif type.lower() in alias_dict["crit_success_alias"]:
        official_type = "Natural Twenty"
        getter = character.get_crit_success
        setter = character.set_crit_success

    elif type.lower() in alias_dict["crit_fail_alias"]:
        official_type = "Natural One"
        getter = character.get_crit_fail
        setter = character.set_crit_fail

    elif type.lower() == character._chara_specific_type.lower():
        official_type = character._chara_specific_type
        setter = character.set_spec_count
        getter = character.get_spec_count

    return setter, getter, official_type


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

def create_alias_dict():
    """
    Creates a dictionary of all the different allowed
    ways of specifying which stat is being referred to.
    """
    kill_alias =        ['kill', 'kills']
    unconc_alias =      ['ko', 'uncon', 'unconc', 'unc', 'unconscious', 'knocked', 'down']
    death_alias =       ['dead', 'death', 'deaths', 'died']
    final_alias =       ['final', 'hdywtdt', 'finalkill', 'how']
    max_damage_alias =  ['damage', 'maxdamage', 'max']
    healing_alias =     ['healed', 'heal', 'healing']
    crit_success_alias= ["20", 'nat20', 'bigsucc', 'bigsuccess']
    crit_fail_alias =   ['1', 'nat1', 'bigfail']

    alias_dict = {
    "kill_alias":kill_alias,
    "unconc_alias":unconc_alias,
    "death_alias":death_alias,
    "final_alias":final_alias,
    "max_damage_alias":max_damage_alias,
    "healing_alias":healing_alias,
    "crit_success_alias":crit_success_alias,
    "crit_fail_alias":crit_fail_alias
    }
    return alias_dict

def handle_log(character, type, new_value):
    """
    Handles the logging stats logic.
    """
    setter, getter, logged_type = set_get_type(type, character)

    if logged_type == "Damage in a single turn":
        cur_value = getter()
        if cur_value < new_value:
            setter(new_value)

    else:
        cur_value = getter()
        new_value += cur_value
        setter(new_value)

    return character, logged_type

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

def char_class_refresh(guilds):
    for guild in guilds:
        filename = guild_filename(guild, ".pkl")
        chars_dict = unpickle(filename)
        if chars_dict != None:
            new_dict = {}
            for character in chars_dict.values():
                new_char = remake_char(character)
                single_dict = {new_char._name: new_char}
                new_dict.update(single_dict)
            repickle(new_dict, filename)

def rollstats() -> str:
    string = "Stats are\n-----------\n"
    for loop in range(0,6):
        dropped, three_six = dice.four_six_drop()
        stat = sum(three_six)
        string += ("**" + str(stat) + "** ")
        string += (str(three_six) + " {" + str(dropped) + "}\n")
    return string

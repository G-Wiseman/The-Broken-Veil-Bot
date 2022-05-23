"""
Various Commands and logic for the main function to call on so that it remains
uncluttered.
"""

import dice
import os
import discord
import json
import datetime
import pickle
import Character


def create_alias_dict():
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

def handle_log(character, type, count):

    alias_dict = create_alias_dict()
    logged_type = None
    if type.lower() in alias_dict["kill_alias"]:
        logged_type = "Kill"
        character._kills += count

    elif type.lower() in alias_dict["unconc_alias"]:
        logged_type = "Time Unconscious"
        character._unconc += count

    elif type.lower() in alias_dict["death_alias"]:
        logged_type = "Death"
        character._deaths += count

    elif type.lower() in alias_dict["final_alias"]:
        logged_type = "\"How do you want to this\""
        character._final_kills += count

    elif type.lower() in alias_dict["max_damage_alias"]:
        if character._max_damage_dealt < count:
            character._max_damage_dealt = count
        logged_type = "Damage in a single turn"

    elif type.lower() in alias_dict["healing_alias"]:
        logged_type = "Healing dealt"
        character._healing_dealt += count

    elif type.lower() in alias_dict["crit_success_alias"]:
        logged_type = "Natural Twenty"
        character._crit_success += count

    elif type.lower() in alias_dict["crit_fail_alias"]:
        logged_type = "Natural One"
        character._crit_fail += count

    elif type.lower() == character._chara_specific_type.lower():
        logged_type = character._chara_specific_type
        character._chara_specific_count += count

    return character, logged_type

def get_key():
    """
    Reads the key to log into the Baator Bot, from  config.json,
    since this is going on Github.
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
    with open(filename, "rb") as pkl_file:
        try:
            unpickled =  pickle.load(pkl_file)
            return unpickled
        except EOFError as e:
            print(e)
            return None

def repickle(obj, filename:str) ->None:
    """
    Stores a Python object into a pkl file. Overwrites anything currently
    in the file.
    """
    with open(filename, "wb") as pkl_file:
            pickle.dump(obj, pkl_file, -1)

def rollstats():
    string = "Stats are\n-----------\n"
    for loop in range(0,6):
        dropped, three_six = dice.four_six_drop()
        stat = sum(three_six)
        string += ("**" + str(stat) + "** ")
        string += (str(three_six) + " {" + str(dropped) + "}\n")
    return string

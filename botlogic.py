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



def handle_log(character, type, count):
    kill_alias = ['kill', 'kills']
    unconc_alias = ['uncon', 'unconc', 'unc', 'unconscious', 'knocked', 'down', 'ko']
    death_alias = ['dead', 'death', 'deaths', 'died']
    final_alias = ['final', 'hdywtdt', 'finalkill']
    max_damage_alias = ['damage', 'maxdamage', 'max']
    healing_alias = ['healed', 'heal', 'healing']
    crit_success_alias = ["20", 'nat20', 'bigsucc', 'bigsuccess']
    crit_fail_alias = ['1', 'nat1', 'bigfail']

    if type.lower() in kill_alias:
        character._kills += count

    elif type.lower() in unconc_alias:
        character._unconc += count

    elif type.lower() in death_alias:
        character._deaths += count

    elif type.lower() in final_alias:
        character._final_kills += count

    elif type.lower() in max_damage_alias:
        if character._max_damage_dealt < count:
            character._max_damage_dealt = count

    elif type.lower() in healing_alias:
        character._healing_dealt += count

    elif type.lower() in crit_success_alias:
        character._crit_success += count

    elif type.lower() in crit_fail_alias:
        character._crit_fail += count

    elif type.lower() == character._chara_specific_type.lower():
        character._chara_specific_count += count

    return character

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
    An error handling pi
    Loads from a pickle file, unless the file is empty,
    and then it returns None.
    """
    with open(filename, "rb") as pkl_file:
        try:
            unpickled =  pickle.load(pkl_file)
            return unpickled
        except EOFError as e:
            print(e)
            return None

def rollstats():
    string = "Stats are\n-----------\n"
    for loop in range(0,6):
        dropped, three_six = dice.four_six_drop()
        stat = sum(three_six)
        string += ("**" + str(stat) + "** ")
        string += (str(three_six) + " {" + str(dropped) + "}\n")
    return string

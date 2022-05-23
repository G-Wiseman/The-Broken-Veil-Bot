#!/usr/bin/env python3
import discord
from discord.ext import commands
import os
import botlogic as bl
import pickle
import datetime
from Character import *

doggled = False #The "Doggle" is the toggle to remove any messages with the annoying dog emoji when it is toggled on
bot = commands.Bot(command_prefix='!', case_insensitive=True)
bot.name = "The Broken Veil"


@bot.event
async def on_ready():

    print(f"We have logged in as {bot.name}".format())

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

    if "<:Chihuaxander:951361274774716486>" in message.content and doggled:
        await message.delete()

@bot.command()
async def ping(ctx):
	await ctx.send("<:legham:939388158443941898>")

@bot.command(name="roll-stats")
async def roll_character_stats(ctx):
    await ctx.send(bl.rollstats())

@bot.command(name="NameTest")
async def nametest(ctx, real=False):
    sender = ctx.author
    if real == "Real":
        sender_name = sender.name
    else:
        sender_name = sender.display_name
    await ctx.send(sender_name)

@bot.command(name="Doggle")
async def blockChihuahua(ctx, switchDirection=None):
    global doggled

    if switchDirection.lower() == "on":
        doggled = True
    elif switchDirection.lower() == "off":
        doggled = False
    else:
        doggled = not doggled

    if doggled == True:
        on_off = "on"
    else:
        on_off = "off"
    await ctx.send(f"The blocking has been doggled {on_off}")

@bot.command(name="log")
async def logStats(ctx, char_name, type, count=1):

    chars_dict = bl.unpickle("Character_Stats.pkl")
    char_name = char_name.lower()

    if (chars_dict == None) or (char_name not in chars_dict.keys()):
        await ctx.send(f"**Failed** The character {char_name} doesn't exist.")
        return

    found_char = chars_dict[char_name]

    updated_char, logged_type = bl.handle_log(found_char, type, count)

    chars_dict[char_name] = updated_char

    bl.repickle(chars_dict, "Character_Stats.pkl")

    await ctx.send(f"{count} {logged_type}(s) has been logged for {char_name}")
    return

@bot.command(name="ShowStats")
async def show_character_stat_display(ctx, char_name):
    char_name = char_name.lower()

    chars_dict = bl.unpickle("Character_Stats.pkl")
    if (chars_dict == None) or (char_name not in chars_dict.keys()):
        await ctx.send(f"**Failed** The character {char_name} doesn't exist.")
        return

    character = chars_dict[char_name]
    await ctx.send(character.show_current_stats())

@bot.command(name="DeleteCharacter")
async def delete_char(ctx, char_name):
    await ctx.send("Hasn't been implemented yet. Go bug George...")
    return

@bot.command(name="CreateCharacter")
async def create_character_stats_sheet(ctx, char_name=None, char_specific_stat=None):
    if char_name == None:
        await ctx.send("Your Character needs a name\n Try !CreateCharacter \"Name\"")
        return

    if char_specific_stat== None:
        await ctx.send("**Failed** Your Character could use a personalized stat\nTry !CreateCharacter \"Character Name\" \"Name of Personalized Stat\"")
        return

    caller_id = ctx.author.id
    chars_dict = bl.unpickle("Character_Stats.pkl")
    if chars_dict == None:
        chars_dict = {}

    #Check if the character already exists
    if char_name not in chars_dict.keys():
        #Add the character to the dictionary
        new_char = Character(char_name, specific_stat=char_specific_stat, owner=caller_id)
        new_char_temp_dict = {new_char._name.lower() : new_char}
        chars_dict.update(new_char_temp_dict)
    else:
        #Alert the user that the character already exists, then abort
        await ctx.send(f"Cannot Create Character. The character {char_name} already exists.\nUse **!DeleteCharacter \"{char_name}\"** to delete the character that already exists.")
        return


    bl.repickle(chars_dict, "Character_Stats.pkl")


    await ctx.send(f"{char_name} created, with a personalized stat of {char_specific_stat}")
    return

@bot.command(name="CharacterList")
async def char_list_output(ctx):

    chars_dict = bl.unpickle("Character_Stats.pkl")
    output_string = "Characters in this server\n-----\n"
    for character in chars_dict.values():
        output_string += f"{character._name}: Personal Stat is *{character._chara_specific_type}*\n"

    await ctx.send(output_string)






key = bl.get_key()
bot.run(key)

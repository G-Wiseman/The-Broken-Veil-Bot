#!/usr/bin/env python3
import discord
from discord.ext import commands
import os
import botlogic
import json
import datetime
from Character import *

doggled = False #The "Doggle" is the toggle to remove any messages with the annoying dog emoji when it is toggled on
bot = commands.Bot(command_prefix='!')
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
    await ctx.send(botlogic.rollstats())

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

@bot.command(name="Log")
async def logStats(ctx, char_name, type, count):
    return

@bot.command(name="CreateCharacter")
async def create_character_stats_sheet(ctx, char_name=None, char_specific_stat=None):
    if char_name == None:
        await ctx.send("Your Character needs a name\n Try !CreateCharacter \"Name\"")
        return

    if char_specific_stat== None:
        await ctx.send("Your Character could use a personalized stat\n Try !CreateCharacter \"Character Name\" \"Name of Personalized Stat\"")
        return

    caller_id = ctx.author.id
    new_char = Character(char_name, specific_stat=char_name, owner=caller_id)

    with open("Characters.json", "w+") as file:
        try:
            file_data = json.load(file)
        except Exception as e:
            print(e)
            file_data = {}

        json_new_char = new_char.json_prepare()
        print(file_data)

        file_data.update(json_new_char)
        dump = json.dumps(file_data)
        file.write(dump)


    await ctx.send(f"{char_name} created, with a personalized stat of {char_specific_stat}")
    return


key = botlogic.get_key()
bot.run(key)

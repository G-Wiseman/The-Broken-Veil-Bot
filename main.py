#!/usr/bin/env python3
import discord
from discord.ext import commands
import os
import botlogic
import json
import datetime

doggled = True #The Doggle is the toggle to remove any messages with the annoying dog emoji when it is toggled on
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
    if switchDirection == None:
        doggled = not doggled
    elif switchDirection.lower() == "on":
        doggled = True
    elif switchDirection.lower() == "off":
        doggled = False

    if doggled == True:
        on_off = "on"
    else:
        on_off = "off"
    await ctx.send(f"The blocking has been doggled {on_off}")

key = botlogic.get_key()
bot.run(key)

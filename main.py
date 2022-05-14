#!/usr/bin/env python3
import discord
from discord.ext import commands
import os
import botlogic
import json
import datetime

bot = commands.Bot(command_prefix='!')
bot.name = "Baator-Bot"

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.name}".format())

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

    if "<:Chihuaxander:951361274774716486>" in message.content:
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


key = botlogic.get_key()
bot.run(key)

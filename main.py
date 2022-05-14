#!/usr/bin/env python3
import discord
from discord.ext import commands
import os
import botlogic
import json
import datetime

bot = commands.Bot(command_prefix="!")
bot.name = "Baator-Bot"

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.name}".format(client))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "<:Chihuaxander:951361274774716486>" in message.content:
        await message.delete()

@bot.command(name="ping")
async def some_crazy_function_name(ctx):
	await ctx.channel.send("pong")

key = botlogic.get_key()
bot.run(key)

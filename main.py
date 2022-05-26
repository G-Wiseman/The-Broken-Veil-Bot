#!/usr/bin/env python3
import discord
from discord.ext import commands
import os
import botlogic as bl
import pickle
import datetime
import re
from Character import *

doggled = False #The "Doggle" is the toggle to remove any messages with the annoying dog emoji when it is toggled on
bot = commands.Bot(command_prefix='!', case_insensitive=True)
bot.name = "The Broken Veil"


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.name}")
    bl.char_class_refresh(bot.guilds)
    print(f"All Guilds have refreshed characters")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

    if "<:Chihuaxander:951361274774716486>" in message.content and doggled:
        await message.delete()
@bot.command(name="at_test")
async def attest(ctx, the_at):
    print(the_at)

@bot.command()
async def ping(ctx):
	await ctx.send("<:legham:939388158443941898>")

@bot.command(name="roll-stats")
async def roll_character_stats(ctx):
    await ctx.send(bl.rollstats())

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
async def logStats(ctx, char_name, type, count=1):

    guild_filename = bl.guild_filename(ctx.guild, ".pkl")
    chars_dict = bl.unpickle(guild_filename)
    if (chars_dict == None) or (char_name.lower() not in chars_dict.keys()):
        await ctx.send(f"**Failed** The character {char_name} doesn't exist.")
        return

    found_char = chars_dict[char_name.lower()]

    updated_char, logged_type = bl.handle_log(found_char, type, count)

    chars_dict[char_name] = updated_char

    bl.repickle(chars_dict, guild_filename)
    await ctx.send(f"{count} {logged_type}(s) has been logged for {updated_char.get_name()}")
    return

@bot.command(name="ShowStats")
async def show_character_stat_display(ctx, char_name):
    char_name = char_name.lower()

    guild_filename = bl.guild_filename(ctx.guild, ".pkl")
    chars_dict = bl.unpickle(guild_filename)
    if (chars_dict == None) or (char_name.lower() not in chars_dict.keys()):
        await ctx.send(f"**Failed** The character {char_name} doesn't exist.")
        return

    character = chars_dict[char_name]
    await ctx.send(character.show_current_stats())

@bot.command(name="ReleaseCharacter")
async def unclaim_character(ctx, char_name):
    """
    Releases a character from the ownership of a user.
    When a character is released, anyone can then claim the
    character as their own.
    """

    guild_filename = bl.guild_filename(ctx.guild, ".pkl")
    chars_dict = bl.unpickle(guild_filename)
    if (chars_dict == None) or (char_name.lower() not in chars_dict.keys()):
        await ctx.send(f"**Failed** The character {char_name} doesn't exist.")
        return

    character = chars_dict[char_name.lower()]
    if character.get_owner_id() != ctx.author.id:
        await ctx.send(f"**Failed** {char_name} does not belong to you!")
        return

    character.set_owner_id(None)
    chars_dict[char_name.lower()] = character
    bl.repickle(chars_dict, guild_filename)

    await ctx.send(f"{char_name} no longer belongs to anyone. Use *!ClaimCharacter {char_name}* to claim them")
    return

@bot.command(name="ClaimCharacter")
async def delete_char(ctx, char_name):
    guild_filename = bl.guild_filename(ctx.guild, ".pkl")
    chars_dict = bl.unpickle(guild_filename)
    if (chars_dict == None) or (char_name.lower() not in chars_dict.keys()):
        await ctx.send(f"**Failed** The character {char_name} doesn't exist.")
        return

    character = chars_dict[char_name.lower()]
    if character.get_owner_id() != None:
        await ctx.send(f"**Failed** {char_name} is not claimable!")
        return

    character.set_owner_id(ctx.author.id)
    chars_dict[char_name.lower()] = character
    bl.repickle(chars_dict, guild_filename)

    await ctx.send(f"{char_name} now belongs to {ctx.author.name}")
    return

@bot.command(name = "GiveCharacter")
async def give_char(ctx, char_name, mention):
    """
    Give a character, that belongs to you, to someone else who you mention.
    !GiveCharacter character-name @username
    """
    guild_filename = bl.guild_filename(ctx.guild, ".pkl")
    chars_dict = bl.unpickle(guild_filename)
    if (chars_dict == None) or (char_name.lower() not in chars_dict.keys()):
        await ctx.send(f"**Failed** The character {char_name} doesn't exist.")
        return

    character = chars_dict[char_name.lower()]
    if character.get_owner_id() != ctx.author.id:
        await ctx.send(f"**Failed** {char_name} is not yours to give!")
        return

    recieving_user = await handle_mention(mention)
    if recieving_user == None:
        await ctx.send("**Failed** You need to mention (@) someone to give them your character!")

    character.set_owner_id(recieving_user.id)
    chars_dict[char_name.lower()] = character
    bl.repickle(chars_dict, guild_filename)

    await ctx.send(f"{char_name} now belongs to {recieving_user.name}")
    return

@bot.command(name="DeleteCharacter")
async def delete_char(ctx, char_name):
    guild_filename = bl.guild_filename(ctx.guild, ".pkl")
    chars_dict = bl.unpickle(guild_filename)
    if (chars_dict == None) or (char_name.lower() not in chars_dict.keys()):
        await ctx.send(f"**Failed** The character {char_name} doesn't exist.")
        return

    character = chars_dict[char_name.lower()]
    if character.get_owner_id() != ctx.author.id:
        await ctx.send(f"**Failed** {char_name} does not belong to you!")
        return

    del chars_dict[char_name.lower()]
    bl.repickle(chars_dict, guild_filename)

    await ctx.send(f"{char_name} no longer exists. So long and thanks for all the fish!")
    return

@bot.command(name="CreateCharacter")
async def create_character_stats_sheet(ctx, char_name=None, char_specific_stat=None):
    if char_name == None:
        await ctx.send("**Failed** Your Character needs a name\n Try !CreateCharacter \"Name\"")
        return

    if char_specific_stat== None:
        await ctx.send("**Failed** Your Character could use a personalized stat\nTry !CreateCharacter \"Character Name\" \"Name of Personalized Stat\"")
        return

    guild_filename = bl.guild_filename(ctx.guild, ".pkl")
    caller_id = ctx.author.id
    chars_dict = bl.unpickle(guild_filename)
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


    bl.repickle(chars_dict, guild_filename)


    await ctx.send(f"{char_name} created, with a personalized stat of {char_specific_stat}")
    return

@bot.command(name="CharacterList")
async def char_list_output(ctx, keyword=None):

    guild_filename = bl.guild_filename(ctx.guild, ".pkl")
    chars_dict = bl.unpickle(guild_filename)
    if chars_dict == None:
        await ctx.send("No charactes exist in this server right now!")
    output_string = "Characters in this server\n-----\n"

    if keyword == None:
        for character in chars_dict.values():
            output_string += f"{character._name}: Personal Stat is *{character._chara_specific_type}*\n"

    elif keyword.lower() == "mine":
        for character in chars_dict.values():
            if character.get_owner_id() == ctx.author.id:
                output_string += f"{character._name}: Personal Stat is *{character._chara_specific_type}*\n"

    await ctx.send(output_string)

@bot.command(name="Backup")
async def backup_char_data(ctx):

    guild_filename = bl.guild_filename(ctx.guild, ".pkl")
    chars_dict = bl.unpickle(guild_filename)
    backup_text = ""
    for character in chars_dict.values():
        backup_text += character.show_current_stats()

    # Creates a readable overview of the character data
    backup_name = bl.create_backup_title(ctx.guild, ".txt")
    with open("BACKUPS/"+backup_name, "w+") as backup_file:
        backup_file.write(backup_text)

    #Creates a back up of the pkl file as well
    backup_pickle_name = bl.create_backup_title(ctx.guild, ".pkl")
    bl.repickle(chars_dict, "BACKUPS/"+backup_pickle_name)

    await ctx.send(f"Created back up files {backup_name} and {backup_pickle_name}")



### Some None Command Bot Functions
async def handle_mention(input_mention):
    """
    Takes the <@NUMBERS> generated with a mention, and
    returns a discord.user object. If the input string is not
    valid mentions, returns None.
    """
    regex = re.match("<@(.*)>", input_mention)

    user_id = regex.group(1)
    try:
        user = await bot.fetch_user(user_id)
    except  discord.NotFound as e:
        print(e)
        return None

    return user


#Now the bot's event loop should be run! It begins!
key = bl.get_key()
bot.run(key)

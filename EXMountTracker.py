# EXMountTracker.py
# Author: Abby Kloss
# TW: @heykloss

'''
Literally just a framework, everything happens in the cogs at this point
'''

import os
import sqlite3
import time
import discord
from discord.ext import commands
from dotenv import load_dotenv
#from google_images_search import GoogleImagesSearch
#from pretty_help import PrettyHelp, DefaultMenu

load_dotenv() # make sure you have all the things below filled out in your .env file
TOKEN    = os.getenv('DISCORD_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')

def get_prefix(bot, message):
    prefixes = ""
    con = sqlite3.connect('files/EXMountTracker.db')
    for row in con.cursor().execute("SELECT Prefix from Guilds where GuildID=?", (int(message.guild.id),)):
        prefixes = row[0]
    con.close()
    return prefixes

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=(get_prefix), case_insensitive=True, owner_id=int(ADMIN_ID), intents=intents)



# startup
extensionList = [
                'cogs.BotCommands',
                'cogs.Owner'
                ]

@bot.event
async def on_ready():
    print(f'{bot.user} is connected to the following guild(s):\n')
    for guild in bot.guilds:
        print(f'{guild.name} (id: {guild.id})')
    print(" ")
    for extension in extensionList:
        bot.load_extension(extension)

@bot.event
async def on_guild_join(guild):
    con = sqlite3.connect('files/EXMountTracker.db')
    cur = con.cursor()
    cur.execute("insert into Guilds values (?, ';')", (int(guild.id), ))
    con.commit()
    con.close()
    print(f'Connected to {guild.name} (id: {guild.id}) at '+ time.strftime("%H:%M:%S", time.localtime()))

@bot.event
async def on_guild_remove(guild):
    con = sqlite3.connect('files/EXMountTracker.db')
    cur = con.cursor()
    cur.execute("delete from Guilds where GuildID=?", (int(guild.id),))
    con.commit()
    con.close()



bot.run(TOKEN)
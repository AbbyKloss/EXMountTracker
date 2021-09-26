from discord.ext import commands
from random import choice
import sqlite3

class Info(commands.Cog, description="basic info"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='table', help='shows how we represent the mounts by name')
    async def table(self, ctx):
        string = '''```        ARR       |       HW        |       SB         |        ShB        
___________|______|__________|______|___________|______|__________|_______
   Word    |  DB  |   Word   |  DB  |   Word    |  DB  |   Word   |  DB   
___________|______|__________|______|___________|______|__________|_______
 Boreas    | ARRB | Demonic  | HWDe | Hallowed  | SBHa | Diamond  | ShBD
 Markab    | ARRM | Sophic   | HWDo | Euphonius | SBEu | Emerald  | ShBE
 Enbarr    | ARRE | Dark     | HWDa | Lunar     | SBLu | Light    | ShBL
 Gullfaxi  | ARRG | Warring  | HWWa | Auspicious| SBAu | Ruby     | ShBR
 Xanthos   | ARRX | Round    | HWRn | Legendary | SBLe | Shadow   | ShBS
 Aithon    | ARRA | Rose     | HWRo | Reveling  | SBRe | Innocent | ShBI
 Nightmare | ARRN | White    | HWWh | Blissful  | SBBl | Fae      | ShBF

note: not case sensitive```'''
        await ctx.reply(string, mention_author=False)

def setup(bot):
    bot.add_cog(Info(bot))
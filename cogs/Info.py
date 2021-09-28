from discord.ext.commands.core import has_permissions
from discord.ext import commands
import discord
import sqlite3

class Info(commands.Cog, description="basic info"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='table', help='shows how we represent the mounts by name')
    async def table(self, ctx):
        string = '''```      ARR     |     HW     |      SB       |     ShB     
_________|____|_______|____|__________|____|________|____
  Word   | DB |  Word | DB |  Word    | DB |  Word  | DB 
_________|____|_______|____|__________|____|________|____
Boreas   |ARRB|Demonic|HWDe|Hallowed  |SBHa|Diamond |ShBD
Markab   |ARRM|Sophic |HWDo|Euphonius |SBEu|Emerald |ShBE
Enbarr   |ARRE|Dark   |HWDa|Lunar     |SBLu|Light   |ShBL
Gullfaxi |ARRG|Warring|HWWa|Auspicious|SBAu|Ruby    |ShBR
Xanthos  |ARRX|Round  |HWRn|Legendary |SBLe|Shadow  |ShBS
Aithon   |ARRA|Rose   |HWRo|Reveling  |SBRe|Innocent|ShBI
Nightmare|ARRN|White  |HWWh|Blissful  |SBBl|Fae     |ShBF

note: not case sensitive```'''
        await ctx.reply(string, mention_author=False)

    @commands.command(name='prefix', help='change the prefix (ADMIN)', usage="<prefix>")
    @has_permissions(administrator=True)
    async def prefix(self, ctx, *args):
        if (args):
            con = sqlite3.connect('files/EXMountTracker.db')
            prefix = str(args[0][:5])
            con.cursor().execute("update Guilds set Prefix=? where GuildID=?", (prefix, int(ctx.guild.id), ))
            con.commit()
            con.close()
            await ctx.reply("Prefix changed to: `" + prefix + "`", mention_author=False)
        else:
            await ctx.reply("No prefix entered", mention_author=False)

    @commands.command(name='invite', help="invite me to another server")
    async def invite(self, ctx):
        await ctx.reply("Here's the link:\nhttps://discord.com/oauth2/authorize?client_id=891445253092036680&permissions=264192&scope=bot%20applications.commands", mention_author=False)

    @commands.command(name='embedPages', help='proto-help')
    async def embedPages(self, ctx):
        page1 = discord.Embed (
        title = 'Page 1/3',
        description = 'Description',
        colour = discord.Colour.orange()
        )
        page2 = discord.Embed (
            title = 'Page 2/3',
            description = 'Description',
            colour = discord.Colour.orange()
        )
        page3 = discord.Embed (
            title = 'Page 3/3',
            description = 'Description',
            colour = discord.Colour.orange()
        )
        
        pages = [page1, page2, page3]

        message = await ctx.send(embed = page1)
        await message.add_reaction('⏮')
        await message.add_reaction('◀')
        await message.add_reaction('▶')
        await message.add_reaction('⏭')

        def check(reaction, user):
            return user == ctx.author

        i = 0
        reaction = None

        while True:
            if str(reaction) == '⏮':
                i = 0
                await message.edit(embed = pages[i])
            elif str(reaction) == '◀':
                if i > 0:
                    i -= 1
                    await message.edit(embed = pages[i])
            elif str(reaction) == '▶':
                if i < 2:
                    i += 1
                    await message.edit(embed = pages[i])
            elif str(reaction) == '⏭':
                i = 2
                await message.edit(embed = pages[i])
            
            try:
                reaction, user = await self.wait_for('reaction_add', timeout = 30.0, check = check)
                await message.remove_reaction(reaction, user)
            except:
                break

        await message.clear_reactions()

def setup(bot):
    bot.add_cog(Info(bot))
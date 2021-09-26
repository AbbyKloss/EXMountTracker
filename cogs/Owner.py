import discord
from discord.ext import commands
from discord.ext import tasks

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='loadCog', hidden=True) # taken from https://gist.github.com/EvieePy/d78c061a4798ae81be9825468fe146be
    @commands.is_owner()
    async def load_cog(self, ctx, *, cog: str):
        """Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='unloadCog', hidden=True) # taken from https://gist.github.com/EvieePy/d78c061a4798ae81be9825468fe146be
    @commands.is_owner()
    async def unload_cog(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='reloadCog', hidden=True) # taken from https://gist.github.com/EvieePy/d78c061a4798ae81be9825468fe146be
    @commands.is_owner()
    async def reload_cog(self, ctx, *, cog: str):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name="ownerCheck", hidden=True)
    @commands.is_owner()
    async def owner_check(self, ctx):
        await ctx.send(f'howdy **{ctx.author.display_name}**!')

    @commands.command(name="testPrint", hidden=True)
    @commands.is_owner()
    async def test_print(self, ctx, *args):
        if args != ():
            printable = '{}'.format(' '.join(args))
            print('\n' + printable + '\n')
            await ctx.reply('done!', mention_author=False)


def setup(bot):
    bot.add_cog(Owner(bot))
import discord 
from discord.ext import commands

from music_cog import music_cog
from help_cog import help_cog

bot = commands.Bot(commands_prefix="!")

bot.add_cog(help_cog(bot))
bot.add_cog(music_cog(bot))

bot.run("MTMzMTIzMDUxMTQ1MTg2NTE4OA.GQ0u0A.QfcuIyQxcnMrEFrsTVr6t08F8gYv3WsMKX6CUc")
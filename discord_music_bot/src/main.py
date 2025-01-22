import discord
from discord.ext import commands
import os

from music_cog import music_cog
from help_cog import help_cog

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

bot.add_cog(help_cog(bot))
bot.add_cog(music_cog(bot))

bot.run("MTMzMTIzMDUxMTQ1MTg2NTE4OA.GQ0u0A.QfcuIyQxcnMrEFrsTVr6t08F8gYv3WsMKX6CUc")
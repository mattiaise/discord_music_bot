import discord
from discord.ext import commands
import asyncio
import logging

from music_cog import music_cog
from help_cog import help_cog

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

bot.remove_command('help')

@bot.event
async def on_ready():
    logging.info(f"Bot online come {bot.user}")
    activity = discord.Activity(type=discord.ActivityType.listening, name="delle uova")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    logging.info("Bot è pronto e in ascolto di comandi.")

async def main():
    async with bot:
        await bot.add_cog(help_cog(bot))
        await bot.add_cog(music_cog(bot))
        await bot.start("TOKEN")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot interrotto manualmente. Chiusura in corso...")
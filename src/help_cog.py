import discord 
from discord.ext import commands

class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.text_channel_text = []
        self.help_message = f"""        
```
General commands:
!help - displays all the available commands
!play <URL> - finds the song on youtube and plays it in your current channel.
!playlist - finds on youtube and plays the songs from the default playlist.
!skip - skips the current song being played
!pause - pauses the current song being played or resumes if already paused
!leave - disconnect the bot from the voice channel
```        
"""
        
    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                if channel.name == "bot-commands":
                    self.text_channel_text.append(channel)                
        await self.send_to_all(self.help_message)
        
    async def send_to_all(self, msg):
        for text_channel in self.text_channel_text:
            await text_channel.send(msg)
            
    @commands.command(name="help", help="Displays all the available commands")
    async def help(self, ctx):
        await ctx.send(self.help_message)
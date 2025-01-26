import discord
from discord.ext import commands 
import yt_dlp
from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.is_paused = False
        self.vc = None
        self.music_queue = []        
        self.YDL_OPTIONS = {
            'format': 'bestaudio/best',
            'noplaylist': True,    
            'quiet': True,           
            'extract_flat': True,      
            }
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
            }

    def search_yt(self, item):
        with yt_dlp.YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.sanitize_info(
                    ydl.extract_info(item, download=False))
            except Exception:
                return False
        return {'source': info['url'], 'title': info['title']}
    
    def play_next(self): 
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            self.music_queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else: 
            self.is_playing = False

    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()
                if self.vc == None:
                    await ctx.send("Could not connect to the voice channel")
                    return
            else: 
                await self.vc.move_to(self.music_queue[0][1])
            self.music_queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else: 
            self.is_playing = False
            
    @commands.command(name="play", aliases=["p", "playing"], help="Plays the selected song from youtube")
    async def play(self, ctx, *args):
        query = " ".join(args)
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("Connect to a voice channel!")
        elif self.is_paused:
            self.vc.resume()
        else: 
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Could not download the song. Incorrect format, try a different  keyword")
            else: 
                await ctx.send("Song added to the queue")
                self.music_queue.append([song, voice_channel])
                if self.is_playing == False:
                    await self.play_music(ctx)
                    
    @commands.command(name="pause", aliases=["ps", "resume", "r", "stop"], help="Pauses or resumes the current song being played")
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()
            
    @commands.command(name="skip", aliases=["s"], help="Skips the currently played song")
    async def skip(self, ctx, *args):
        if self.vc != None and self.vc:
            self.vc.stop()
            await self.play_music(ctx)
            
    @commands.command(name="leave", aliases=["disconnect", "d", "l", "quit"])
    async def leave(self, ctx, *args):
        self.is_playing = False
        self.is_paused = False
        self.music_queue.clear()
        await self.vc.disconnect()
        
    @commands.command(name="playlist", aliases=["pp"], help="Plays the default playlist")
    async def playlist(self, ctx, *args):
        voice_channel = ctx.author.voice.channel
        file_path = "./../songs.txt"
        with open(file_path, "r", encoding="utf-8") as file:
            for url in file:
                song = self.search_yt(url.strip())
                self.music_queue.append([song, voice_channel])     
        if self.is_playing == False:
            await self.play_music(ctx)
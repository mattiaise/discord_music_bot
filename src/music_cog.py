import discord
from discord.ext import commands
import yt_dlp
import asyncio

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

    async def connect_to_voice(self, ctx, voice_channel):
        if self.vc is None or not self.vc.is_connected():
            self.vc = await voice_channel.connect()
        else:
            await self.vc.move_to(voice_channel)

    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            await self.connect_to_voice(ctx, self.music_queue[0][1])
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
            if not song:
                await ctx.send("Could not download the song. Incorrect format, try a different keyword")
            else:
                await ctx.send("Song added to the queue")
                self.music_queue.append([song, voice_channel])
                if not self.is_playing:
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
        if self.vc is not None and self.vc.is_playing():
            self.vc.stop()
            await self.play_music(ctx)

    @commands.command(name="leave", aliases=["disconnect", "d", "l", "quit"])
    async def leave(self, ctx, *args):
        self.is_playing = False
        self.is_paused = False
        self.music_queue.clear()
        if self.vc is not None:
            await self.vc.disconnect()

    async def search_yt_async(self, url):
        return self.search_yt(url.strip())

    @commands.command(name="playlist", aliases=["pp"], help="Plays the default playlist")
    async def playlist(self, ctx, *args):
        voice_channel = ctx.author.voice.channel
        file_path = "./../playlists/prepartita.txt" if args == "prepartita" else "./../playlists/triste.txt"
        with open(file_path, "r", encoding="utf-8") as file:
            urls = [url.strip() for url in file]

        tasks = [self.search_yt_async(url) for url in urls]
        songs = await asyncio.gather(*tasks)

        for song in songs:
            if song:
                self.music_queue.append([song, voice_channel])

        if not self.is_playing:
            await self.play_music(ctx)
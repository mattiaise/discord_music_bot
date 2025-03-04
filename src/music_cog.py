import discord
from discord.ext import commands
import yt_dlp
import asyncio
import logging
import concurrent.futures
import collections
import functools
import random

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.is_paused = False
        self.vc = None
        self.music_queue = collections.deque()
        self.YDL_OPTIONS = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'extract_flat': True,
            'default_search': 'ytsearch',
        }
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
        self.song_cache = functools.lru_cache(maxsize=100)(self.search_yt)

    def search_yt(self, item):
        with yt_dlp.YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.sanitize_info(ydl.extract_info(item, download=False))
            except Exception as e:
                logging.error(f"Error searching YouTube: {e}")
                return None
        return {'source': info['url'], 'title': info['title']}

    def play_next(self):
        if self.music_queue:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            self.music_queue.popleft()
            self.vc.play(
                discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS),
                after=lambda e: self.play_next()
            )
        else:
            self.is_playing = False
            logging.info("No more songs in the queue.")

    async def connect_to_voice(self, ctx, voice_channel):
        try:
            if self.vc is None or not self.vc.is_connected():
                self.vc = await voice_channel.connect()
                logging.info(f"Connected to voice channel: {voice_channel.name}")
            else:
                await self.vc.move_to(voice_channel)
                logging.info(f"Moved to voice channel: {voice_channel.name}")
        except Exception as e:
            logging.error(f"Error connecting to voice channel: {e}")
            await ctx.send("Could not connect to the voice channel.")

    async def play_music(self, ctx):
        if self.music_queue:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            await self.connect_to_voice(ctx, self.music_queue[0][1])
            self.music_queue.popleft()
            self.vc.play(
                discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS),
                after=lambda e: self.play_next()
            )
        else:
            self.is_playing = False
            logging.info("Music queue is empty.")

    @commands.command(name="play", aliases=["p", "playing"], help="Plays the selected song from youtube")
    async def play(self, ctx, *args):
        query = " ".join(args)
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("Connect to a voice channel!")
            return
        if self.is_paused:
            self.vc.resume()
            logging.info("Resumed the music.")
            return
        loop = asyncio.get_running_loop()
        song = await loop.run_in_executor(self.executor, self.song_cache, query)
        if not song:
            await ctx.send("Could not download the song. Incorrect format, try a different keyword")
        else:
            await ctx.send("Song added to the queue")
            self.music_queue.append([song, voice_channel])
            logging.info(f"Added song to queue: {song['title']}")
            if not self.is_playing:
                await self.play_music(ctx)

    @commands.command(name="pause", aliases=["ps", "resume", "r", "stop"], help="Pauses or resumes the current song being played")
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
            logging.info("Paused the music.")
        elif self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()
            logging.info("Resumed the music.")

    @commands.command(name="skip", aliases=["s"], help="Skips the currently played song")
    async def skip(self, ctx, *args):
        if self.vc is not None and self.vc.is_playing():
            self.vc.stop()
            logging.info("Skipped the current song.")

    @commands.command(name="leave", aliases=["disconnect", "d", "l", "quit"])
    async def leave(self, ctx, *args):
        self.is_playing = False
        self.is_paused = False
        self.music_queue.clear()
        if self.vc is not None:
            await self.vc.disconnect()
            logging.info("Disconnected from the voice channel.")

    @commands.command(name="playlist", aliases=["pp"], help="Plays the default playlist")
    async def playlist(self, ctx, *args):
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.send("You need to be connected to a voice channel to use this command.")
            return
        voice_channel = ctx.author.voice.channel
        file_path = "./../playlists/playlist.txt"
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                urls = [url.strip() for url in file if url.strip()]
        except FileNotFoundError as e:
            logging.error(f"Playlist file not found: {e}")
            await ctx.send("Playlist file not found.")
            return
        random.shuffle(urls)
        loop = asyncio.get_running_loop()
        first_url = urls.pop(0)
        first_song = await loop.run_in_executor(self.executor, self.song_cache, first_url)
        if first_song:
            self.music_queue.append([first_song, voice_channel])
            logging.info(f"Added first song to queue: {first_song['title']}")
            if not self.is_playing:
                await self.play_music(ctx)
        else:
            await ctx.send("Could not load the first song in the playlist.")
            return
        semaphore = asyncio.Semaphore(2)
        async def load_song(url):
            async with semaphore:
                song = await loop.run_in_executor(self.executor, self.song_cache, url)
                if song:
                    self.music_queue.append([song, voice_channel])
                    logging.info(f"Added song to queue: {song['title']}")
                else:
                    logging.error(f"Could not load song: {url}")
        tasks = [load_song(url) for url in urls]
        async def run_tasks():
            await asyncio.gather(*tasks)
        asyncio.create_task(run_tasks())
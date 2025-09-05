# music.py
# imports
import asyncio
from collections import deque
import discord
from discord.ext import commands
from yt_dlp import YoutubeDL

# Options for yt-dlp downloader
ydl_opts = {
    'format': 'm4a/bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'source_address': '0.0.0.0',
    'postprocessors':
    [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
    }]
}

# Options for ffmpeg
ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

ydl = YoutubeDL(ydl_opts)

song_queue = deque()

# Searches for song
async def search_yt(query):
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(None, lambda: ydl.extract_info(query, download=False))

    # Takes first item from playlist
    if "entries" in data:
        data = data["entries"][0]

    song_queue.append({'title': data["title"], 'url': data["url"]})

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Music Commands
    @commands.command()
    async def play(self, ctx, *, args: str):
        """Connects to the user's voice channel and plays music"""
        vc = ctx.author.voice.channel

        # Join the voice channel
        if ctx.voice_client:
            await ctx.voice_client.move_to(vc)
        else:
            await vc.connect()

        # Search and play audio
        query = "ytsearch1:" + args
        await search_yt(query)
        if not (ctx.voice_client.is_playing() or ctx.voice_client.is_paused()):
            self.play_next_song(ctx)
        else:
            embed = discord.Embed(title="Queued Song")
            embed.description = f"Added {song_queue[-1]['title']} to queue in position {len(song_queue)}"
            await ctx.send(embed=embed)

    def play_next_song(self, ctx):
        """Plays next song in queue"""
        if not song_queue:
            return

        song = song_queue.popleft()
        title = song['title']
        url = song['url']

        source = discord.FFmpegOpusAudio(url, **ffmpeg_options)
        ctx.voice_client.play(source, after=lambda e: self.play_next_song(ctx))

        embed = discord.Embed(title="Now Playing")
        embed.description = title
        asyncio.run_coroutine_threadsafe(ctx.send(embed=embed), self.bot.loop) 
        
    @commands.command()
    async def pause(self, ctx):
        """Pauses audio"""
        ctx.voice_client.pause()

    @commands.command()
    async def unpause(self, ctx):
        """Unpauses audio"""
        ctx.voice_client.resume()

    @commands.command()
    async def skip(self, ctx):
        """Skips current track"""
        ctx.voice_client.stop()

    @commands.command()
    async def queue(self, ctx):
        """Displays the music queue"""
        if not song_queue:
            await ctx.send("The song queue is empty.")
        else:
            embed = discord.Embed(title="Song Queue")
            embed.description = '\n'.join([f"{song_queue.index(song) + 1}. {song['title']}" for song in song_queue])
            await ctx.send(embed=embed)

    @commands.command()
    async def leave(self, ctx):
        """Leaves the voice channel"""
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()

    @play.before_invoke
    @pause.before_invoke
    @unpause.before_invoke
    @skip.before_invoke
    @queue.before_invoke
    async def check_voice(self, ctx):
        # Check if the user is in a voice channel
        if ctx.author.voice is None:
            await ctx.reply("You must be in a voice channel to do this")
            raise commands.CommandError("Author not in voice channel")
        
async def setup(bot):
    print("Loading music")
    await bot.add_cog(Music(bot))
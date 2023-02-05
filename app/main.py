# bot.py
import os
import time
import glob
import random

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
voice_channel_id = int(os.getenv("VOICE_CHANNEL"))
ignored_bot_id = int(os.getenv("IGNORED_USER_ID"))
dev_text_channel_id = int(os.getenv("DEV_TEXT_CHANNEL_ID"))
dev_text_channel = None
directory = "app/audio"
file_types = ('aac', '*.flac', '*.mp3', '*.m4a', '*.opus',
              '*.vorbis', '*.wav')  # the tuple of file types

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(
    description="Relatively simple music bot example",
    intents=intents,
)
client = discord.Client()


# Create a list of audio files
os.chdir(directory)
audio_files_grabbed = []
for files in file_types:
    audio_files_grabbed.extend(glob.glob(files))
print(f"Audio files: {audio_files_grabbed}")


# Commands
@bot.slash_command(description="Sends the bot's latency.")
async def ping(ctx):
    await ctx.respond(f"Pong! Latency is {bot.latency}")


# Events
@bot.event
async def on_ready():
    global dev_text_channel
    print(f"{bot.user} has connected to Discord!")
    dev_text_channel = await bot.fetch_channel(dev_text_channel_id)


@bot.event
# when someone joins voice
async def on_voice_state_update(member, before, after):
    # We need this for audio to play for the newly connected user.
    time.sleep(0.2)
    if member.id == ignored_bot_id:  # Ignore bots, rewrite this
        return
    if after.channel is None:  # ignore state change if someone disconnects.
        return
    try:
        # Print some outputs
        print(f"User: {member.name}")
        print(f"Old Channel: {before.channel}")
        print(f"Current Channel: {after.channel}")
    except Exception as e:
        print(f"{e}")
        pass

    if after.channel.id == voice_channel_id:
        # Do nothing if before and after is same channel
        if before.channel is not None:
            if before.channel.id == after.channel.id:
                return
        # Random sound
        random_audio_file = random.choice(audio_files_grabbed)
        print(f"Random audio file is {random_audio_file}")
        await dev_text_channel.send(content=f"Playing {random_audio_file} for little {member.name}.")
        await connect_and_play_sound(after.channel, random_audio_file, member)


async def connect_and_play_sound(channel, sound, member):
    vc = await channel.connect()
    vc.play(
        discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(sound), volume=0.3
        )
    )
    print(f"{channel.members}")
    while vc.is_playing():
        # Fetch members in voice channel
        channel = await member.guild.fetch_channel(channel.id)
        # if no users in voice, stop playing
        if len(channel.members) <= 1:
            break
        time.sleep(0.1)
    await vc.disconnect()
    # User will be kicked after channel change. it is intended behaviour.
    await member.move_to(None)

bot.run(TOKEN)

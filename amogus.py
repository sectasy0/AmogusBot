#!/usr/bin/python3

from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.opus import load_opus
from os.path import join, exists
from os import getcwd
from random import choice
from asyncio import sleep

from settings import Settings

import ctypes.util

sett = Settings.from_json()
client = commands.Bot(command_prefix=sett.cmd_prefix)
script_path = getcwd()

client.settings: Settings = sett
client.currently_playing: bool = False


async def play_sound(ctx, file_name: str):
   opus = ctypes.util.find_library('opus')
   load_opus(opus)

   if not exists(f"sounds/{file_name}.mp3"):
      await ctx.send("This sound has been injected!")
      return

   if not ctx.author.voice and not ctx.author.voice.channel:
      await ctx.send(f"{ctx.author.name} is not in a voice channel")

   client.currently_playing = True

   voice_channel = ctx.author.voice.channel

   vc = await voice_channel.connect()
   vc.play(FFmpegPCMAudio(executable=join(script_path, "bin", "ffmpeg"), 
            source=join(script_path, "sounds", f"{file_name}.mp3")))

   while vc.is_playing():
      await sleep(.1)

   client.currently_playing = False

   await vc.disconnect()
   await ctx.message.delete()


async def get_task() -> str:
   return choice(client.settings.tasks)


@client.command(name='a')
async def a_command(ctx, arg):
   if not client.currently_playing:
      await play_sound(ctx, arg)
   else:
      await ctx.send(f"Amogus {await get_task()}, try in a while")


client.run(sett.app_token)
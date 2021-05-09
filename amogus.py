#!/usr/bin/python3

from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.opus import load_opus
from asyncio import sleep

from os.path import join, exists
from os import getcwd
from random import choice

import ctypes.util

client = commands.Bot(command_prefix="^")
script_path = getcwd()

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
   tasks = [
      "is fixes wires",
      "is fixes weather node",
      "making a burger",
      "is rebooting wifi",
      "is uploading data"
   ]
   return choice(tasks)

@client.command(name='a')
async def a_command(ctx, arg):
   if not client.currently_playing:
      await play_sound(ctx, arg)
   else:
      await ctx.send(f"Amogus {await get_task()}, try in a while")


client.run("your token here")
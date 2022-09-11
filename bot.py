import discord
import json
from discord.ext import commands

from music_cog import music_cog

def get_prefix(bot, message):
  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)
  return prefixes[str(message.guild.id)]

Bot = commands.Bot(command_prefix=get_prefix)

Bot.add_cog(music_cog(Bot))

@Bot.event
async def on_ready():
  await Bot.change_presence(status=discord.Status.dnd, activity=discord.Game('yo girl'))
  print('Bot is ready.')

@Bot.event
async def on_guild_join(guild):
  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)
  prefixes[str(guild.id)] = '!'

  with open('prefixes.json', 'w') as f:
    json.dump(prefixes, f, indent=4)

@Bot.event
async def on_guild_remove(guild):
  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)
  prefixes.pop(str(guild.id))

  with open('prefixes.json', 'w') as f:
    json.dump(prefixes, f, indent=4)

@Bot.command()
async def changeprefix(ctx, prefix):
  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)
  prefixes[str(ctx.guild.id)] = prefix

  with open('prefixes.json', 'w') as f:
    json.dump(prefixes, f, indent=4)

  await ctx.send(f'The prefix has been changed to {prefix}')

@Bot.command()
async def ping(ctx):
  await ctx.send(f'{round(Bot.latency * 1000)}ms')

token=""
with open("token.txt") as file:
    token = file.read()

Bot.run(token)
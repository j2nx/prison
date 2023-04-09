import discord, os, asyncio, datetime, inspect, sys, requests, ast, re, subprocess, json
from datetime import date
from discord.ext import commands, tasks
from discord.ext.commands import BucketType
from discord.ext.commands import Context

os.system("pip3 install git+https://github.com/Rapptz/discord.py")

#configs
tkn = os.getenv("TKN")
bot_prefix = ','
bot = commands.Bot(command_prefix=bot_prefix, intents=discord.Intents.all())
color = 0x2f3136
owner_ids = [981350984246771762, 1019234423742402560]
bot.remove_command("help")

#intents
intents = discord.Intents.default()
intents.members = True
intents.guilds = True


#start
@bot.event
async def on_ready() -> None:
  status_task.start()


@tasks.loop()
async def status_task() -> None:
  await bot.change_presence(activity=discord.Streaming(
    name=f"@prisoner#0001", url='https://www.twitch.tv/prisonantinuke'))
  await asyncio.sleep(10)
  await bot.change_presence(activity=discord.Streaming(
    name=f"bot coming soon", url='https://www.twitch.tv/prisonantinuke'))
  await asyncio.sleep(10)


@bot.event
async def on_member_join(member):
  await member.send("hi, {user} my prefix in this server is `,`")


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.member = None, *, reason=None):
  today = date.today()

  if member == None:
    local = discord.Embed(
      title=f"",
      description=
      f'''⚠️  {ctx.author.mention}: **YOU FORGOT TO ADD A USER** ''',
      color=color)
    await ctx.channel.send(embed=local)


  if reason == None:
    reason = "None"
    await ctx.guild.ban(member)
    await ctx.send(f'User {member.mention} was banned')
    await ctx.author.send(f'User {member} was banned on {today}')

  else:
    reason = reason
    await ctx.guild.ban(member)
    await ctx.send(f'User {member.mention} was banned')
    await ctx.author.send(f'User {member} was banned on {today}')


am = int()


@bot.command(aliases=['c', 'clear', 'clr'])
#@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount=am):
  if amount <= 0:
    author = ctx.author
    # await message.channel.send(author.avatar_url)
    bing = discord.Embed(color=0)
    bing.set_author(name='prison Help\n', icon_url=author.display_avatar)
    bing.add_field(name="Cmd : Purge",
                   value=f'''
‎ 
deletes amount of messages from the current channel.   
```
Syntax: {bot_prefix}purge <amount>
Example: {bot_prefix}purge (amount)
```

                    ''')
    await ctx.channel.send(embed=bing), 0x00
  else:
    await ctx.channel.purge(limit=amount), 0x00


@bot.command(aliases=['setav', 'setbotav'])
#@commands.owner_ids()
async def setbotpfp(ctx, *, url=None):
  if not url:
    if ctx.message.attachments:
      url = ctx.message.attachments[0].url
    else:
      em = discord.Embed(description=" > provide a valid image", color=color)
      return await ctx.send(embed=em)
  avatar = requests.get(url).content
  try:
    await bot.user.edit(avatar=avatar)
  except:
    em = discord.Embed(description=" > cant change pfp anymore", color=color)
    return await ctx.send(embed=em)
    em = discord.Embed(description=" > ive changed my profile picture",
                       color=color)
    return await ctx.send(embed=em)



@bot.command()
@commands.has_permissions(administrator=True)
@commands.cooldown(1, 200, commands.BucketType.member)
async def seticon(self, ctx, *, url=None):
  if not url:
    if ctx.message.attachments:
      url = ctx.message.attachments[0].url
    else:
      return await ctx.send(
        embed=discord.Embed(description="Provide a valid image", color=color))
    avatar = requests.get(url).content
    try:
      await ctx.guild.edit(icon=avatar)
    except:
      return

    await ctx.send(embed=discord.Embed(
      description="{ctx.author.mention}: Changed the Guild Icon", color=color))


@bot.command()
@commands.has_permissions(administrator=True)
@commands.cooldown(1, 200, commands.BucketType.member)
async def setbanner(self, ctx, *, url=None):
  if not url:
    if ctx.message.attachments:
      url = ctx.message.attachments[0].url
    else:
      return await ctx.send(
        embed=discord.Embed(description="Provide a valid image", color=color))
    banner = requests.get(url).content
    try:
      await ctx.guild.edit(banner=banner)
    except:
      return

    await ctx.send(embed=discord.Embed(
      description="{ctx.author.mention}: Changed the Guild Banner"))


@bot.command()
async def command(ctx):
  if ctx.author.id in owner_ids:
    await ctx.channel.send("you are owner / whitelisted")
  else:
    await ctx.channel.send("You are not owner or whitelisted")


@bot.command()
@commands.has_permissions(ban_members=True)
async def kick(ctx, member: discord.member = None, *, reason=None):
  today = date.today()

  if member == None:
    local = discord.Embed(
      title=f"",
      description=
      f'''⚠️  {ctx.author.mention}: **YOU FORGOT TO ADD A USER** ''',
      color=color)
    await ctx.channel.send(embed=local)

  if reason == None:
    reason = "None"
    await ctx.guild.kick(member)
    await ctx.send(f'User {member.mention} was kicked')
    await ctx.author.send(f'User {member} was kicked on {today}')
  else:
    reason = reason
    await ctx.guild.kick(member)
    await ctx.send(f'User {member.mention} was kicked')
    await ctx.author.send(f'User {member} was kicked on {today}')


@bot.command(pass_context=True)
async def banner(ctx, *, user: commands.UserConverter = None):

  if user == None:

    member = ctx.author

  else:

    member = user

  usr = await bot.fetch_user(member.id)

  if usr.banner:

    bannerEmbed = discord.Embed(
      description=f"[**{usr.name}'s banner**]({usr.banner.url})", color=color)

    bannerEmbed.set_image(url=usr.banner.url)

    await ctx.send(embed=bannerEmbed)

  else:

    await ctx.reply(mention_author=False,
                    embed=discord.Embed(
                      description="This user doesn't have a banner",
                      color=color))


@bot.command(pass_context=True)
async def av(ctx, *, user: commands.UserConverter = None):

  if user == None:

    member = ctx.author

  else:

    member = user

  usr = await bot.fetch_user(member.id)

  if usr.avatar:

    avatarEmbed = discord.Embed(
      description=f"[**{usr.name}'s avatar**]({usr.avatar.url})", color=color)

    avatarEmbed.set_image(url=usr.avatar.url)

    await ctx.send(embed=avatarEmbed)

  else:

    await ctx.reply(mention_author=False,
                    embed=discord.Embed(
                      description="This user doesn't have a avatar",
                      color=color))


@bot.command(aliases=['inv'])
async def invite(ctx):
  await ctx.send(embed=discord.Embed(
    description=
    " > **[prison's Invite](https://discord.com/oauth2/authorize?client_id=1082107560074674188&permissions=8&scope=bot%20applications.commands)**",
    color=color))
  try:
    return await ctx.author.send(embed=em)
  except:
    return await ctx.reply(embed=em)


@bot.command(aliases=['bi'])
async def botinfo(ctx, *, user: commands.UserConverter = None):
  embed = discord.Embed(description="**prison botinfo**", color=color)
  embed.add_field(
    name='Creators',
    value=f'`0x00#5909`,`prisoner#0001`,`luh micah#7126`',
    inline=True)
  embed.add_field(
    name='Guilds and Users',
    value=
    f'Users: `{len(set(bot.get_all_members()))}`\nTotal Guilds: `{len(bot.guilds)}`',
    inline=True)
  embed.add_field(name='Ping', value=f"`{round(bot.latency*1000)}ms`")
  embed.add_field(name='Library', value=f'`discord.py`', inline=True)
  embed.set_thumbnail(
    url=
    "https://media.discordapp.net/attachments/1093377999321170011/1094066705866702929/50c1d40094337f2d6383f828486ee4f5_1.png"
  )
  embed.set_footer(
    text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}',
    icon_url=ctx.author.avatar.url
    if ctx.author.avatar else ctx.author.default_avatar.url)
  await ctx.send(embed=embed)


@bot.command(aliases=['restart'])
async def reload(ctx):
  if ctx.author.id in owner_ids:
    await ctx.send(embed=discord.Embed(
      description=
      " > restarting bot <a:black_Typing_BlackDot:1093345271469051996>",
      color=color))
    subprocess.call(
      [sys.executable, os.path.realpath(__file__)] + sys.argv[1:])


@bot.command()
async def help(ctx):
  await ctx.send(embed=discord.Embed(
    description="> https://discord.gg/prisonbot \ for future cmds",
    color=color))


@bot.event
async def on_message(message):
  if message.content.lower() == f"<@!{bot.user.id}>" or message.content.lower(
  ) == f"<@{bot.user.id}>":
    await message.channel.send(embed=discord.Embed(
      description="> my prefix in this server is `,`", color=color))
  await bot.process_commands(message)


@bot.command(aliases=['setname', 'setbotname'])
@commands.check(lambda ctx: ctx.author.id in owner_ids)
async def setbotusername(ctx, *, name=None):
  if not name:
    em = discord.Embed(description=f" > please provide a valid username",
                       color=color)
    return await ctx.send(embed=em)
  try:
    await bot.user.edit(username=name)
  except:
    em = discord.Embed(description=f" > cant change username", color=color)
    return await ctx.send(embed=em)
    await ctx.send(embed=discord.Embed(
      description=" > My username has been updated to `{name}`"))


@bot.event
async def on_guild_join(guild):
  channel = bot.get_channel(channel_id)
  message = f"Joined {guild.name} `({guild.id})` owned by {guild.owner}, **{guild.member_count}** members"
  await channel.send(message)


@bot.event
async def on_guild_remove(guild):
  channel = bot.get_channel(channel_id2)
  message = f"Left {guild.name} `({guild.id})` owned by {guild.owner}, **{guild.member_count}** members"
  await channel.send(message)


channel_id = 1093639429006045357
channel_id2 = 1093639445913280532


@commands.command(aliases=["leave"])
@commands.is_owner()
@commands.cooldown(1, 5, commands.BucketType.user)
async def guildleave(self, ctx, *, guild: discord.Guild = None):
  if guild is None:
    guild = ctx.guild
    await ctx.message.delete()
    await guild.leave()




@bot.command()
async def hey(ctx):
  await ctx.send("hey guys!")
bot.run(tkn)

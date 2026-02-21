import discord
from discord import app_commands
from discord.ext import commands, tasks
from utils import mentionstrip
import asyncio

sniped_messages = {}

class snipe(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access

  @commands.Cog.listener()
  async def on_message_delete(self, message):
    if message.author != self.bot.user:
      sniped_messages[message.channel.id] = message # log most recent message in channel to sniped messages dictionary
      await asyncio.sleep(30)
      try:
        del sniped_messages[message.channel.id] # after 30 seconds, remove most recent message in channel from sniped messages
      except KeyError:
        pass

  @commands.hybrid_command(name="snipe", description="Snipe the most recent message in a channel, if one is found")
  @app_commands.allowed_installs(guilds=True, users=False)
  @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False) # Guilds, DMs, DMs/Group DMs
  @commands.has_permissions(manage_channels=True)
  async def snipe(self, ctx):
    try: #This piece of code is run if the bot finds anything in the dictionary
      files = []
      message = sniped_messages[ctx.channel.id]
      if (message.attachments != [] or message.stickers != []):
        if message.attachments != []:
          for i in message.attachments:
            files.append(await i.to_file())
        if message.stickers != []:
          for i in message.stickers:
            if isinstance(await i.fetch(), discord.GuildSticker): # can't reupload discord's lottie format stickers
              files.append(await i.to_file())
      await ctx.reply(content=f"{message.author.mention}:\n{await mentionstrip(ctx.guild, message.content)}\n", files=files, mention_author=False)
    except KeyError:
      await ctx.reply(f"Could not find a message from the last 30 seconds to snipe!", mention_author=False, ephemeral=True)

async def setup(bot):
  await bot.add_cog(snipe(bot=bot))
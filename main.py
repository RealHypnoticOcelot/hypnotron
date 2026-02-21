# -*- coding: utf8 -*-
import discord
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import dotenv_values

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or("h!"), case_insensitive=True, intents=intents, activity=discord.Game(name="I'm alive!"))
env_file = dotenv_values()

@bot.event
async def on_ready():
    print(f'Bot connected, logged in as {bot.user}, ID {bot.user.id}')

@bot.event
async def setup_hook():
	enabled_extensions = [
		"guessplace",
		"quotes",
		"hex",
		"echo",
		"addsticker",
		"hieroglyphify",
		"dice",
		"tomato",
		"ping",
		"savevoice",
		"wheel",
		"8ball",
		"coinflip",
		"slowmode",
		"pin",
		"delete",
		"inspire",
		"cat",
		"dog",
		"time",
		"xkcd",
		"wikipedia",
		"tiktok",
		"discordstatus",
		"tosdr",
		"google",
		"itemshop",
		"lockdown",
		"snipe",
		"logging.deleted_messages",
		"logging.edited_messages",
		"logging.moderation_actions",
		"logging.member_updates",
		"logging.voice_updates",
		"logging.server_voice_updates",
		"mindfulness"
	]
	for extension in enabled_extensions:
		await bot.load_extension("modules." + extension)

ignored = (commands.CommandNotFound, commands.BadLiteralArgument, commands.MissingRequiredArgument)

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, ignored):
		return
	else:
		raise error

@bot.hybrid_command(name="resync", with_app_command=True, description="Resync the commands!")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@commands.is_owner()
async def resync(ctx: commands.Context):
	await bot.tree.sync()
	await ctx.reply(content="Resynced slash commands!", mention_author=False, ephemeral=True)

bot.run(env_file['BOT_TOKEN'])
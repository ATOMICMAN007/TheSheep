import os
import platform
from glob import glob

from dotenv import load_dotenv
import discord
from discord.ext import commands

from discord import Webhook, AsyncWebhookAdapter
import aiohttp

from utils.json_handler import read_json

ul = read_json('secrets')['nuke_webhook']

# Discord user ID
OWNER_ID = 0

async def foo():
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(ul, adapter=AsyncWebhookAdapter(session))
        await webhook.send('Hello World', username='Foo')

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("."),
    owner_id=OWNER_ID,
    strip_after_prefix=True,
    intents=discord.Intents.all()
)


@bot.event
async def on_ready():
    pythonVersion = platform.python_version()
    dpyVersion = discord.__version__
    serverCount = len(bot.guilds)
    memberCount = len(set(bot.get_all_members()))

    embed = discord.Embed(
        title=f"{bot.user.name} Stats",
        description=":wave:",
        colour=discord.Colour.blurple()
    )

    embed.add_field(name="Python Version:", value=pythonVersion)
    embed.add_field(name="Discord.Py Version", value=dpyVersion)
    embed.add_field(name="Total Guilds:", value=serverCount)
    embed.add_field(name="Total Users:", value=memberCount)
    embed.add_field(name="Bot Developer:", value=f"<@{OWNER_ID}>")

    embed.set_footer(text=f"TheSheep | {bot.user.name}")
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)

    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(ul, adapter=AsyncWebhookAdapter(session))
        await webhook.send(embed=embed, username=bot.user.name)
    print('Bot Ready')


@bot.command(name='send', description='Send a webhook message')
async def _sii(ctx):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(ul, adapter=AsyncWebhookAdapter(session))
        embed = discord.Embed(
            title=bot.user.name,
            description="desc",
            colour=0xFFFFFF
        )
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.set_image(url=ctx.author.avatar_url)
        embed.set_footer(icon_url=ctx.author.avatar_url)
        await webhook.send(embed=embed,
                       username=ctx.author.display_name,
                       avatar_url=ctx.author.avatar_url
                       )

# Loading Cogs
# COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]

# for cog in COGS:
#     bot.load_extension(f'cogs/{cog}')

# Running the bot
load_dotenv()
bot.run(os.getenv('botToken'))

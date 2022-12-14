# -*- coding: utf8 -*-
from discord.ext import commands
import discord
import time as t
import asyncio
import datetime
import random
import re
from discord import app_commands, Interaction
from discord.app_commands import Choice
from typing import Literal
import typing
import mysql.connector
from PIL import Image, ImageFont, ImageDraw, ImageOps
from urllib.request import urlopen
import os
from io import BytesIO

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or("h!"), case_insensitive=True, intents=intents, status=discord.Status.do_not_disturb, activity=discord.Game(name="h!help"))

flagpairs = [("๐ฆ๐จ", "Ascension Island"), ("๐ฆ๐ฉ", "Andorra"), ("๐ฆ๐ช", "United Arab Emirates"), ("๐ฆ๐ซ", "Afghanistan"), ("๐ฆ๐ฌ", "Antigua & Barbuda"), ("๐ฆ๐ฎ", "Anguilla"), ("๐ฆ๐ฑ", "Albania"), ("๐ฆ๐ฒ", "Armenia"), ("๐ฆ๐ด", "Angola"), ("๐ฆ๐ถ", "Antarctica"), ("๐ฆ๐ท", "Argentina"), ("๐ฆ๐ธ", "American Samoa"), ("๐ฆ๐น", "Austria"), ("๐ฆ๐บ", "Australia"), ("๐ฆ๐ผ", "Aruba"), ("๐ฆ๐ฝ", "รland Islands"), ("๐ฆ๐ฟ", "Azerbaijan"), ("๐ง๐ฆ", "Bosnia & Herzegovina"), ("๐ง๐ง", "Barbados"), ("๐ง๐ฉ", "Bangladesh"), ("๐ง๐ช", "Belgium"), ("๐ง๐ซ", "Burkina Faso"), ("๐ง๐ฌ", "Bulgaria"), ("๐ง๐ญ", "Bahrain"), ("๐ง๐ฎ", "Burundi"), ("๐ง๐ฏ", "Benin"), ("๐ง๐ฑ", "St. Barthรฉlemy"), ("๐ง๐ฒ", "Bermuda"), ("๐ง๐ณ", "Brunei"), ("๐ง๐ด", "Bolivia"), ("๐ง๐ถ", "Caribbean Netherlands"), ("๐ง๐ท", "Brazil"), ("๐ง๐ธ", "Bahamas"), ("๐ง๐น", "Bhutan"), ("๐ง๐ป", "Bouvet Island"), ("๐ง๐ผ", "Botswana"), ("๐ง๐พ", "Belarus"), ("๐ง๐ฟ", "Belize"), ("๐จ๐ฆ", "Canada"), ("๐จ๐จ", "Cocos (Keeling) Islands"), ("๐จ๐ฉ", "Congo - Kinshasa"), ("๐จ๐ซ", "Central African Republic"), ("๐จ๐ฌ", "Congo - Brazzaville"), ("๐จ๐ญ", "Switzerland"), ("๐จ๐ฎ", "Cรดte D\โIvoire"), ("๐จ๐ฐ", "Cook Islands"), ("๐จ๐ฑ", "Chile"), ("๐จ๐ฒ", "Cameroon"), ("๐จ๐ณ", "China"), ("๐จ๐ด", "Colombia"), ("๐จ๐ต", "Clipperton Island"), ("๐จ๐ท", "Costa Rica"), ("๐จ๐บ", "Cuba"), ("๐จ๐ป", "Cape Verde"), ("๐จ๐ผ", "Curaรงao"), ("๐จ๐ฝ", "Christmas Island"), ("๐จ๐พ", "Cyprus"), ("๐จ๐ฟ", "Czechia"), ("๐ฉ๐ช", "Germany"), ("๐ฉ๐ฌ", "Diego Garcia"), ("๐ฉ๐ฏ", "Djibouti"), ("๐ฉ๐ฐ", "Denmark"), ("๐ฉ๐ฒ", "Dominica"), ("๐ฉ๐ด", "Dominican Republic"), ("๐ฉ๐ฟ", "Algeria"), ("๐ช๐ฆ", "Ceuta & Melilla"), ("๐ช๐จ", "Ecuador"), ("๐ช๐ช", "Estonia"), ("๐ช๐ฌ", "Egypt"), ("๐ช๐ญ", "Western Sahara"), ("๐ช๐ท", "Eritrea"), ("๐ช๐ธ", "Spain"), ("๐ช๐น", "Ethiopia"), ("๐ช๐บ", "European Union"), ("๐ซ๐ฎ", "Finland"), ("๐ซ๐ฏ", "Fiji"), ("๐ซ๐ฐ", "Falkland Islands"), ("๐ซ๐ฒ", "Micronesia"), ("๐ซ๐ด", "Faroe Islands"), ("๐ซ๐ท", "France"), ("๐ฌ๐ฆ", "Gabon"), ("๐ฌ๐ง", "United Kingdom"), ("๐ฌ๐ฉ", "Grenada"), ("๐ฌ๐ช", "Georgia"), ("๐ฌ๐ซ", "French Guiana"), ("๐ฌ๐ฌ", "Guernsey"), ("๐ฌ๐ญ", "Ghana"), ("๐ฌ๐ฎ", "Gibraltar"), ("๐ฌ๐ฑ", "Greenland"), ("๐ฌ๐ฒ", "Gambia"), ("๐ฌ๐ณ", "Guinea"), ("๐ฌ๐ต", "Guadeloupe"), ("๐ฌ๐ถ", "Equatorial Guinea"), ("๐ฌ๐ท", "Greece"), ("๐ฌ๐ธ", "South Georgia & South Sandwich Islands"), ("๐ฌ๐น", "Guatemala"), ("๐ฌ๐บ", "Guam"), ("๐ฌ๐ผ", "Guinea-Bissau"), ("๐ฌ๐พ", "Guyana"), ("๐ญ๐ฐ", "Hong Kong"), ("๐ญ๐ฒ", "Heard & McDonald Islands"), ("๐ญ๐ณ", "Honduras"), ("๐ญ๐ท", "Croatia"), ("๐ญ๐น", "Haiti"), ("๐ญ๐บ", "Hungary"), ("๐ฎ๐จ", "Canary Islands"), ("๐ฎ๐ฉ", "Indonesia"), ("๐ฎ๐ช", "Ireland"), ("๐ฎ๐ฑ", "Israel"), ("๐ฎ๐ฒ", "Isle of Man"), ("๐ฎ๐ณ", "India"), ("๐ฎ๐ด", "British Indian Ocean Territory"), ("๐ฎ๐ถ", "Iraq"), ("๐ฎ๐ท", "Iran"), ("๐ฎ๐ธ", "Iceland"), ("๐ฎ๐น", "Italy"), ("๐ฏ๐ช", "Jersey"), ("๐ฏ๐ฒ", "Jamaica"), ("๐ฏ๐ด", "Jordan"), ("๐ฏ๐ต", "Japan"), ("๐ฐ๐ช", "Kenya"), ("๐ฐ๐ฌ", "Kyrgyzstan"), ("๐ฐ๐ญ", "Cambodia"), ("๐ฐ๐ฎ", "Kiribati"), ("๐ฐ๐ฒ", "Comoros"), ("๐ฐ๐ณ", "St. Kitts & Nevis"), ("๐ฐ๐ต", "North Korea"), ("๐ฐ๐ท", "South Korea"), ("๐ฐ๐ผ", "Kuwait"), ("๐ฐ๐พ", "Cayman Islands"), ("๐ฐ๐ฟ", "Kazakhstan"), ("๐ฑ๐ฆ", "Laos"), ("๐ฑ๐ง", "Lebanon"), ("๐ฑ๐จ", "St. Lucia"), ("๐ฑ๐ฎ", "Liechtenstein"), ("๐ฑ๐ฐ", "Sri Lanka"), ("๐ฑ๐ท", "Liberia"), ("๐ฑ๐ธ", "Lesotho"), ("๐ฑ๐น", "Lithuania"), ("๐ฑ๐บ", "Luxembourg"), ("๐ฑ๐ป", "Latvia"), ("๐ฑ๐พ", "Libya"), ("๐ฒ๐ฆ", "Morocco"), ("๐ฒ๐จ", "Monaco"), ("๐ฒ๐ฉ", "Moldova"), ("๐ฒ๐ช", "Montenegro"), ("๐ฒ๐ซ", "St. Martin"), ("๐ฒ๐ฌ", "Madagascar"), ("๐ฒ๐ญ", "Marshall Islands"), ("๐ฒ๐ฐ", "Macedonia"), ("๐ฒ๐ฑ", "Mali"), ("๐ฒ๐ฒ", "Myanmar (Burma)"), ("๐ฒ๐ณ", "Mongolia"), ("๐ฒ๐ด", "Macau SAR China"), ("๐ฒ๐ต", "Northern Mariana Islands"), ("๐ฒ๐ถ", "Martinique"), ("๐ฒ๐ท", "Mauritania"), ("๐ฒ๐ธ", "Montserrat"), ("๐ฒ๐น", "Malta"), ("๐ฒ๐บ", "Mauritius"), ("๐ฒ๐ป", "Maldives"), ("๐ฒ๐ผ", "Malawi"), ("๐ฒ๐ฝ", "Mexico"), ("๐ฒ๐พ", "Malaysia"), ("๐ฒ๐ฟ", "Mozambique"), ("๐ณ๐ฆ", "Namibia"), ("๐ณ๐จ", "New Caledonia"), ("๐ณ๐ช", "Niger"), ("๐ณ๐ซ", "Norfolk Island"), ("๐ณ๐ฌ", "Nigeria"), ("๐ณ๐ฎ", "Nicaragua"), ("๐ณ๐ฑ", "Netherlands"), ("๐ณ๐ด", "Norway"), ("๐ณ๐ต", "Nepal"), ("๐ณ๐ท", "Nauru"), ("๐ณ๐บ", "Niue"), ("๐ณ๐ฟ", "New Zealand"), ("๐ด๐ฒ", "Oman"), ("๐ต๐ฆ", "Panama"), ("๐ต๐ช", "Peru"), ("๐ต๐ซ", "French Polynesia"), ("๐ต๐ฌ", "Papua New Guinea"), ("๐ต๐ญ", "Philippines"), ("๐ต๐ฐ", "Pakistan"), ("๐ต๐ฑ", "Poland"), ("๐ต๐ฒ", "St. Pierre & Miquelon"), ("๐ต๐ณ", "Pitcairn Islands"), ("๐ต๐ท", "Puerto Rico"), ("๐ต๐ธ", "Palestinian Territories"), ("๐ต๐น", "Portugal"), ("๐ต๐ผ", "Palau"), ("๐ต๐พ", "Paraguay"), ("๐ถ๐ฆ", "Qatar"), ("๐ท๐ช", "Rรฉunion"), ("๐ท๐ด", "Romania"), ("๐ท๐ธ", "Serbia"), ("๐ท๐บ", "Russia"), ("๐ท๐ผ", "Rwanda"), ("๐ธ๐ฆ", "Saudi Arabia"), ("๐ธ๐ง", "Solomon Islands"), ("๐ธ๐จ", "Seychelles"), ("๐ธ๐ฉ", "Sudan"), ("๐ธ๐ช", "Sweden"), ("๐ธ๐ฌ", "Singapore"), ("๐ธ๐ญ", "St. Helena"), ("๐ธ๐ฎ", "Slovenia"), ("๐ธ๐ฏ", "Svalbard & Jan Mayen"), ("๐ธ๐ฐ", "Slovakia"), ("๐ธ๐ฑ", "Sierra Leone"), ("๐ธ๐ฒ", "San Marino"), ("๐ธ๐ณ", "Senegal"), ("๐ธ๐ด", "Somalia"), ("๐ธ๐ท", "Suriname"), ("๐ธ๐ธ", "South Sudan"), ("๐ธ๐น", "Sรฃo Tomรฉ & Prรญncipe"), ("๐ธ๐ป", "El Salvador"), ("๐ธ๐ฝ", "Sint Maarten"), ("๐ธ๐พ", "Syria"), ("๐ธ๐ฟ", "Swaziland"), ("๐น๐ฆ", "Tristan Da Cunha"), ("๐น๐จ", "Turks & Caicos Islands"), ("๐น๐ฉ", "Chad"), ("๐น๐ซ", "French Southern Territories"), ("๐น๐ฌ", "Togo"), ("๐น๐ญ", "Thailand"), ("๐น๐ฏ", "Tajikistan"), ("๐น๐ฐ", "Tokelau"), ("๐น๐ฑ", "Timor-Leste"), ("๐น๐ฒ", "Turkmenistan"), ("๐น๐ณ", "Tunisia"), ("๐น๐ด", "Tonga"), ("๐น๐ท", "Turkey"), ("๐น๐น", "Trinidad & Tobago"), ("๐น๐ป", "Tuvalu"), ("๐น๐ผ", "Taiwan"), ("๐น๐ฟ", "Tanzania"), ("๐บ๐ฆ", "Ukraine"), ("๐บ๐ฌ", "Uganda"), ("๐บ๐ฒ", "United States"), ("๐บ๐ณ", "United Nations"), ("๐บ๐พ", "Uruguay"), ("๐บ๐ฟ", "Uzbekistan"), ("๐ป๐ฆ", "Vatican City"), ("๐ป๐จ", "St. Vincent & Grenadines"), ("๐ป๐ช", "Venezuela"), ("๐ป๐ฌ", "British Virgin Islands"), ("๐ป๐ฎ", "U.S. Virgin Islands"), ("๐ป๐ณ", "Vietnam"), ("๐ป๐บ", "Vanuatu"), ("๐ผ๐ซ", "Wallis & Futuna"), ("๐ผ๐ธ", "Samoa"), ("๐ฝ๐ฐ", "Kosovo"), ("๐พ๐ช", "Yemen"), ("๐พ๐น", "Mayotte"), ("๐ฟ๐ฆ", "South Africa"), ("๐ฟ๐ฒ", "Zambia"), ("๐ฟ๐ผ", "Zimbabwe"), ("๐ด๓?ง๓?ข๓?ฅ๓?ฎ๓?ง๓?ฟ", "England"), ("๐ด๓?ง๓?ข๓?ณ๓?ฃ๓?ด๓?ฟ", "Scotland"), ("๐ด๓?ง๓?ข๓?ท๓?ฌ๓?ณ๓?ฟ," "Wales")]
print("Flag Emojis up to date as of October 25, 2022")

@bot.event
async def on_ready():
    print(f'Bot connected, logged in as {bot.user}, ID {bot.user.id}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.BadLiteralArgument):
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        return
    else:
        raise error

def getbuttons(index):
    name4 = random.choice(flagpairs)
    names = [random.choice(flagpairs)[index], random.choice(flagpairs)[index], random.choice(flagpairs)[index], name4[index]] # name4 will be the answer one, we chose this one special because it has both index 1 and 2 saved
    while len(names) != len(set(names)): # Re-roll if there are duplicates
        name4 = random.choice(flagpairs)
        names = [random.choice(flagpairs)[index], random.choice(flagpairs)[index], random.choice(flagpairs)[index], name4[index]]
        print("\n\n\nRerolled because of duplicates")
    if index == 1: # crude statement to check whether we're looking for flags or for flag names
        answer = name4[0]
        match = name4[1]
    else:
        answer = name4[1]
        match = name4[0]
    
    random.shuffle(names) # shuffle it so that it's not always answer 4
    return(names, answer, match)

@bot.hybrid_command(name = "guessplace", with_app_command=True, description="Guess the name of a place from its flag!")
@app_commands.describe(
    guesstype="Choose whether to guess the flag or the place!"
)
async def guessplace(ctx: commands.Context, guesstype: Literal["flag", "place"]):
    if guesstype.lower() == "flag":
        flagorplace = "place"
        sendorguess = "Guess"
        guesstype = 0
    elif guesstype.lower() == "place":
        flagorplace = "flag"
        sendorguess = "Send"
        guesstype = 1
    input = getbuttons(guesstype)
    await ctx.reply(f"{sendorguess} the {flagorplace}: {input[2]}", mention_author=False)
    channel = ctx.channel
    def check(m):
            return m.content.lower() == input[1].lower() and m.channel == channel
    try:
        msg = await bot.wait_for('message', check=check, timeout=20)
    except asyncio.TimeoutError:
        await channel.send(f"Nobody got it... the {flagorplace} was {input[1]}!")
        print(f"Nobody got the word, word was {input[1]}")
    else:
        await msg.reply(f"{msg.author.mention} got it!")
        print(f"{msg.author}({msg.author.id}) won in {msg.guild.name}({msg.guild.id}), word was {input[1]}")

@bot.hybrid_command(name="resync", with_app_command=True, description="Resync the commands!")
async def resync(ctx: commands.Context):
    if ctx.message.author.guild_permissions.administrator:
        await bot.tree.sync()
        await ctx.reply(content="Resynced slash commands!", mention_author=False, ephemeral=True)
    else:
        await ctx.reply(content="No permissions!", mention_author=False, ephemeral=True)

def raptvfunc(img, msg):
    with Image.open(BytesIO(img)) as final:
        overlay = Image.open("raptvnotext.png")
        bg = Image.open(BytesIO(img))
        font = ImageFont.truetype(font='steelfisheb.otf', size=400)

        bg = bg.resize((overlay.size[0], overlay.size[1]))
        bg = bg.convert("RGBA")
        final = Image.alpha_composite(bg, overlay)
        draw = ImageDraw.Draw(im=final)
        text=msg.upper()

        def get_wrapped_text(text: str, font: ImageFont.ImageFont, line_length: int):
                lines = ['']
                for word in text.split():
                    line = f'{lines[-1]} {word}'.strip()
                    if font.getlength(line) <= line_length:
                        lines[-1] = line
                    else:
                        lines.append(word)
                return '\n'.join(lines)
        draw.text(xy=(final.size[0]/2, final.size[1]/2 + 300), text=get_wrapped_text(text, font, line_length=2950), font=font, fill='#FF6508', anchor='ma')
        output_buffer = BytesIO()
        final.save(output_buffer, "png")  # or whatever format
        output_buffer.seek(0)
        return output_buffer

@bot.hybrid_command(name="raptv", with_app_command=True, description="Create a post akin to the RapTV Instagram account!")
async def raptv(ctx: commands.Context, img: discord.Attachment, *, msg: str):
    img = await img.read()
    async with ctx.typing():
        await ctx.reply(mention_author=False, file=discord.File(raptvfunc(img,msg), filename="output.png"))

def quotefunc(img, msg):
    with Image.open(BytesIO(img)) as final:
        overlay = Image.open("quote.png")
        bg = Image.open(BytesIO(img))
        font = ImageFont.truetype(font='avenirnext.otf', size=50)

        bg = bg.resize((overlay.size[1], overlay.size[1]))
        bg = ImageOps.grayscale(bg)
        bg = bg.convert("RGBA")
        bgfinal = Image.new(mode="RGBA", size=(overlay.size[0], overlay.size[1]))
        bgfinal.paste(bg, (-100, 0))
        final = Image.alpha_composite(bgfinal, overlay)
        draw = ImageDraw.Draw(im=final)
        time = datetime.datetime.now
        mentions = ["dummy mention"]
        for i in msg.mentions:
            mentions.append((i.id, i.name))
            print("mention found")
        for i in mentions:
            if str(i[0]) in str(msg.content):
                withtags = "<@" + str(i[0]) + ">"
                newname = "@" + str(i[1])
                newmsg = str(msg.content).replace(withtags, newname)
            else:
                newmsg = str(msg.content)
        text="\"" + newmsg + "\""
        def get_wrapped_text(text: str, font: ImageFont.ImageFont, line_length: int):
                lines = ['']
                for word in text.split():
                    line = f'{lines[-1]} {word}'.strip()
                    if font.getlength(line) <= line_length:
                        lines[-1] = line
                    else:
                        lines.append(word)
                return '\n'.join(lines)
        text = get_wrapped_text(text,font, line_length=700)
        if msg.author.nick != None:
            text=text + "\n\n-" + get_wrapped_text(str(msg.author.nick), font, line_length=700) + ", " + str(time().year)
        else:
            text=text + "\n\n-" + get_wrapped_text(str(msg.author.name), font, line_length=700) + ", " + str(time().year)
        draw.text(xy=(final.size[0]/2 + 200, final.size[1]/2), text=text, font=font, fill='#FFFFFF', anchor='mm')
        output_buffer = BytesIO()
        final = final.resize((overlay.size[0], overlay.size[1]))
        final.save(output_buffer, "png", optimize=True, quality=10)  # or whatever format
        output_buffer.seek(0)
        return output_buffer

@bot.hybrid_command(name="quote", with_app_command=True, description="Create a quote from the most recent message of a member!")
async def quote(ctx: commands.Context, user: discord.Member):
    channel = ctx.channel
    msg = ""
    async for i in channel.history(limit=50):
        if i.author == user:
            if not i.content.lower().startswith("h!") and not "quote" in i.content.lower():
                msg = i.id
                break
    img = user.display_avatar
    img = await img.read()
    if msg == "":
        await ctx.reply(content="Message not found! Here are some things to check:\n\n**- Does the user's most recent message include text?**\n**- Has the user sent a message within the last 50 messages?**", mention_author=False, ephemeral=True)
        return
    msg = await ctx.fetch_message(msg)
    if msg.content == "":
        await ctx.reply(content="Message not found! Here are some things to check:\n\n**- Does the user's most recent message include text?**\n**- Has the user sent a message within the last 50 messages?**", mention_author=False, ephemeral=True)
        return
    async with ctx.typing():
        await ctx.reply(mention_author=False, file=discord.File(quotefunc(img, msg), filename="output.png"))

@bot.hybrid_command(name="echo", with_app_command=True, description="Send a message to another channel through the bot!")
async def resync(ctx: commands.Context, channels: discord.TextChannel, *, msg: str):
    if ctx.message.author.guild_permissions.administrator:
        await channels.send(msg)
        channeltag = "<#" + str(channels.id) + ">"
        await ctx.reply(content=f"Sent \"{msg}\" to {channeltag}!", mention_author=False, ephemeral=True)
    else:
        await ctx.reply(content="No permissions!", mention_author=False, ephemeral=True)

@bot.hybrid_command(name="dice", description="Roll a dice")
async def dice(ctx: commands.Context, maxroll: typing.Optional[int] = 6):
    await ctx.reply(f"The dice landed on {random.randint(1, maxroll)}!", mention_author=False, ephemeral=True)


@bot.hybrid_command(name="ping", description="Get the bot's ping")
async def gifture(ctx: commands.Context):
    await ctx.reply(f"My ping is {round(bot.latency * 1000)}ms.", mention_author=False)

@bot.hybrid_command(name="wheel", description="Spin a wheel between multiple options!")
@app_commands.describe(choices="Options; Comma separate each choice.")
async def wheel(ctx: commands.Context, *, choices: str):
    list = choices.split(",")
    newlist = []
    for i in list:
        i = i.replace(",", "")
        if not i == "":
            i = i.rstrip()
            newlist.append(i)
    if len(list) > 1:
        final = random.choice(newlist)
        await ctx.reply(final, mention_author=False)
        print(f"Selected \"{final}\" from {newlist} for {ctx.message.author}")
    else:
        await ctx.reply("Not enough arguments detected! Did you comma separate them?", mention_author=False, ephemeral=True)

@bot.hybrid_command(name="coinflip", description="Flip a coin!")
async def coinflip(ctx: commands.Context):
    sides = ["Heads", "Tails"]
    side = random.choice(sides)
    await ctx.reply("The coin landed on " + side + "!", mention_author=False)
    print(f"Landed on {side} for {ctx.message.author}")

@bot.event
async def on_message(message):
    if message.author != bot.user: # If the message is from a bot and not a human
        if message.content.lower().startswith('jarvis'): #if it starts with jarvis, the .lower() part makes sure it's not case sensitive
            def ingFrom(s): # Present participle function I copied from https://gist.github.com/arjun921/5f38259ea056fdc35617cb7449fb234e
                for x in s:
                    li.append(x)
                if li[len(li)-1]=='e' and li[len(li)-2]!='i':
                    del li[len(li)-1]
                    li.append("ing")
                elif li[len(li)-1]=='e' and li[len(li)-2]=='i':
                    del li[len(li)-1]
                    del li[len(li)-1]
                    li.append("ying")
                    """To Check"""
                elif li[len(li)-2] in 'aeiou' and li[len(li)-1] not in 'aeiou':
                    temp = li[len(li)-1]
                    del li[len(li)-1]
                    li.append(temp)
                    li.append(temp)
                    li.append("ing")
                elif li[len(li)-1] in 'aeiouy':
                    li.append("ing")
                else:
                    li.append("ing")
                return "".join(li)
            li=[]

            text = message.content
            firstword = []
            list = [*text] # takes the message and splits it up ['l', 'i', 'k', 'e', ' ', 't', 'h', 'i', 's']
            count = 0


            try:
                if list[6] == ",": #if the seventh character in the message is a comma, remove it  from the list(makes sure it supports messages with and without commas)
                    list.pop(6)
            except:
                return #cancels if there's nothing after jarvis
            try:
                list[7]
            except:
                return # cancels if there's nothing after the comma
            while list[6] == " ": #gets rid of all spaces leading up to the first character
                list.pop(6)

            for i in range(6): # remove the phrase "jarvis" from the beginning of the message
                list.pop(0)

            for i in list:
                if i != " ": # repeats until it finishes the first word in list(until there's a space)
                    firstword.append(i)
                    count = count+1 # counts how many characters it added to the firstword list
                else:
                    break # if there's a space, quit
            for i in range(count): # remove the first word from the list
                list.pop(0)
            firstword = "".join(map(str, firstword)) # convert ['t', 'h', 'i', 's'] into 'this'
            mentions = []
            for i in message.mentions:
                mentions.append((i.id, i.nick))
            addtick = 0
            for i in mentions:
                if str(i[0]) in firstword:
                    withtags = "<@" + str(i[0]) + ">"
                    newname = "`@" + str(i[1])
                    firstword = firstword.replace(withtags, newname)
                    addtick = 1
                    tickloc = len(firstword)
                    print(firstword)
            firstwordfinal = ingFrom(firstword) # attempts to make the first word a present participle
            if addtick == 1:
                firstwordfinal = [*firstwordfinal]
                firstwordfinal.insert(tickloc, "`")
                firstwordfinal = "".join(map(str, firstwordfinal))
            list = "".join(map(str, list)) # same as line 63
            list = list.lower()
            list = list.replace('@everyone', '`@everyone`')
            list = list.replace('@here', '`@here`')
            list = re.sub(r'\bi\b', 'you', list)
            list = re.sub(r'\bme\b', 'you', list)
            list = re.sub(r'\bmy\b', 'your', list)

            # creates the final text
            yorn = ["yes", "no"]
            for i in mentions:
                if str(i[0]) in list:
                    withtags = "<@" + str(i[0]) + ">"
                    newname = "`@" + str(i[1]) + "`"
                    list = list.replace(withtags, newname)
            if firstword.endswith("?") or list.endswith("?"):
                final = random.choice(yorn)
            else:
                if addtick == 1:
                    final = firstwordfinal + list
                else:
                    final = firstwordfinal.lower() + list
            print(f"Sent \"{final}\" to {message.guild}({message.guild.id})")
            await message.channel.send(content=final, reference=message, mention_author=False, allowed_mentions=None) # send the final message
    await bot.process_commands(message)

bot.run('TOKEN')

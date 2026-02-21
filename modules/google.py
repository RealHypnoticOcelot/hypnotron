import discord
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import dotenv_values
import aiohttp
from urllib.parse import urlsplit

serpapi_key = dotenv_values()['SERPAPI_KEY']

# Thanks to TizzySaurus on Discord for helping with these functions, ID 442244135840382978

def round_sig(n: int, sig: int) -> int:
  """Returns the amount of decimal places to display in order to display `n` as `sig` sf."""
  return -(int(floor(log10(abs(n))))-1)

def format_number(num: float) -> str:
  if isinstance(num, int):  # no formatting
    return f"{num}"
  if num.is_integer():
    return f"{int(num)}"  # remove trailing ".0..."
  if num >= 0.01:
    num_dp = 2
    return f"{num:.{num_dp}f}" # format to 2dp, change both 2's to change how many it rounds to
  num_sf = 2
  num_decimals = round_sig(num, num_sf)
  return f"{num:.{num_decimals}f}"  # format to 2 sf

class google(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access

  @commands.hybrid_command(name="google", description="Google anything!")
  @app_commands.allowed_installs(guilds=True, users=True)
  @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True) # Guilds, DMs, DMs/Group DMs
  async def google(self, ctx, *, query: str):
    async with ctx.typing():
      async with aiohttp.ClientSession() as session:
        async with session.get(f"https://serpapi.com/search.json?q={query}&hl=en&gl=us&safe=active&api_key={serpapi_key}") as resp:
          if resp.status == 429:
            return await ctx.reply(f"Error: Out of searches!", mention_author=False, ephemeral=True)
          if resp.status == 401:
            return await ctx.reply(f"Error: Invalid API key!", mention_author=False, ephemeral=True)
          elif resp.status != 200: 
            return await ctx.reply(f"Error: Response code {resp.status}", mention_author=False, ephemeral=True)
          data = await resp.json()
          if "answer_box" in data:        
            answer_box = data['answer_box']
            # calculator
            if answer_box['type'] == "calculator_result":
              calculator_result = data['answer_box']['result']

              embed = discord.Embed(
                  color=discord.Color.random(), 
                  title=f"Calculator Result", 
                  description=calculator_result)
              await ctx.reply(embed=embed, mention_author=False)
            # weather
            elif answer_box['type'] == "weather_result":
              weather_location = answer_box['location']
              weather_temperature = f"{answer_box['temperature']}°"
              weather_temperature_unit = answer_box['unit']
              weather_outside = answer_box['weather'] # i.e. Partly Cloudy
              weather_humidity = answer_box['humidity']
              weather_wind = answer_box['wind']
              weather_precipitation = answer_box['precipitation']

              embed = discord.Embed(
                color=discord.Color.random(), 
                title=weather_location, 
                description=f"{weather_temperature} {weather_temperature_unit}").set_footer(
                  text=f"Weather: {weather_outside} | Humidity {weather_humidity} | Wind {weather_wind} | Precipitation {weather_precipitation}"
                )
              await ctx.reply(embed=embed, mention_author=False)
            # stocks
            elif answer_box['type'] == "finance_results":
              finance_company_name = answer_box['title']

              finance_stock_name = answer_box['stock']
              finance_stock_price = answer_box['price']
              finance_stock_currency = answer_box['currency']

              price_movement = answer_box['price_movement']
              finance_stock_movement = price_movement['movement'] # up or down
              finance_stock_movement_amount = price_movement['price']
              finance_stock_movement_percent = f"{price_movement['percentage']}%"
              finance_stock_movement_date = price_movement['date']
              
              embed = discord.Embed(
                color=discord.Color.random(), 
                title=f"{finance_company_name} -{finance_stock_name}", 
                description=f"{finance_stock_price} {finance_stock_currency}").set_footer(
                  text=f"{finance_stock_movement} {finance_stock_movement_amount}({finance_stock_movement_percent}) {finance_stock_movement_date}"
                )
              await ctx.reply(embed=embed, mention_author=False)
            # population
            elif answer_box['type'] == "population_result":
              population_area = answer_box['place']
              population_amount = answer_box['population']
              population_last_update = answer_box['year']

              embed = discord.Embed(
                color=discord.Color.random(), 
                title=f"{population_area} Population", 
                description=population_amount).set_footer(text=f"As of {population_last_update}")
              await ctx.reply(embed=embed, mention_author=False)
            # currency
            elif answer_box['type'] == "currency_converter":
              currency_converter = answer_box['currency_converter']
              
              currency_from_value = currency_converter['from']['price']
              currency_formatted_from_value = format_number(currency_from_value)
              currency_from_type = currency_converter['from']['currency']

              currency_to_value = currency_converter['to']['price']
              currency_formatted_to_value = format_number(currency_to_value)
              currency_to_type = currency_converter['to']['currency']

              symbol = "=" if currency_from_value == float(currency_formatted_from_value) and currency_to_value == float(currency_formatted_to_value) else "≈"
              embed = discord.Embed(
                color=discord.Color.random(), 
                title=f"Currency Converter", 
                description=f"{currency_formatted_from_value} {currency_from_type} {symbol} {currency_formatted_to_value} {currency_to_type}")
              await ctx.reply(embed=embed, mention_author=False)
            # translation
            elif answer_box['type'] == "translation_result":
              translation_original_text = f"\"{data['answer_box']['translation']['source']['text']}\""
              translation_target_language = data['answer_box']['translation']['target']['language']
              translation_target_text = data['answer_box']['translation']['target']['text']
              embed = discord.Embed(
                color=discord.Color.random(), 
                title=f"{translation_original_text} in {translation_target_language}", 
                description=f"{translation_target_text}")
              await ctx.reply(embed=embed, mention_author=False)
            # unit conversion
            elif answer_box['type'] == "unit_converter":
              unit_conversion_type = answer_box['unit_type']
              
              unit_from_value = answer_box['from']['value']
              unit_formatted_from_value = format_number(unit_from_value)
              unit_from_unit = answer_box['from']['unit']

              unit_to_value = answer_box['to']['value']
              unit_formatted_to_value = format_number(unit_to_value)
              unit_to_unit = answer_box['to']['unit']

              symbol = "=" if unit_from_value == float(unit_formatted_from_value) and unit_to_value == float(unit_formatted_to_value) else "≈"
              embed = discord.Embed(
                color=discord.Color.random(), 
                title=unit_conversion_type,
                description=f"{unit_formatted_from_value} {unit_from_unit} {symbol} {unit_formatted_to_value} {unit_to_unit}")
              await ctx.reply(embed=embed, mention_author=False)
            # dictionary
            elif answer_box['type'] == "dictionary_results":
              dictionary_name = answer_box['syllables'].replace("·", "")
              dictionary_syllables = answer_box['syllables']
              title = dictionary_name if dictionary_syllables == dictionary_name else f"{dictionary_name} - {dictionary_syllables}"
              dictionary_pronunciation = answer_box['pronunciation_audio']
              dictionary_descriptions = []
              for i in range(len(answer_box['definitions'])):
                definition = answer_box['definitions'][i]
                try:
                  example = answer_box['examples'][i]
                  dictionary_descriptions.append(f"{i + 1}. `{definition}`\n*{example}*\n")
                except:
                  dictionary_descriptions.append(f"{i + 1}. `{definition}`\n")
              dictionary_descriptions = ''.join(dictionary_descriptions)
                
              embed = discord.Embed(
                color=discord.Color.random(),
                title=title,
                url=dictionary_pronunciation,
                description = dictionary_descriptions
              )
              await ctx.reply(embed=embed, mention_author=False)
            # if the answer box is of some other unknown type
            else: # Probably a better way than just having this code there twice
              organic_results = data['organic_results'][0]

              result_title = organic_results['title']
              result_url = organic_results['link']
              result_snippet = organic_results['snippet']
              result_source = organic_results['source']
              try:
                result_thumbnail = organic_results['thumbnail']
              except:
                basedomain = urlsplit(organic_results['link']).netloc
                result_thumbnail = f"https://icon.horse/icon/{basedomain}"

              embed = discord.Embed(
                color=discord.Color.random(), 
                title=result_title, 
                url=result_url, 
                description=result_snippet).set_footer(text=f"Source: {result_source}")
              embed.set_thumbnail(url=result_thumbnail)
              await ctx.reply(embed=embed, mention_author=False)                     
          else:
            organic_results = data['organic_results'][0]

            result_title = organic_results['title']
            result_url = organic_results['link']
            result_snippet = organic_results['snippet']
            result_source = organic_results['source']
            try:
              result_thumbnail = organic_results['thumbnail']
            except:
              basedomain = urlsplit(organic_results['link']).netloc
              result_thumbnail = f"https://icon.horse/icon/{basedomain}"
            
            embed = discord.Embed(
              color=discord.Color.random(), 
              title=result_title, 
              url=result_url, 
              description=result_snippet).set_footer(text=f"Source: {result_source}")
            embed.set_thumbnail(url=result_thumbnail)
            await ctx.reply(embed=embed, mention_author=False)

async def setup(bot):
  await bot.add_cog(google(bot=bot))
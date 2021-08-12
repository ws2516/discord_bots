# bot.py
import os
import random
import scrapers
import datetime
import time

from datetime import datetime
from scrapers import finance
from scrapers import lifestyle

import article_save
from article_save import write_to_sheet
from article_save import on_sheet_grab
from article_save import get_last_time
from article_save import write_to_sheet_time

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.command(name='libor')
async def libor_curve(ctx):
    getLibor = finance.libor()
    response = getLibor
    await ctx.send(response)

@bot.command(name='vesto')
async def vesto(ctx, message):
    getDef = finance.investopedia_definitions(message)
    response = getDef
    await ctx.send(response)

@bot.command(name='coffee')
async def coffee(ctx, message):
    getCoffee = lifestyle.coffee_bot(message)
    response = getCoffee
    await ctx.send(response)

@bot.command(name='article')
async def nyker(ctx, *, arg):
    global times_used
    article_url = lifestyle.google_search('The New Yorker ', arg)
    await ctx.send("Is the article: \n {}".format(article_url))
    if article_url.split('www.')[1][:len('theatlantic')] == 'theatlantic':
    	titled = article_url.split('/')[-3].replace('-',' ')
    elif article_url.split('www.')[1][:len('nybooks')] == 'nybooks':
    	titled = article_url.split('/')[-2].replace('-',' ')
    else:
    	titled = article_url.split('/')[-1].replace('-',' ')
    	
    await ctx.send("Reply y if Yes or n for No.")
    article_save.write_to_sheet(titled, article_url)
    # This will make sure that the response will only be registered if the following
    # conditions are met:
    
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and \
        msg.content.lower() in ["y", "n"]

    msg = await bot.wait_for("message", check=check)
    if msg.content.lower() == "y":
        await ctx.send("You said yes, it has been added to your New Yorker article database.")
    else:
        await ctx.send("You said no, maybe try another paragraph or more text - sorry about that :(")

    times_used = times_used + 1
    try:
        msg = await bot.wait_for("message", check=check, timeout=30) # 30 seconds to reply
    except asyncio.TimeoutError:
        await ctx.send("Sorry, you didn't reply in time!")



@bot.command(name='clocking')
async def timesheet(ctx, *, arg):
	now = str(datetime.now())
	helpers = pd.read_csv('time_logger.csv')
	helper = list(helpers.values)
	if typed == "in":
		write_to_sheet_time(time.time(),'in')
		print(f"You clocked {typed} at {now}")
	elif typed == "out":
		timer = get_last_time()
		length = (time.time() - timer)/(60*60)
		write_to_sheet_time(time.time(),'out')
		print(f"You clocked {typed} at {now} for a total of {length} hours.")
	else:
		print(f"Errr I didn't understand that.")
	

bot.run(TOKEN)












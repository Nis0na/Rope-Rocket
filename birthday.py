import discord
from discord.ext import commands
from datetime import datetime, timedelta

# Replace 'YOUR_BOT_TOKEN' with your bot's token
TOKEN = 'YOUR_BOT_TOKEN'

# Initialize the bot with the '!' command prefix
bot = commands.Bot(command_prefix='!')

# Dictionary to store user birthdays
birthdays = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name='set_birthday')
async def set_birthday(ctx, date: str):
    """Command to set the user's birthday. Date should be in YYYY-MM-DD format."""
    try:
        birthday = datetime.strptime(date, '%Y-%m-%d')
        birthdays[ctx.author.id] = birthday
        await ctx.send(f'Birthday set for {ctx.author.name} on {birthday.strftime("%B %d, %Y")}')
    except ValueError:
        await ctx.send('Invalid date format. Please use YYYY-MM-DD.')

@bot.command(name='days_until_birthday')
async def days_until_birthday(ctx, user: discord.User = None):
    """Command to calculate the number of days until the user's birthday."""
    user = user or ctx.author
    if user.id in birthdays:
        today = datetime.today()
        bday = birthdays[user.id]
        bday_this_year = bday.replace(year=today.year)
        if bday_this_year < today:
            bday_this_year = bday_this_year.replace(year=today.year + 1)
        days_left = (bday_this_year - today).days
        await ctx.send(f'{days_left} days until {user.name}\'s birthday.')
    else:
        await ctx.send(f'Birthday not set for {user.name}. Use `!set_birthday YYYY-MM-DD` to set it.')

# Run the bot
if __name__ == "__main__":
    bot.run(TOKEN)
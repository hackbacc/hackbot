import os
from twitchio.ext import commands
import subprocess
import datetime

bot = commands.Bot(
        irc_token="oauth:"+os.environ['tip'],
    client_id=os.environ['twitch_cid'],
    nick="hackbacc",
    prefix='!',
    initial_channels=['hackbacc']
)

@bot.event
async def event_ready():
    print(f'Ready | {bot.nick}')

@bot.event
async def event_message(message):
    print(message.content)

    await bot.handle_commands(message)

@bot.command(name='test', aliases=['t'])
async def test_command(ctx):
    await ctx.send(f'Hello {ctx.author.name}')

@bot.command(name='agenda', aliases=['c'])
async def agenda_command(ctx):
    date = str(datetime.datetime.now().date())
    agenda = subprocess.check_output("curl -s https://raw.githubusercontent.com/hackbacc/schedule/master/json/schedule.json | jq .'projects[] | select(.starts==\"" + date + "\") | .description'", shell=1)#[2:-1]
    if agenda == b"":
        agenda = "There is no agenda yet."
    await ctx.send(agenda.encode('utf-8'))
bot.run()

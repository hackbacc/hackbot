import os
from twitchio.ext import commands
import subprocess
import datetime
import urllib.request, json

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
    with urllib.request.urlopen("https://raw.githubusercontent.com/hackbacc/schedule/master/json/schedule.json") as url:
        data = json.loads(url.read().decode())

# with open('json/schedule.json', 'r') as f:
#     data = json.load(f)

    to_date = datetime.datetime.now().date()
    agendas = []

    for project in data['projects']:
        st_date = datetime.datetime.strptime(project['starts'], "%Y-%m-%d").date() 
        ed_date = datetime.datetime.strptime(project.get('ends', str(to_date)), "%Y-%m-%d").date()


        if st_date <= to_date and to_date <= ed_date and (to_date.weekday() + 1) in project['days']:
            agendas.append(project['description'])
    
    for agenda in agendas:
        await ctx.send(agenda)#.encode('utf-8'))
bot.run()

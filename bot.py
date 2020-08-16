import os
from twitchio.ext import commands
import subprocess
import datetime
import urllib.request, json
import requests

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

@bot.command(name='agenda', aliases=['a'])
async def agenda_command(ctx):
    with urllib.request.urlopen("https://raw.githubusercontent.com/hackbacc/schedule/master/json/schedule.json") as url:
        data = json.loads(url.read().decode())

    to_date = datetime.datetime.now().date()
    agendas = []

    for project in data['projects']:
        st_date = datetime.datetime.strptime(project['starts'], "%Y-%m-%d").date() 
        ed_date = datetime.datetime.strptime(project.get('ends', str(to_date)), "%Y-%m-%d").date()


        if st_date <= to_date and to_date <= ed_date and (to_date.weekday() + 1) in project['days']:
            agendas.append(project['description'])
    
    for agenda in agendas:
        await ctx.send(agenda)#.encode('utf-8'))

@bot.command(name='discord', aliases=['d'])
async def discord_command(ctx):
    await ctx.send("https://discord.gg/9pQgEEx")

@bot.command(name='github', aliases=['g'])
async def github_command(ctx):
    await ctx.send("Personal - https://github.com/markroxor")
    await ctx.send("Channel - https://github.com/hackbacc")

@bot.command(name='projects', aliases=['p'])
async def projects_command(ctx):
    payload = requests.get('https://api.github.com/users/hackbacc/repos').text
    for project in json.loads(payload):
        await ctx.send(project['full_name'] + " -\n " + project['html_url'] + " - " + str(project['description']))

@bot.command(name='cmds', aliases=['c'])
async def cmds_command(ctx):
    cmds = []
    for f in funcs:
        if f.endswith('_command'):
            cmds.append("!"+f.split('_')[0])
    await ctx.send('available cmds are - ' + ' '.join(cmds))

funcs = locals().keys()
bot.run()

import discord,json,os,random
from discord.ext import commands, tasks
from discord.ext.commands import cooldown, BucketType, CommandNotFound
from bs4 import BeautifulSoup
import requests
import re
from samp_client.client import SampClient


URLL = "https://www.lsgyvenimas.lt/d-baze/adminai"
pagee = requests.get(URLL)

URL1 = "https://www.lsgyvenimas.lt/d-baze/direk"
page1 = requests.get(URL1)

listadm = []
listonline= []





with open("config.json") as file: # config failo uzkrovimas
    info = json.load(file)
    token = info["token"]
    prefix = info["prefix"]

bot = commands.Bot(command_prefix=prefix, activity=discord.Game(name="Plaunu indus"), status=discord.Status.do_not_disturb)

@bot.event
async def on_ready():
    print("Botas dirba!")
    if not loop.is_running():
        loop.start()
    
    
    
@tasks.loop(seconds=35)
async def loop():
    with SampClient(address='54.36.124.11', port=7777) as client:
      lst = []
      for client in client.get_server_clients():
            listonline.append(f"{client.name}")
      joined = "\n".join(listonline) + '\n'
    URL = "https://lsgyvenimas.lt/monitor/index.php"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    divs = soup.findAll("table", {"class": "table table-bordered table-striped"})  
    for div in divs:
     row = ''
     rows = div.findAll('tr')
     for row in rows:
      if(row.text.find("/") > -1):
            pattern = re.compile(r'\s+')
            sentence = re.sub(pattern, '',row.text)
            await bot.change_presence(activity=discord.Game(name="Online: " + sentence))  
    soup = BeautifulSoup(pagee.content, "html.parser")
    divs = soup.findAll("table", {"class": "bga"})  
    for div in divs:
     row = ''
     rows = div.findAll('td')
     lst=[]
     for row in rows:
        if(row.text.find("_") > -1):
         listadm.append(row.text)


        
   
          
            
@bot.command() 
async def admin(ctx):
 soup = BeautifulSoup(pagee.content, "html.parser")
 divs = soup.findAll("table", {"class": "bga"})  
 for div in divs:
    row = ''
    rows = div.findAll('td')
    lst=[]
    for row in rows:
        if(row.text.find("_") > -1):
         lst.append(row.text)
    joined_string ="\n".join(lst)  
    adm = discord.Embed(title="ADMINAI",description=joined_string) # Define embed
    await ctx.send(embed=adm) # siust embed 
    
@bot.command() 
async def drk(ctx):
 soup = BeautifulSoup(page1.content, "html.parser")
 divs = soup.findAll("table", {"class": "bga"})  
 for div in divs:
    row = ''
    rows = div.findAll('td')
    lst=[]
    for row in rows:
        if(row.text.find("") > -1):
         lst.append(row.text)
    joined_string ="\n".join(lst) + '\n'  
    adm = discord.Embed(title="DIREKTORIAI",description=joined_string) # Define embed
    await ctx.send(embed=adm) # siust embed 


@bot.command()
async def online(ctx):
 with SampClient(address='54.36.124.11', port=7777) as client:
      for client in client.get_server_clients():
            listonline.append(f"{client.name}")
      joined = "\n".join(listonline) + '\n'
 soup = BeautifulSoup(pagee.content, "html.parser")
 divs = soup.findAll("table", {"class": "bga"})  
 for div in divs:
    row = ''
    rows = div.findAll('td')
    listadm =[]
    for row in rows:
        if(row.text.find("_") > -1):
         listadm.append(row.text)
    joined_string ="\n".join(listadm) 
 admon = (list(set(listonline) & set(listadm)))
 joined_ ="\n".join(admon)
 admx = discord.Embed(title="ADMINAI ONLINE",description=joined_) # Define embed
 await ctx.send(embed = admx)
                         
            
@bot.command()
async def check(ctx):
 with SampClient(address='54.36.124.11', port=7777) as client:
      lst = []
      for client in client.get_server_clients():
            lst.append(f"{client.name}")
      joined = "\n".join(lst) + '\n'
    
    
    
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
     await ctx.send("Tokios komandos nera `*pagalba` ")    
    return    

@bot.command() 
async def pagalba(ctx):
     await ctx.send("`*drk` - parodo direktoriu sarasa\n`*admin` - parodo admin sarasa\n`*online` - parodo prisijungusius adminus\n`*prisijunges [nick]` - parodo ar zaidejas yra prisijunges")   
     
@bot.command() 
async def prisijunges(ctx, arg):
    if arg in listonline:
        await ctx.send(f'Zaidejas `{arg}` yra prisijunges')
    else:
         await ctx.send(f'Zaidejas `{arg}` nera prisijunges')   
bot.run(token)    
